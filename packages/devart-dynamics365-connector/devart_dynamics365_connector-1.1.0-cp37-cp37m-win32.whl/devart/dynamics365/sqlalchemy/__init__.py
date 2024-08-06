from sqlalchemy.dialects import registry
from sqlalchemy.dialects.sqlite.base import SQLiteDialect

registry.register('devart.dynamics365', 'devart.dynamics365.sqlalchemy', 'DevartDynamics365Dialect')

class DevartDynamics365Dialect(SQLiteDialect):
    driver = "devart"
    name = "dynamics365"

    supports_statement_cache = False
    default_paramstyle = "named"

    @classmethod
    def import_dbapi(cls):
        import devart.dynamics365
        dynamics365_package = devart.dynamics365
        setattr(dynamics365_package, "sqlite_version_info", (3, 39, 2))
        return dynamics365_package

    def get_isolation_level(self, dbapi_connection):
        return "SERIALIZABLE"
    
    def has_table(self, connection, table_name, schema=None, **kw):
        self._ensure_has_table_connection(connection)

        if schema is not None and schema not in self.get_schema_names(
            connection, **kw
        ):
            return False

        cursor = connection.connection.cursor()
        try:
            try:
                cursor.execute("select * from {} where 1 = 0".format(table_name))
                exists = True
            except:
                exists = False
        finally:
            cursor.close()
        return exists