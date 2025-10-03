from logging.config import fileConfig
from sqlalchemy import pool
from alembic import context
from sqlalchemy import create_engine
import os, sys

# Asegura que 'backend' esté en sys.path para importar 'app'
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # .../backend
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.db.session import Base
from app.core.config import settings
import app.models  # registra todos los modelos

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline():
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = create_engine(settings.DATABASE_URL, poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
