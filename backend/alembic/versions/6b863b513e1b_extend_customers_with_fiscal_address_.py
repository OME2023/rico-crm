"""extend customers with fiscal + address fields (sqlite-safe, idempotent)"""
from alembic import op
import sqlalchemy as sa

revision = '6b863b513e1b'
down_revision = 'b89e08c0379e'
branch_labels = None
depends_on = None

def _has_column_sqlite(bind, table: str, column: str) -> bool:
    rows = bind.exec_driver_sql(f"PRAGMA table_info({table})").fetchall()
    names = {row[1] for row in rows}  # row[1] = column name
    return column in names

def _add_col_if_missing(bind, table: str, column: str, ddl: str):
    if not _has_column_sqlite(bind, table, column):
        op.execute(f'ALTER TABLE {table} ADD COLUMN {column} {ddl}')

def upgrade():
    bind = op.get_bind()
    # Usamos SQL crudo con verificación previa por PRAGMA (evita duplicados)
    _add_col_if_missing(bind, 'customers', 'dni',               'VARCHAR(20)')
    _add_col_if_missing(bind, 'customers', 'phone',             'VARCHAR(50)')
    _add_col_if_missing(bind, 'customers', 'address_street',    'VARCHAR(120)')
    _add_col_if_missing(bind, 'customers', 'address_number',    'VARCHAR(20)')
    _add_col_if_missing(bind, 'customers', 'address_floor',     'VARCHAR(10)')
    _add_col_if_missing(bind, 'customers', 'address_apartment', 'VARCHAR(10)')
    _add_col_if_missing(bind, 'customers', 'neighborhood',      'VARCHAR(80)')
    _add_col_if_missing(bind, 'customers', 'cuit',              'VARCHAR(20)')
    _add_col_if_missing(bind, 'customers', 'fiscal_condition',  'VARCHAR(40)')

def downgrade():
    # SQLite no soporta DROP COLUMN antes de 3.35; omitimos downgrade seguro.
    pass
