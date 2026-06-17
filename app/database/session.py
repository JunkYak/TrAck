"""
app/database/session.py
-----------------------
Async SQLAlchemy engine and session factory.

Design decisions
~~~~~~~~~~~~~~~~
* **aiosqlite** is used as the async driver for SQLite.
* ``expire_on_commit=False`` prevents accidental lazy-load after a commit
  inside async code (which would raise ``MissingGreenlet``).
* The ``get_db_session`` generator is the canonical FastAPI dependency; it is
  re-exported through ``app/core/dependencies.py`` so routers have a single
  import location.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import get_settings

settings = get_settings()

from sqlalchemy import event
from sqlalchemy.engine import Engine

# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------
engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    # echo SQL only in debug/dev mode – never in production.
    echo=settings.APP_DEBUG and not settings.is_production,
    # SQLite-specific: disable same-thread check for async usage.
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    # Pool tuning (SQLite is file-based so a small pool is fine).
    pool_pre_ping=True,
)

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if "sqlite" in settings.DATABASE_URL:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

# ---------------------------------------------------------------------------
# Session factory
# ---------------------------------------------------------------------------
AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


# ---------------------------------------------------------------------------
# Dependency / context-manager
# ---------------------------------------------------------------------------
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield an :class:`AsyncSession` scoped to a single request.

    The session is committed on success and rolled back on any exception,
    then always closed.  Use via ``Depends(get_session)`` in route handlers.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


@asynccontextmanager
async def get_db_context() -> AsyncGenerator[AsyncSession, None]:
    """Context-manager variant for use outside of FastAPI routes (e.g. scripts)."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
