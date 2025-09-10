from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
import sys
from pathlib import Path
import asyncio

# Добавляем корень проекта в sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

# Импорты
from database.config import DB_HOST, DB_PORT, DB_USER, DB_NAME, DB_PASS
from database.database import Base
from models import user_model, recipe_model, collection_model, comment_model, rating_model

target_metadata = Base.metadata
config = context.config
section = config.config_ini_section

config.set_section_option(section, "DB_HOST", DB_HOST)
config.set_section_option(section, "DB_PORT", str(DB_PORT))
config.set_section_option(section, "DB_USER", DB_USER)
config.set_section_option(section, "DB_NAME", DB_NAME)
config.set_section_option(section, "DB_PASS", DB_PASS)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_offline():
    url = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online_async():
    connectable = create_async_engine(
        f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        poolclass=pool.NullPool
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    asyncio.run(run_migrations_online_async())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
