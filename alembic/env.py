from logging.config import fileConfig
from sqlalchemy import create_engine
from alembic import context

import os
import sys

from database.models.base import Base

# Ensure the 'models' directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'database', 'models')))

# This is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Auto-discover models by importing them dynamically
# Loop through the models directory and import everything
import database.models  # Assuming models are in 'database/models'

# Provide the target metadata for Alembic to work with
# Alembic will use all models that are registered in `Base.metadata`
target_metadata = Base.metadata  # Set target_metadata to your Base's metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    engine = create_engine("postgresql://endsem_root_user_dev:endsem_root_pwd@localhost:5432/endsem_development")

    with engine.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
