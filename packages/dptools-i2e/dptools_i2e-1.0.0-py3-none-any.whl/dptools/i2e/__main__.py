import argparse
from importlib.metadata import version


def main():
    from . import log

    parser = argparse.ArgumentParser()

    parser.add_argument('--version', action='version', version=f'%(prog)s {version("dptools-i2e")}')

    parser.add_argument("--pg-host", help="PostgreSQL host", type=str, default="localhost")
    parser.add_argument("--pg-port", help="PostgreSQL port", type=int, default=5432)
    parser.add_argument("--pg-user", help="PostgreSQL user", type=str, default="postgres")
    parser.add_argument("--pg-password", help="PostgreSQL password", type=str, default="")

    parser.add_argument("--edb-host", help="EdgeDB host", type=str, default="localhost")
    parser.add_argument("--edb-port", help="EdgeDB port", type=int, default=5656)
    parser.add_argument("--edb-user", help="EdgeDB user", type=str, default="edgedb")
    parser.add_argument("--edb-password", help="EdgeDB password", type=str, default="")

    parser.add_argument("--dry-run", help="Dry run", action="store_true")

    parser.add_argument("-d", "--database", help="DeepModel database", type=str, required=True)

    parser.add_argument("--log-to", help="Logging destination", type=str, default="result.log")

    args = parser.parse_args()
    log.setup(args.log_to)

    from . import internal_to_external, pg, edb
    edb_con = edb.EDBConnection(
        host=args.edb_host,
        port=args.edb_port,
        user=args.edb_user,
        password=args.edb_password,
    )

    pg_con = pg.PGConnection(
        host=args.pg_host,
        port=args.pg_port,
        user=args.pg_user,
        password=args.pg_password,
    )

    with pg_con.connect_to(args.database, mangle_database=False) as conn:
        conn.execute("SELECT space, edgedb_name from deepmodel_space_connection_config")
        space_to_db = conn.fetchall()

    internal_to_external.main(space_to_db, edb_con, pg_con, args.dry_run)


if __name__ == "__main__":
    main()
