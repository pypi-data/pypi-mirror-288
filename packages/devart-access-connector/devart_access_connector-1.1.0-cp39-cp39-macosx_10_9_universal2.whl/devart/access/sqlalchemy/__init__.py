from sqlalchemy.dialects import registry
from sqlalchemy.dialects.sqlite.base import SQLiteDialect

registry.register('devart.access', 'devart.access.sqlalchemy', 'DevartAccessDialect')

class DevartAccessDialect(SQLiteDialect):
    driver = "devart"
    name = "access"

    supports_statement_cache = False
    default_paramstyle = "named"

    @classmethod
    def import_dbapi(cls):
        import devart.access
        access_package = devart.access
        setattr(access_package, "sqlite_version_info", (3, 39, 2))
        return access_package

    def get_isolation_level(self, dbapi_connection):
        return "SERIALIZABLE"

    def _get_table_pragma(self, connection, pragma, table_name, schema=None):
        quote = self.identifier_preparer.quote_identifier
        qtable = quote(table_name)
        statement = "PRAGMA {}({})".format(pragma, qtable)
        cursor = connection.exec_driver_sql(statement)
        if not cursor._soft_closed:
            result = cursor.fetchall()
        else:
            result = []
        if result:
            return result