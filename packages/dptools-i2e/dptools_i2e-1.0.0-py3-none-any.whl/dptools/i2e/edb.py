import ssl

from typing import NamedTuple, Dict

import edgedb
from edgedb import platform
import edgedb.con_utils as edcu


class Config(edcu.ResolvedConnectConfig):
    @property
    def ssl_ctx(self):
        if (self._ssl_ctx):
            return self._ssl_ctx

        self._ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self._ssl_ctx.check_hostname = self.tls_security == "strict"
        self._ssl_ctx.verify_mode = ssl.CERT_NONE
        if self._tls_ca_data:
            self._ssl_ctx.load_verify_locations(
                cadata=self._tls_ca_data
            )
        else:
            self._ssl_ctx.load_default_certs(ssl.Purpose.SERVER_AUTH)
            if platform.IS_WINDOWS:
                import certifi
                self._ssl_ctx.load_verify_locations(cafile=certifi.where())
        self._ssl_ctx.set_alpn_protocols(['edgedb-binary'])

        return self._ssl_ctx


edcu.ResolvedConnectConfig = Config


class EDBConnection(NamedTuple):
    host: str
    port: int = 5656
    user: str = 'edgedb'
    password: str = ''


def create_client(database: str, conn: EDBConnection) -> edgedb.Client:
    return edgedb.create_client(
        **conn._asdict(),
        database=database,
        tls_security='insecure',
    )
