"""
app/repositories/base.py
------------------------
Generic async repository implementing basic CRUD operations.

All concrete repositories extend :class:`BaseRepository` and receive
a specific SQLAlchemy model type ``M`` and primary-key type ``ID``.

This satisfies the *Repository Pattern* and the *Open/Closed Principle* –
you can extend behaviour in subclasses without modifying this base.
"""

from __future__ import annotations

from typing import Any, Generic, List, Optional, Sequence, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import Base

M = TypeVar("M", bound=Base)
ID = TypeVar("ID", int, str)


class BaseRepository(Generic[M, ID]):
    """Async CRUD repository.

    Usage::

        class UserRepository(BaseRepository[User, int]):
            model = User
    """

    model: Type[M]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    # ------------------------------------------------------------------ #
    # Read
    # ------------------------------------------------------------------ #
    async def get_by_id(self, entity_id: ID) -> Optional[M]:
        """Return the entity with the given primary key, or ``None``."""
        return await self._session.get(self.model, entity_id)

    async def get_all(self, *, limit: int = 100, offset: int = 0) -> Sequence[M]:
        """Return a page of all entities."""
        result = await self._session.execute(
            select(self.model).limit(limit).offset(offset)
        )
        return result.scalars().all()

    async def filter_by(self, **kwargs: Any) -> Sequence[M]:
        """Return entities matching all keyword filters (equality checks)."""
        stmt = select(self.model)
        for field, value in kwargs.items():
            stmt = stmt.where(getattr(self.model, field) == value)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_one_by(self, **kwargs: Any) -> Optional[M]:
        """Return the first entity matching the filters, or ``None``."""
        stmt = select(self.model)
        for field, value in kwargs.items():
            stmt = stmt.where(getattr(self.model, field) == value)
        result = await self._session.execute(stmt)
        return result.scalars().first()

    # ------------------------------------------------------------------ #
    # Write
    # ------------------------------------------------------------------ #
    async def create(self, entity: M) -> M:
        """Persist a new entity and refresh it from the database."""
        self._session.add(entity)
        await self._session.flush()
        await self._session.refresh(entity)
        return entity

    async def update(self, entity: M, data: dict[str, Any]) -> M:
        """Apply *data* fields to *entity* and flush."""
        for field, value in data.items():
            setattr(entity, field, value)
        self._session.add(entity)
        await self._session.flush()
        await self._session.refresh(entity)
        return entity

    async def delete(self, entity: M) -> None:
        """Delete *entity* from the session."""
        await self._session.delete(entity)
        await self._session.flush()

    async def save(self, entity: M) -> M:
        """Add (or re-attach) and flush an entity; use for upsert patterns."""
        self._session.add(entity)
        await self._session.flush()
        await self._session.refresh(entity)
        return entity
