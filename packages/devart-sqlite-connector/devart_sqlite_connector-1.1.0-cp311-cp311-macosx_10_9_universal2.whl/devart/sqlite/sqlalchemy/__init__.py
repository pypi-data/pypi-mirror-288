from sqlalchemy.dialects import registry
from sqlalchemy.dialects.sqlite.base import SQLiteDialect

registry.register('devart.sqlite', 'devart.sqlite.sqlalchemy', 'DevartSQLiteDialect')

class DevartSQLiteDialect(SQLiteDialect):
    driver = "devart"
    name = "sqlite"

    supports_statement_cache = False
    default_paramstyle = "named"

    @classmethod
    def import_dbapi(cls):
        import devart.sqlite
        sqlite_package = devart.sqlite
        setattr(sqlite_package, "sqlite_version_info", (3, 39, 2))
        return sqlite_package

    def get_isolation_level(self, dbapi_connection):
        return "SERIALIZABLE"