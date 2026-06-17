"""
app/repositories/cardio.py
--------------------------
Data-access layer for CardioSession entities.
"""

from __future__ import annotations

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cardio import CardioSession
from app.repositories.base import BaseRepository


class CardioSessionRepository(BaseRepository[CardioSession, str]):
    model = CardioSession

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get_by_user(self, user_id: str, limit: int = 100, offset: int = 0) -> Sequence[CardioSession]:
        stmt = (
            select(CardioSession)
            .where(CardioSession.user_id == user_id)
            .order_by(CardioSession.performed_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()
