from sqlalchemy.dialects import registry
from sqlalchemy_firebird.base import FBDialect

registry.register('devart.firebird', 'devart.firebird.sqlalchemy', 'DevartFirebirdDialect')

class DevartFirebirdDialect(FBDialect):
    driver = "devart"
    name = "firebird"

    supports_statement_cache = False
    default_paramstyle = "named"

    @classmethod
    def import_dbapi(cls):
        import devart.firebird
        return devart.firebird

    def _get_server_version_info(self, connection):
        vers = connection.exec_driver_sql("SELECT rdb$get_context('SYSTEM', 'ENGINE_VERSION') as version from rdb$database;").scalar()
        t = vers.split(".")
        return (int(t[0]), int(t[1]) + 10)