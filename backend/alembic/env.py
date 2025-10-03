import os, sys

# Agrega la carpeta 'backend/' al sys.path para poder importar 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from logging.config import fileConfig
from sqlalchemy import pool
from alembic import context
from sqlalchemy import create_engine
from app.db.session import Base
from app.core.config import settings
from app.models import ping  # importa tus modelos

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
