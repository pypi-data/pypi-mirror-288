from sqlalchemy.dialects import registry
from sqlalchemy.dialects.sqlite.base import SQLiteDialect
from sqlalchemy.dialects.sqlite.base import SQLiteIdentifierPreparer

registry.register('devart.bigquery', 'devart.bigquery.sqlalchemy', 'DevartBigQueryDialect')

class DevartBigQueryIdentifierPreparer(SQLiteIdentifierPreparer):
    def __init__(
        self,
        dialect,
        initial_quote='"',
        final_quote=None,
        escape_quote='"',
        quote_case_sensitive_collations=True,
        omit_schema=False,
    ):
        super().__init__(dialect, "", "", escape_quote, quote_case_sensitive_collations, omit_schema)

class DevartBigQueryDialect(SQLiteDialect):
    driver = "devart"
    name = "bigquery"

    supports_statement_cache = False

    preparer = DevartBigQueryIdentifierPreparer

    @classmethod
    def import_dbapi(cls):
        import devart.bigquery
        bigquery_package = devart.bigquery
        setattr(bigquery_package, "sqlite_version_info", (3, 39, 2))
        return bigquery_package

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.paramstyle = "qmark"

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