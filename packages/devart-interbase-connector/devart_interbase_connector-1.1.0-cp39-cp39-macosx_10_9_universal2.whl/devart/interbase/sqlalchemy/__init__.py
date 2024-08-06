from sqlalchemy.dialects import registry
from sqlalchemy_firebird.base import FBDialect

registry.register('devart.interbase', 'devart.interbase.sqlalchemy', 'DevartInterBaseDialect')

class DevartInterBaseDialect(FBDialect):
    driver = "devart"
    name = "interbase"

    supports_statement_cache = False
    default_paramstyle = "named"

    @classmethod
    def import_dbapi(cls):
        import devart.interbase
        return devart.interbase

    def _get_server_version_info(self, connection):
        return (3, 10,)