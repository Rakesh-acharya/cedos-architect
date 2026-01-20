from logging.config import fileConfig
from sqlalchemy import engine_from_config, create_engine
from sqlalchemy import pool
from alembic import context
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.core.database import Base
from app.core.config import settings
from app.models import *  # Import all models

# this is the Alembic Config object
config = context.config

# Override sqlalchemy.url with settings
# Use direct URL to avoid configparser interpolation issues with % characters
# Escape % by doubling them for configparser, or use direct engine creation
try:
    # Try to set it normally first
    config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
except ValueError:
    # If it fails due to interpolation, disable interpolation
    config.parser = config.parser.__class__(interpolation=None)
    config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    # Use direct URL from settings to avoid configparser interpolation issues
    url = settings.DATABASE_URL
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
    # Create engine directly from DATABASE_URL to avoid configparser interpolation issues
    # This handles URL-encoded passwords with % characters properly
    connectable = create_engine(
        settings.DATABASE_URL,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
