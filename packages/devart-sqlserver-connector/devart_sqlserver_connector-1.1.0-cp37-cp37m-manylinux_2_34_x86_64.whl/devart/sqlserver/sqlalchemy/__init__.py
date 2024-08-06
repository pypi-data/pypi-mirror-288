import re

from sqlalchemy.dialects import registry
from sqlalchemy.dialects.mssql.base import MSDialect

registry.register('devart.sqlserver', 'devart.sqlserver.sqlalchemy', 'DevartSqlServerDialect')

class DevartSqlServerDialect(MSDialect):
    driver = "devart"
    name = "sqlserver"

    supports_statement_cache = False
    default_paramstyle = "named"

    @classmethod
    def import_dbapi(cls):
        import devart.sqlserver
        return devart.sqlserver

    def _get_server_version_info(self, connection):
        vers = connection.exec_driver_sql("select @@version").scalar()
        m = re.match(r"Microsoft .*? - (\d+)\.(\d+)\.(\d+)\.(\d+)", vers)
        if m:
            return tuple(int(x) for x in m.group(1, 2, 3, 4))
        else:
            return None
