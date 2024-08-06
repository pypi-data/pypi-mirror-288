from sqlalchemy.dialects import registry
from sqlalchemy.dialects.oracle.base import OracleDialect

registry.register('devart.oracle', 'devart.oracle.sqlalchemy', 'DevartOracleDialect')

class DevartOracleDialect(OracleDialect):
    driver = "devart"
    name = "oracle"

    supports_statement_cache = False
    default_paramstyle = "named"

    @classmethod
    def import_dbapi(cls):
        import devart.oracle
        return devart.oracle

    def _get_server_version_info(self, connection):
        cursor = connection.exec_driver_sql("select version from v$instance;")
        if not cursor._soft_closed:
            version = cursor.fetchone()
        else:
            version = []
        return tuple(int(x) for x in version[0].split("."))