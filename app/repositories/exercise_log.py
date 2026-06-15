"""
app/repositories/exercise_log.py
--------------------------------
Data-access layer for :class:`ExerciseLog` entities.

Extends :class:`BaseRepository` with per-user, per-exercise, and
date-based queries for weekly best-set tracking.
"""

from __future__ import annotations

from datetime import date
from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.exercise_log import ExerciseLog
from app.repositories.base import BaseRepository


class ExerciseLogRepository(BaseRepository[ExerciseLog, str]):
    """Repository for :class:`ExerciseLog` ORM entities."""

    model = ExerciseLog

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    # ------------------------------------------------------------------ #
    # Domain-specific reads
    # ------------------------------------------------------------------ #
    async def get_by_user_exercise_and_date(
        self, user_id: str, exercise_id: str, log_date: date
    ) -> Optional[ExerciseLog]:
        """Return the log for a specific user + exercise + date, or ``None``."""
        return await self.get_one_by(
            user_id=user_id, exercise_id=exercise_id, log_date=log_date
        )

    async def get_by_exercise(
        self,
        exercise_id: str,
        *,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[ExerciseLog]:
        """Return logs for an exercise ordered by date descending."""
        stmt = (
            select(ExerciseLog)
            .where(ExerciseLog.exercise_id == exercise_id)
            .order_by(ExerciseLog.log_date.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_by_user(
        self,
        user_id: str,
        *,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[ExerciseLog]:
        """Return all logs for a user ordered by date descending."""
        stmt = (
            select(ExerciseLog)
            .where(ExerciseLog.user_id == user_id)
            .order_by(ExerciseLog.log_date.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_latest_per_exercise(
        self, user_id: str
    ) -> Sequence[ExerciseLog]:
        """Return the most recent log entry for each exercise of a user.

        Uses a correlated subquery to pick the latest ``log_date`` per
        ``exercise_id``.
        """
        from sqlalchemy import func

        latest_date = (
            select(func.max(ExerciseLog.log_date))
            .where(
                ExerciseLog.user_id == user_id,
                ExerciseLog.exercise_id == ExerciseLog.exercise_id,
            )
            .correlate(ExerciseLog)
            .scalar_subquery()
        )
        # Simpler approach: fetch recent logs and deduplicate in Python.
        # This avoids complex correlated subqueries on SQLite.
        stmt = (
            select(ExerciseLog)
            .where(ExerciseLog.user_id == user_id)
            .order_by(ExerciseLog.log_date.desc())
        )
        result = await self._session.execute(stmt)
        all_logs = result.scalars().all()

        seen_exercises: set[str] = set()
        latest: list[ExerciseLog] = []
        for log in all_logs:
            if log.exercise_id not in seen_exercises:
                seen_exercises.add(log.exercise_id)
                latest.append(log)
        return latest

    async def get_by_user_date_range(
        self,
        user_id: str,
        start_date: date,
        end_date: date,
    ) -> Sequence[ExerciseLog]:
        """Return logs for a user within a date range (inclusive)."""
        stmt = (
            select(ExerciseLog)
            .where(
                ExerciseLog.user_id == user_id,
                ExerciseLog.log_date >= start_date,
                ExerciseLog.log_date <= end_date,
            )
            .order_by(ExerciseLog.log_date.asc())
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()
