import re

from sqlalchemy.dialects import registry
from sqlalchemy.dialects.mssql.base import MSDialect, MSExecutionContext
from sqlalchemy.sql import text

registry.register('devart.ase', 'devart.ase.sqlalchemy', 'DevartASEDialect')

class ASEExecutionContext(MSExecutionContext):
    def pre_exec(self):
        if self.isinsert:
            self._select_lastrowid = (
                not self.compiled.inline
                and not self.compiled.effective_returning
                and not self.executemany
            )

    def post_exec(self):
        if self.isinsert or self.isupdate or self.isdelete:
            self._rowcount = self.cursor.rowcount

class DevartASEDialect(MSDialect):
    driver = "devart"
    name = "ase"

    execution_ctx_cls = ASEExecutionContext

    supports_statement_cache = False
    supports_multivalues_insert = False
    default_paramstyle = "named"

    @classmethod
    def import_dbapi(cls):
        import devart.ase
        return devart.ase

    def _setup_version_attributes(self):
        super()._setup_version_attributes()
        self.supports_multivalues_insert = False

    def _get_default_schema_name(self, connection):
        return ""

    def _get_server_version_info(self, connection):
        vers = connection.exec_driver_sql("select @@version").scalar()
        m = re.match(r"Adaptive .*\/(\d+)\.(\d+)\.(\d+)", vers)
        if m:
            return tuple(int(x) for x in m.group(1, 2, 3))
        else:
            return None

    def _setup_supports_nvarchar_max(self, connection):
        self._supports_nvarchar_max = False

    def _internal_has_table(self, connection, tablename, owner, **kw):
        return bool(connection.scalar(text('SELECT object_id("{}")'.format(tablename))))