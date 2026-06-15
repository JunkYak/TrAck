"""
app/repositories/exercise.py
-----------------------------
Data-access layer for :class:`Exercise` entities.

Extends :class:`BaseRepository` with active/archived filters and
name-based look-ups scoped to a single user.
"""

from __future__ import annotations

from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.exercise import Exercise
from app.repositories.base import BaseRepository


class ExerciseRepository(BaseRepository[Exercise, str]):
    """Repository for :class:`Exercise` ORM entities."""

    model = Exercise

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    # ------------------------------------------------------------------ #
    # Domain-specific reads
    # ------------------------------------------------------------------ #
    async def get_by_user_and_name(
        self, user_id: str, name: str
    ) -> Optional[Exercise]:
        """Return the exercise matching the user and name, or ``None``."""
        return await self.get_one_by(user_id=user_id, name=name)

    async def get_active_by_user(
        self,
        user_id: str,
        *,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[Exercise]:
        """Return non-archived exercises for a user, ordered by name."""
        stmt = (
            select(Exercise)
            .where(Exercise.user_id == user_id, Exercise.is_archived.is_(False))
            .order_by(Exercise.name.asc())
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_archived_by_user(
        self,
        user_id: str,
        *,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[Exercise]:
        """Return archived exercises for a user, ordered by name."""
        stmt = (
            select(Exercise)
            .where(Exercise.user_id == user_id, Exercise.is_archived.is_(True))
            .order_by(Exercise.name.asc())
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def exists_by_user_and_name(
        self, user_id: str, name: str
    ) -> bool:
        """Return ``True`` if a user already has an exercise with this name."""
        return (await self.get_by_user_and_name(user_id, name)) is not None
