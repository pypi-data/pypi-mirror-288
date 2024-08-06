from sqlalchemy.dialects import registry
from sqlalchemy.dialects.mysql.base import MySQLDialect

registry.register('devart.mysql', 'devart.mysql.sqlalchemy', 'DevartMySQLDialect')

class DevartMySQLDialect(MySQLDialect):
    driver = "devart"
    name = "mysql"

    supports_statement_cache = False
    default_paramstyle = "named"

    @classmethod
    def import_dbapi(cls):
        import devart.mysql
        return devart.mysql

    def _extract_error_code(self, exception):
        return exception.args[0]

    def _detect_charset(self, connection):
        cursor = connection.exec_driver_sql("SHOW VARIABLES LIKE 'character_set%%'")
        if not cursor._soft_closed:
            charset = cursor.fetchone()
        else:
            charset = []
        if charset != None and len(charset) > 0:
            return charset[0]
        else:
            return "latin1"

    def has_table(self, connection, table_name, schema=None, **kw):
        self._ensure_has_table_connection(connection)
        if schema is None:
            schema = self.default_schema_name
        full_name = ".".join(self.identifier_preparer._quote_free_identifiers(schema, table_name))
        try:
            with connection.exec_driver_sql("DESCRIBE {}".format(full_name), execution_options={"skip_user_error_events": True},) as rs:
                return rs.fetchone() is not None
        except Exception as e:
            if "doesn't exist" in e.orig.args[0]:
                return False
            raise
