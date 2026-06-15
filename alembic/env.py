"""
alembic/env.py
--------------
Alembic environment configuration for async SQLAlchemy with SQLite.

Key points
~~~~~~~~~~
* ``run_migrations_online`` uses ``AsyncEngine`` so Alembic can work with
  the same async engine used by the application.
* ``target_metadata`` points at ``Base.metadata`` so ``alembic revision
  --autogenerate`` can diff the current database schema against the ORM models.
* Import all model modules before ``Base.metadata`` is passed to Alembic so
  every table is registered.
"""

from __future__ import annotations

import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# ── Alembic Config ──────────────────────────────────────────────────────────
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ── Application imports ──────────────────────────────────────────────────────
# Import Base (and all models so they register on metadata) before passing
# target_metadata to Alembic.
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from app.database.base import Base  # noqa: E402

from app.models.user import User
from app.models.weight_log import WeightLog
from app.models.measurement_session import MeasurementSession

target_metadata = Base.metadata

# ── Pull database URL from app settings ─────────────────────────────────────
from app.core.config import get_settings  # noqa: E402

_settings = get_settings()
config.set_main_option("sqlalchemy.url", _settings.DATABASE_URL)


# ── Offline migrations ───────────────────────────────────────────────────────
def run_migrations_offline() -> None:
    """Emit SQL to stdout without a live database connection."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,  # Required for SQLite ALTER support
    )
    with context.begin_transaction():
        context.run_migrations()


# ── Online migrations ────────────────────────────────────────────────────────
def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        render_as_batch=True,  # Required for SQLite ALTER support
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Create an async engine and run migrations within a sync runner."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


# ── Entry point ──────────────────────────────────────────────────────────────
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
