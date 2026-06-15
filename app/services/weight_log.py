"""
app/services/weight_log.py
--------------------------
Business-logic layer for the WeightLog domain.

Enforces the "one entry per user per day" rule using upsert semantics:
if an entry already exists for the given date, it is updated in-place
rather than raising an error.
"""

from __future__ import annotations

from datetime import date
from typing import Sequence

from app.core.exceptions import NotFoundError
from app.models.weight_log import WeightLog
from app.repositories.weight_log import WeightLogRepository
from app.schemas.weight_log import WeightLogCreate, WeightLogUpdate
from app.services.base import BaseService


class WeightLogService(BaseService):
    """High-level operations on :class:`WeightLog` entities."""

    def __init__(self, weight_log_repo: WeightLogRepository) -> None:
        self._repo = weight_log_repo

    # ------------------------------------------------------------------ #
    # Reads
    # ------------------------------------------------------------------ #
    async def get_by_id(self, log_id: str) -> WeightLog:
        """Return a weight log by primary key or raise :class:`NotFoundError`."""
        entry = await self._repo.get_by_id(log_id)
        if entry is None:
            raise NotFoundError(f"WeightLog with id '{log_id}' not found.")
        return entry

    async def list_by_user(
        self, user_id: str, *, limit: int = 100, offset: int = 0
    ) -> Sequence[WeightLog]:
        """Return paginated weight entries for a user (newest first)."""
        return await self._repo.get_by_user(user_id, limit=limit, offset=offset)

    async def get_by_date_range(
        self, user_id: str, start_date: date, end_date: date
    ) -> Sequence[WeightLog]:
        """Return weight entries for a user between two dates (inclusive)."""
        return await self._repo.get_by_user_date_range(
            user_id, start_date, end_date
        )

    # ------------------------------------------------------------------ #
    # Writes
    # ------------------------------------------------------------------ #
    async def log_weight(self, user_id: str, data: WeightLogCreate) -> WeightLog:
        """Create or update the weight entry for a user on the given date.

        Implements upsert semantics: if an entry already exists for the
        ``(user_id, date)`` pair, the weight is updated instead of inserting
        a duplicate.
        """
        existing = await self._repo.get_by_user_and_date(user_id, data.date)
        if existing is not None:
            return await self._repo.update(
                existing, {"weight_kg": data.weight_kg}
            )

        entry = WeightLog(
            user_id=user_id,
            date=data.date,
            weight_kg=data.weight_kg,
        )
        return await self._repo.create(entry)

    async def update_entry(self, log_id: str, data: WeightLogUpdate) -> WeightLog:
        """Apply a partial update to an existing weight entry."""
        entry = await self.get_by_id(log_id)
        update_fields = data.model_dump(exclude_unset=True)
        if not update_fields:
            return entry
        return await self._repo.update(entry, update_fields)

    async def delete_entry(self, log_id: str) -> None:
        """Delete a weight entry by ID."""
        entry = await self.get_by_id(log_id)
        await self._repo.delete(entry)
