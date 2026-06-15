"""
app/repositories/measurement_session.py
---------------------------------------
Data-access layer for :class:`MeasurementSession` entities.

Extends :class:`BaseRepository` with per-user, date, and date-range queries.
"""

from __future__ import annotations

from datetime import date
from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.measurement_session import MeasurementSession
from app.repositories.base import BaseRepository


class MeasurementSessionRepository(BaseRepository[MeasurementSession, str]):
    """Repository for :class:`MeasurementSession` ORM entities."""

    model = MeasurementSession

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    # ------------------------------------------------------------------ #
    # Domain-specific reads
    # ------------------------------------------------------------------ #
    async def get_by_user_and_date(
        self, user_id: str, session_date: date
    ) -> Optional[MeasurementSession]:
        """Return the session for a user on a specific date, or ``None``."""
        return await self.get_one_by(user_id=user_id, date=session_date)

    async def get_by_user(
        self,
        user_id: str,
        *,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[MeasurementSession]:
        """Return measurement sessions for a user ordered by date descending."""
        stmt = (
            select(MeasurementSession)
            .where(MeasurementSession.user_id == user_id)
            .order_by(MeasurementSession.date.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_by_user_date_range(
        self,
        user_id: str,
        start_date: date,
        end_date: date,
    ) -> Sequence[MeasurementSession]:
        """Return sessions for a user within a date range (inclusive)."""
        stmt = (
            select(MeasurementSession)
            .where(
                MeasurementSession.user_id == user_id,
                MeasurementSession.date >= start_date,
                MeasurementSession.date <= end_date,
            )
            .order_by(MeasurementSession.date.asc())
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_latest_by_user(self, user_id: str) -> Optional[MeasurementSession]:
        """Return the most recent measurement session for a user."""
        stmt = (
            select(MeasurementSession)
            .where(MeasurementSession.user_id == user_id)
            .order_by(MeasurementSession.date.desc())
            .limit(1)
        )
        result = await self._session.execute(stmt)
        return result.scalars().first()
