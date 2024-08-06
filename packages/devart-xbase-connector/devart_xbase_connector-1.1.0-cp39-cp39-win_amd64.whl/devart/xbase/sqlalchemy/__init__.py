from sqlalchemy.dialects import registry
from sqlalchemy.dialects.sqlite.base import SQLiteDialect

registry.register('devart.xbase', 'devart.xbase.sqlalchemy', 'DevartxBaseDialect')

class DevartxBaseDialect(SQLiteDialect):
    driver = "devart"
    name = "xbase"

    supports_statement_cache = False
    default_paramstyle = "named"

    @classmethod
    def import_dbapi(cls):
        import devart.xbase
        xbase_package = devart.xbase
        setattr(xbase_package, "sqlite_version_info", (3, 39, 2))
        return xbase_package

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