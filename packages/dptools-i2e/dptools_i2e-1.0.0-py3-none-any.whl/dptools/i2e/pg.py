import contextlib
from dataclasses import dataclass
from typing import Optional, Literal, Dict, ContextManager

import psycopg2
from psycopg2._psycopg import cursor  # noqa


@dataclass
class PGConnection:
    host: str = 'localhost'
    port: int = 5432
    user: str = 'postgres'
    password: Optional[str] = None

    def _get_connection_info(
        self,
        database: str,
        mangle_database: bool = True,
    ):
        if database.startswith('+'):
            database = database[1:-1]
        elif mangle_database:
            database = f"V2f147ded60_{database}"
        conn_info = {
            'host': self.host,
            'port': self.port,
            'user': self.user,
            'database': database,
        }
        if self.password:
            conn_info['password'] = self.password
        return conn_info

    @contextlib.contextmanager
    def connect_to(
        self,
        database: str,
        auto_commit: bool = False,
        mangle_database: bool = True,
    ) -> cursor:
        conn = cur = None
        try:
            conn = psycopg2.connect(
                **self._get_connection_info(database, mangle_database))
            cur = conn.cursor()
            yield cur
            if auto_commit:
                conn.commit()
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()


def connect_to(
    database: str,
    conn: PGConnection,
    auto_commit: bool = False
) -> ContextManager[cursor]:
    return conn.connect_to(database, auto_commit=auto_commit)
