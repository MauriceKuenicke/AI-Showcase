from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from alembic.ddl import impl
import os
from dotenv import load_dotenv
import snowflake.sqlalchemy  # Import to register the Snowflake dialect

# Custom Snowflake implementation for Alembic
class SnowflakeImpl(impl.DefaultImpl):
    __dialect__ = 'snowflake'
# Register the Snowflake implementation with Alembic
impl._impls['snowflake'] = SnowflakeImpl

load_dotenv()

config = context.config

def run_migrations_online() -> None:
    """Run migrations in 'online' mode with proper error handling."""
    configuration = config.get_section(config.config_ini_section)

    db_url = os.getenv("APP__SF__SQL_ALCHEMY_CONN")
    if not db_url:
        raise ValueError(
            f"Environment variable 'APP__SF__SQL_ALCHEMY_CONN' is not set. "
        )
    
    configuration["sqlalchemy.url"] = db_url

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    raise NotImplementedError("Offline mode is not implemented")
else:
    run_migrations_online()