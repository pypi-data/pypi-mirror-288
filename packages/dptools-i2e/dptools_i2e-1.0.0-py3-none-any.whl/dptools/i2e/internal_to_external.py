import functools
import itertools
import sys
import textwrap
import urllib.error
import urllib.request
import uuid
from dataclasses import dataclass
from typing import *

import edgedb
from edgedb.enums import Cardinality

from . import edb, pg, req, structs, log
from .structs import CreateObjectType


logger = log.get_logger(__name__)

SQL = str
EDGEQL = str
S = TypeVar('S', bound=str)

DATABASE: str = None # noqa
CLIENT: edgedb.Client = None # noqa
DRY_RUN: bool = False
PGCON: pg.PGConnection = None # noqa


class ObjectType(NamedTuple):
    name: str
    primary_key: str


class Link(NamedTuple):
    name: str
    source: ObjectType


class Constraint(NamedTuple):
    name: str
    subjectexpr: str = ''


def unwrap_bracket(s: str, lb: str = '(', rb: str = ')') -> str:
    if (
        (li := s.find(lb)) >= 0
        and (ri := s.rfind(rb)) >= 0
    ):
        return unwrap_bracket(s[li + 1: ri], lb, rb)
    else:
        return s


def validate(objtype: CreateObjectType):
    schema = _get_object_schema(objtype.qualname)

    create_props = set(prop.realname for prop in objtype.properties)
    create_links = set(prop.realname for prop in objtype.links)

    missing = []
    for prop in schema.properties:
        if prop.name == 'id':
            continue
        if prop.name not in create_props:
            missing.append(('property', prop.name))

    for link in schema.links:
        if link.name == '__type__':
            continue
        if link.name not in create_links:
            missing.append(('link', link.name))

    if missing:
        msg = '\n'.join(f"{tp}: {name}" for tp, name in missing)
        print(f"Missing:\n{textwrap.indent(msg, ' ')}", file=sys.stderr)
        sys.exit(1)


def alter_link_pk2pk(objtype: str) -> Tuple[List[EDGEQL], List[EDGEQL], List[EDGEQL]]:
    def to_objtype(obj):
        if not obj.annotations:
            pri_key = _get_primary_key(obj.name, DATABASE)
        else:
            pri_key = obj.annotations[0].v
        return ObjectType(obj.name, pri_key)

    pre_ddl = {}
    post_ddl = {}

    target_obj = CLIENT.query_single("""\
        select schema::ObjectType {
            name, 
            annotations: { v := @value } filter .name like '%%business_key'
        } filter .name = '%s' limit 1
    """ % objtype)

    def check_link_src_constraint(link: Link):
        link_source = link.source.name
        for constraint in _get_objtype_constraint(link_source):
            if constraint.name != 'std::exclusive':
                continue

            constraint_name = unwrap_bracket(constraint.subjectexpr)
            fields = list(map(str.strip, constraint_name.split(',')))

            if not all(s.startswith('.') for s in fields):
                continue

            if '.' + link.name in fields:
                pre_ddl[textwrap.dedent(f"""\
                    ALTER TYPE {link_source} drop constraint exclusive on ({constraint.subjectexpr});\
                """)] = None
                post_ddl[textwrap.dedent(f"""\
                    ALTER TYPE {link_source} create constraint exclusive on ({constraint.subjectexpr});\
                """)] = None

    links = []
    for link in CLIENT.query("""\
        select schema::Link {
            name, 
            src := .source[IS schema::ObjectType] {
                name,
                annotations: { v := @value } filter .name like '%%business_key'
            },
            sp := .source_property.name,
            tp := .target_property.name 
        } filter .target.name = '%s' and not exists .expr 
    """ % objtype):
        if link.tp is not None:
            continue
        try:
            links.append(Link(name=link.name, source=to_objtype(link.src)))
        except ValueError:
            if _is_global(link.src.name):
                continue
            elif DRY_RUN:
                logger.opt(exception=True).warning(f"cannot resolve primary key for link source {link.src.name}. detail: {link.src}")
                continue
            else:
                raise

        check_link_src_constraint(links[-1])
        if cons := _get_link_constraint(link.id):
            if len(cons) == 1 and cons[0].name == 'std::exclusive':
                pre_ddl[textwrap.dedent(f"""\
                    ALTER TYPE {link.src.name} {{ 
                        ALTER LINK {link.name} {{drop constraint exclusive}}
                    }};\
                """)] = None
                post_ddl[textwrap.dedent(f"""\
                    ALTER TYPE {link.src.name} {{ 
                        ALTER LINK {link.name} {{create constraint exclusive}}
                    }};\
                """)] = None
            else:
                msg = f'Link {link.src.name}.{link.name} has constraint {cons}.'
                if DRY_RUN:
                    logger.warning(msg)
                else:
                    raise ValueError(msg)
    try:
        pk = to_objtype(target_obj).primary_key
    except ValueError:
        if DRY_RUN:
            logger.warning(f"cannot resolve primary key for {target_obj.name}. detail: {target_obj}", exc_info=True)
            return []
        else:
            raise

    return (
        list(pre_ddl.keys()),
        [textwrap.dedent(f"""\
            ALTER TYPE {link.source.name} {{
                ALTER LINK {link.name} on {link.source.primary_key} TO {pk}
            }}
        """) for link in links],
        list(reversed(post_ddl.keys()))
    )


@dataclass
class BaseObject:
    id: uuid.UUID
    name: str


@dataclass
class SchemaPointer(BaseObject):
    cardinality: Cardinality


@dataclass
class SchemaObjType(BaseObject):
    properties: List[SchemaPointer]
    links: List[SchemaPointer]
    external: bool


@dataclass
class SchemaLink(BaseObject):
    pointers: List[BaseObject]


@functools.lru_cache(maxsize=None)
def _get_primary_key(objtype: str, database: str) -> str:
    module, obj = objtype.split('::')
    if module.startswith('space'):
        if obj == 'SystemUser':
            return 'user_id'
        else:
            raise ValueError(f"Unknonw space object {objtype}")

    assert module.startswith('app')
    app = module[3:]

    with pg.connect_to(database, PGCON) as conn:
        conn.execute(f"""\
            SELECT field_code from app{app}_md_object_field
            where app = '{app}' and object_code = '{obj}' and whether_business_key = 1
        """)
        fields = conn.fetchall()
        if len(fields) == 0:
            raise ValueError(f"Cannot find primary key for {objtype}")
        elif len(fields) > 1:
            schema = _get_object_schema(objtype)
            props = set(prop.name for prop in schema.properties)
            field_names = set(fl[0] for fl in fields)

            valid_fields = field_names.intersection(props)
            if len(valid_fields) == 1:
                return valid_fields.pop()
            raise ValueError(f"Multiple primary key in {objtype}: {valid_fields}")
        return fields[0][0]


@functools.lru_cache(maxsize=None)
def _is_global(objtype: str) -> bool:
    try:
        CLIENT.query(f"select {objtype} limit 1")
        return False
    except edgedb.InvalidReferenceError:
        return True


@functools.lru_cache(maxsize=None)
def _get_link_constraint(link_id: str) -> List[Constraint]:
    return CLIENT.query("""\
        select schema::Constraint {
            lk := .subject[IS schema::Link],
            name
        } filter .lk.id = <uuid>'%s'
    """ % link_id)


@functools.lru_cache(maxsize=None)
def _get_objtype_constraint(objtype: str) -> List[Constraint]:
    return CLIENT.query("""\
        select schema::Constraint {
            obj := .subject[IS schema::ObjectType],
            name,
            subjectexpr
        } filter .obj.name = '%s'
    """ % objtype)


@functools.lru_cache(maxsize=None)
def _get_object_schema(obj: str) -> SchemaObjType:
    return CLIENT.query_single("""\
        select schema::ObjectType {
            id,
            name,
            properties: { id, name, cardinality },
            links: { id, name, cardinality },
            external
        } filter .name = '%s' 
        limit 1
    """ % obj)


@functools.lru_cache(maxsize=None)
def _get_link_schema(lid: str) -> SchemaLink:
    return CLIENT.query_single("""\
        select schema::Link {
            id,
            name,
            pointers: { id, name },
        } filter .id = <uuid>'%s' 
    """ % lid)


@functools.lru_cache(maxsize=None)
def _get_set_external_pgsql_template(name, reverse: bool = False) -> SQL:
    obj = _get_object_schema(f'schema::{name}')
    external_col = None
    for prop in obj.properties:
        if prop.name == 'external':
            external_col = prop.id
            break
    assert external_col is not None
    flag = 'false' if reverse else 'true'
    return textwrap.dedent(f"""\
        update edgedbstd."{obj.id}" set "{external_col}"={flag} 
        where id = '{{}}'::uuid RETURNING id\
    """)


def set_external_to_true(objtype: str, reverse: bool = False) -> List[SQL]:
    objtype_s = _get_object_schema(objtype)

    sqls = ["-- 更新schema中external字段为true (HACK)"]
    comment = "-- update {}({})"
    objtype_tmpl = _get_set_external_pgsql_template('ObjectType', reverse)
    prop_tmpl = _get_set_external_pgsql_template('Property', reverse)
    link_tmpl = _get_set_external_pgsql_template('Link', reverse)

    sqls.append(comment.format('schema::ObjectType', objtype))
    sqls.append(objtype_tmpl.format(objtype_s.id))
    for prop in objtype_s.properties:
        sqls.append(comment.format('schema::Property', prop.name))
        sqls.append(prop_tmpl.format(prop.id))

    for link in objtype_s.links:
        sqls.append(comment.format('schema::Link', link.name))
        sqls.append(link_tmpl.format(link.id))

        for lp in _get_link_schema(str(link.id)).pointers:
            sqls.append(comment.format('schema::Property', f"{link.name}.{lp.name}"))
            sqls.append(prop_tmpl.format(lp.id))
    return sqls


def backup_internal_table(objtype: str, reverse: bool = False) -> List[SQL]:
    objtype_s = _get_object_schema(objtype)
    sqls = ["-- 备份内部表的物理表和视图（改名）"]

    if reverse:
        def _rename(obj: BaseObject, hint: str):
            sqls.append(f'-- restore {hint}')
            sqls.append(f'ALTER TABLE IF EXISTS edgedbpub."bak_{obj.id}" RENAME TO "{obj.id}"')
            sqls.append(f'ALTER TABLE IF EXISTS edgedbpub."bak_{obj.id}_t" RENAME TO "{obj.id}_t"')
    else:
        def _rename(obj: BaseObject, hint: str):
            sqls.append(f'-- alter {hint}')
            sqls.append(f'ALTER TABLE IF EXISTS edgedbpub."{obj.id}" RENAME TO "bak_{obj.id}"')
            sqls.append(f'ALTER TABLE IF EXISTS edgedbpub."{obj.id}_t" RENAME TO "bak_{obj.id}_t"')

    _rename(objtype_s, objtype)

    for prop in objtype_s.properties:
        if prop.cardinality.value == 'Many':
            _rename(prop, f'{objtype}({prop.name})')

    for link in objtype_s.links:
        if link.cardinality.value == 'Many':
            _rename(link, f'{objtype}({link.name})')
        else:
            link_s = _get_link_schema(str(link.id))
            if len(link_s.pointers) > 2:
                _rename(link, f'{objtype}({link.name})')
    return sqls


def create_external_view(objtype: CreateObjectType, reverse: bool = False) -> List[SQL]:
    sqls = ["-- 创建外部表视图"]
    schema = _get_object_schema(objtype.qualname)
    external_view = objtype.resolve_view()

    name_to_link = {lk.name: lk for lk in schema.links}
    name_to_prop = {prop.name: prop for prop in schema.properties}

    view_def = objtype.view_def

    columns = [
        "edgedbext.uuid_generate_v1mc() AS id",
        f"'{str(schema.id)}'::uuid AS __type__"
    ]

    if reverse:
        def _create_view(qry: str, name: str, hint):
            sqls.extend([
                f'-- drop view for {hint}',
                f'DROP VIEW IF EXISTS edgedbpub."{name}"',
                f'DROP VIEW IF EXISTS edgedbpub."{name}_t"'
            ])
    else:
        def _create_view(qry: str, name: str, hint):
            sqls.extend([
                f'-- create view for {hint}',
                f'CREATE OR REPLACE VIEW edgedbpub."{name}" AS \n{qry}',
                f'CREATE OR REPLACE VIEW edgedbpub."{name}_t" AS \n{qry}'
            ])

    for prop in objtype.properties:
        if prop.expr is not None:
            # computable property has no physical column
            continue

        prop_id = str(name_to_prop[prop.realname].id)

        if prop.has_table:
            view = external_view[(objtype.qualname, prop.realname)]
            src_col = view.columns['source']
            tgt_col = view.columns['target']
            _create_view(
                textwrap.dedent(f"""\
                    SELECT 
                        SOURCE_T."{src_col}" AS "source",
                        SOURCE_T."{tgt_col}" AS "target" 
                    FROM (SELECT * FROM {view.relation}) AS SOURCE_T
                """),
                prop_id,
                f"{objtype.qualname}({prop.realname})"
            )
        else:
            ptrname = view_def.columns[prop.realname]
            columns.append(f'SOURCE_T."{ptrname}" AS "{prop_id}"')

    join_tables: List[Tuple[structs.ViewDef, str]] = []

    for link in objtype.links:
        if link.expr is not None:
            # computable link has no physical column
            continue

        link_id = str(name_to_link[link.realname].id)
        if link.has_table:
            if link.cardinality.is_multi():
                view = external_view[(objtype.qualname, link.realname)]
                src_col = view.columns['source']
                tgt_col = view.columns['target']
                lcols = [
                    f'SOURCE_T."{src_col}" AS "source"',
                    f'SOURCE_T."{tgt_col}" AS "target"'
                ]

                if link.properties:
                    link_s = _get_link_schema(link_id)
                    lp_to_id = {
                        prop.name: prop.id for prop in link_s.pointers
                    }
                    for prop in link.properties:
                        lcols.append(f'SOURCE_T."{prop.name}" AS "{str(lp_to_id[prop.realname])}"')

                _create_view(
                    textwrap.dedent(f"""\
                        SELECT {', '.join(lcols)} 
                        FROM (SELECT * FROM {view.relation}) AS SOURCE_T
                    """),
                    link_id,
                    f"{objtype.qualname}({link.realname})"
                )
            else:
                # single link with link-prop
                view = external_view[(objtype.qualname, link.realname)]
                src_id = view_def.columns[link.from_]
                ptrname = view.columns['target']
                columns.append(f'INNER_T{len(join_tables)}.{ptrname} AS "{link_id}"')
                join_tables.append((view, src_id))
        else:
            ptrname = view_def.columns[link.realname]
            columns.append(f'SOURCE_T."{ptrname}" AS "{link_id}"')

    column_str = textwrap.indent(',\n'.join(columns), ' '*4)
    query = textwrap.dedent(f"""\
        SELECT 
        {{}} 
        FROM (SELECT * FROM {view_def.relation}) 
        AS SOURCE_T
    """).format(column_str)

    for cnt, (view, src_id) in enumerate(join_tables):
        source = view.columns['source']
        target = view.columns['target']
        query += " " + textwrap.dedent(f"""\
            JOIN (SELECT "{source}", "{target}" FROM {view.relation}) AS INNER_T{cnt} 
                ON INNER_T{cnt}."{source}" = SOURCE_T.{src_id}
         """)

    _create_view(query, str(schema.id), objtype.qualname)
    return sqls


def introspect_schema():
    url = f'http://{HOST}:5656/introspect/{DATABASE}'

    try:
        with urllib.request.urlopen(url) as response:
            r = response.read().decode('utf-8')
            assert r == 'Done', r
    except urllib.error.URLError as e:
        print(f"Error fetching URL: {url} - {e}")
    except AssertionError as e:
        print(f"Assertion failed: {e}")


def filter_comment(sqls: Iterable[S]) -> Iterable[S]:
    for s in sqls:
        if not s.strip().startswith('--'):
            if DRY_RUN:
                logger.debug((' '.join(s.splitlines())))
            else:
                print(s)
            yield s
        else:
            logger.debug(s)


def go(body: dict):
    create_objtype = CreateObjectType.from_dict(body)
    objtype = create_objtype.qualname
    if (obj := _get_object_schema(objtype)) is None:
        logger.warning(f"{objtype} does not exist")
        return
    if obj.external:
        logger.warning(f"{objtype} is already external, skipping..")
        return

    validate(create_objtype)

    if DRY_RUN:
        for eql in filter_comment(itertools.chain(*alter_link_pk2pk(objtype))):
            pass

        for sql in filter_comment(itertools.chain(
            backup_internal_table(objtype),
            create_external_view(create_objtype),
            set_external_to_true(objtype)
        )):
            pass

    else:
        with pg.connect_to(DATABASE, PGCON, auto_commit=True) as conn:
            pre, ddl, post = alter_link_pk2pk(objtype)
            for tx in CLIENT.transaction():
                with tx:
                    for eql in filter_comment(pre):
                        tx.execute(eql)
            try:
                for eql in filter_comment(ddl):
                    CLIENT.execute(eql)
            finally:
                try:
                    for tx in CLIENT.transaction():
                        with tx:
                            for eql in filter_comment(post):
                                tx.execute(eql)
                except Exception:
                    print(post)
                    raise

            for sql in filter_comment(itertools.chain(
                backup_internal_table(objtype),
                create_external_view(create_objtype),
                set_external_to_true(objtype)
            )):
                conn.execute(sql)

        introspect_schema()


def rev(body: dict, pg_conn: pg.PGConnection):
    create_objtype = CreateObjectType.from_dict(body)
    objtype = create_objtype.qualname
    with pg.connect_to(DATABASE, pg_conn, auto_commit=True) as conn:
        for sql in filter_comment(itertools.chain(
                set_external_to_true(objtype, reverse=True),
                create_external_view(create_objtype, reverse=True),
                backup_internal_table(objtype, reverse=True),
        )):
            conn.execute(sql)

    introspect_schema()


def single(
    space: str,
    database: str,
    edb_conn: edb.EDBConnection,
    pg_conn: pg.PGConnection,
):
    logger.info(f"===> Processing {database} - {space}")

    global DATABASE, CLIENT, HOST, PGCON

    DATABASE = database
    HOST = edb_conn.host
    PGCON = pg_conn
    CLIENT = edb.create_client(database=DATABASE, conn=edb_conn)

    try:
        go(req.create(space))
    except Exception:  # noqa
        logger.exception(f"===> Failed with {database} - {space}")
    else:
        logger.info(f"===> Finish processing {database} - {space}")


def main(
    data: Iterable[Tuple[str, str]],
    edb_conn: edb.EDBConnection,
    pg_conn: pg.PGConnection,
    dry_run: bool
):
    global DRY_RUN
    DRY_RUN = dry_run

    logger.info(f"Dry run: {dry_run}")

    data = list(data)
    for i, (space, db) in enumerate(data, 1):
        logger.info(f"{i}/{len(data)}")
        single(space, db, edb_conn, pg_conn)
