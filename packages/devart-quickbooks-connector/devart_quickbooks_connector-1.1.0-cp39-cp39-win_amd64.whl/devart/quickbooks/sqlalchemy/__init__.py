from sqlalchemy.dialects import registry
from sqlalchemy.dialects.sqlite.base import SQLiteDialect

registry.register('devart.quickbooks', 'devart.quickbooks.sqlalchemy', 'DevartQuickBooksDialect')

class DevartQuickBooksDialect(SQLiteDialect):
    driver = "devart"
    name = "quickbooks"

    supports_statement_cache = False
    default_paramstyle = "named"

    @classmethod
    def import_dbapi(cls):
        import devart.quickbooks
        salesforce_package = devart.quickbooks
        setattr(salesforce_package, "sqlite_version_info", (3, 39, 2))
        return salesforce_package

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.supports_multivalues_insert = False

    def get_isolation_level(self, dbapi_connection):
        return "SERIALIZABLE"
    
    def has_table(self, connection, table_name, schema=None, **kw):
        self._ensure_has_table_connection(connection)
        query = "select TABLE_NAME as name from SYS_TABLES where TABLE_NAME = '{}'".format(table_name)
        names = connection.exec_driver_sql(query).scalars().all()
        return len(names) > 0
    
    def get_table_names(
        self, connection, schema=None, sqlite_include_internal=False, **kw
    ):
        query = "select TABLE_NAME as name from SYS_TABLES order by TABLE_NAME"
        names = connection.exec_driver_sql(query).scalars().all()
        return names