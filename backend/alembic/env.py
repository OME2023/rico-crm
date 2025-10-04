from logging.config import fileConfig
import os, sys
from alembic import context

# Asegura que 'backend/' esté en sys.path para importar 'app.*'
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.db.session import Base, engine  # noqa

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Offline: genera SQL sin ejecutar."""
    url = str(engine.url)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True if engine.name == "sqlite" else False,
        literal_binds=True,   # SOLO offline
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Online: ejecuta contra la DB."""
    connectable = engine
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True if connection.engine.name == "sqlite" else False,
            # NO literal_binds aquí (causa el error)
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
