from sqlalchemy.dialects import registry
from sqlalchemy.dialects.sqlite.base import SQLiteDialect

registry.register('devart.salesforce', 'devart.salesforce.sqlalchemy', 'DevartSalesforceDialect')

class DevartSalesforceDialect(SQLiteDialect):
    driver = "devart"
    name = "salesforce"

    supports_statement_cache = False
    default_paramstyle = "named"

    @classmethod
    def import_dbapi(cls):
        import devart.salesforce
        salesforce_package = devart.salesforce
        setattr(salesforce_package, "sqlite_version_info", (3, 39, 2))
        return salesforce_package

    def get_isolation_level(self, dbapi_connection):
        return "SERIALIZABLE"
    
    def has_table(self, connection, table_name, schema=None, **kw):
        self._ensure_has_table_connection(connection)
        query = "select QualifiedApiName as name from EntityDefinition where QualifiedApiName = '{}'".format(table_name)
        names = connection.exec_driver_sql(query).scalars().all()
        return len(names) > 0
    
    def get_table_names(
        self, connection, schema=None, sqlite_include_internal=False, **kw
    ):
        query = "select QualifiedApiName as name from EntityDefinition where IsCustomizable = true order by QualifiedApiName"
        names = connection.exec_driver_sql(query).scalars().all()
        return names
