from sqlalchemy.dialects import registry
from sqlalchemy.dialects.postgresql.base import PGDialect

registry.register('devart.postgresql', 'devart.postgresql.sqlalchemy', 'DevartPostgreSqlDialect')

class DevartPostgreSqlDialect(PGDialect):
    driver = "devart"
    name = "postgresql"

    supports_statement_cache = False
    supports_server_side_cursors = False
    default_paramstyle = "named"

    @classmethod
    def import_dbapi(cls):
        import devart.postgresql
        return devart.postgresql