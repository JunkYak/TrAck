"""
app/repositories/weight_log.py
------------------------------
Data-access layer for :class:`WeightLog` entities.

Extends :class:`BaseRepository` with date-range and per-user queries
typical for daily tracking data.
"""

from __future__ import annotations

from datetime import date
from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.weight_log import WeightLog
from app.repositories.base import BaseRepository


class WeightLogRepository(BaseRepository[WeightLog, str]):
    """Repository for :class:`WeightLog` ORM entities."""

    model = WeightLog

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    # ------------------------------------------------------------------ #
    # Domain-specific reads
    # ------------------------------------------------------------------ #
    async def get_by_user_and_date(
        self, user_id: str, log_date: date
    ) -> Optional[WeightLog]:
        """Return the weight entry for a user on a specific date, or ``None``."""
        return await self.get_one_by(user_id=user_id, date=log_date)

    async def get_by_user(
        self,
        user_id: str,
        *,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[WeightLog]:
        """Return weight entries for a user ordered by date descending."""
        stmt = (
            select(WeightLog)
            .where(WeightLog.user_id == user_id)
            .order_by(WeightLog.date.desc())
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
    ) -> Sequence[WeightLog]:
        """Return weight entries for a user within a date range (inclusive)."""
        stmt = (
            select(WeightLog)
            .where(
                WeightLog.user_id == user_id,
                WeightLog.date >= start_date,
                WeightLog.date <= end_date,
            )
            .order_by(WeightLog.date.asc())
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()
