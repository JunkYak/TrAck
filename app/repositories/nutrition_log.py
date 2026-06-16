"""
app/repositories/nutrition_log.py
---------------------------------
Data-access layer for the DailyNutritionLog domain.
"""

from __future__ import annotations

from datetime import date
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.nutrition_log import (
    DailyNutritionLog,
    DailyNutritionLogEntry,
    DailyNutritionLogItem,
)
from app.repositories.base import BaseRepository


class DailyNutritionLogRepository(BaseRepository[DailyNutritionLog, str]):
    model = DailyNutritionLog

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get_by_user_and_date(self, user_id: str, log_date: date) -> Optional[DailyNutritionLog]:
        """Fetch a daily log fully loaded with entries and items."""
        stmt = (
            select(DailyNutritionLog)
            .where(
                DailyNutritionLog.user_id == user_id,
                DailyNutritionLog.date == log_date,
            )
            .options(
                selectinload(DailyNutritionLog.entries).selectinload(
                    DailyNutritionLogEntry.items
                )
            )
        )
        result = await self._session.execute(stmt)
        return result.scalars().first()


class DailyNutritionLogEntryRepository(BaseRepository[DailyNutritionLogEntry, str]):
    model = DailyNutritionLogEntry

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        
    async def get_by_id_with_log(self, entry_id: str) -> Optional[DailyNutritionLogEntry]:
        """Fetch an entry with its parent log for ownership validation."""
        stmt = (
            select(DailyNutritionLogEntry)
            .where(DailyNutritionLogEntry.id == entry_id)
            .options(
                selectinload(DailyNutritionLogEntry.log),
                selectinload(DailyNutritionLogEntry.items),
            )
        )
        result = await self._session.execute(stmt)
        return result.scalars().first()


class DailyNutritionLogItemRepository(BaseRepository[DailyNutritionLogItem, str]):
    model = DailyNutritionLogItem

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get_by_id_with_parents(self, item_id: str) -> Optional[DailyNutritionLogItem]:
        """Fetch an item with its entry and log for ownership validation."""
        stmt = (
            select(DailyNutritionLogItem)
            .where(DailyNutritionLogItem.id == item_id)
            .options(
                selectinload(DailyNutritionLogItem.entry).selectinload(
                    DailyNutritionLogEntry.log
                )
            )
        )
        result = await self._session.execute(stmt)
        return result.scalars().first()
