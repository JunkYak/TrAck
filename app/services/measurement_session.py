"""
app/services/measurement_session.py
-----------------------------------
Business-logic layer for the MeasurementSession domain.

Enforces the "one session per user per day" rule with upsert semantics
so that re-submitting measurements for the same date merges the values.
"""

from __future__ import annotations

from datetime import date
from typing import Optional, Sequence

from app.core.exceptions import NotFoundError
from app.models.measurement_session import MeasurementSession
from app.repositories.measurement_session import MeasurementSessionRepository
from app.schemas.measurement_session import (
    MeasurementSessionCreate,
    MeasurementSessionUpdate,
)
from app.services.base import BaseService


class MeasurementSessionService(BaseService):
    """High-level operations on :class:`MeasurementSession` entities."""

    def __init__(self, measurement_repo: MeasurementSessionRepository) -> None:
        self._repo = measurement_repo

    # ------------------------------------------------------------------ #
    # Reads
    # ------------------------------------------------------------------ #
    async def get_by_id(self, session_id: str) -> MeasurementSession:
        """Return a session by primary key or raise :class:`NotFoundError`."""
        session = await self._repo.get_by_id(session_id)
        if session is None:
            raise NotFoundError(
                f"MeasurementSession with id '{session_id}' not found."
            )
        return session

    async def list_by_user(
        self, user_id: str, *, limit: int = 100, offset: int = 0
    ) -> Sequence[MeasurementSession]:
        """Return paginated sessions for a user (newest first)."""
        return await self._repo.get_by_user(user_id, limit=limit, offset=offset)

    async def get_by_date_range(
        self, user_id: str, start_date: date, end_date: date
    ) -> Sequence[MeasurementSession]:
        """Return sessions for a user between two dates (inclusive)."""
        return await self._repo.get_by_user_date_range(
            user_id, start_date, end_date
        )

    async def get_latest(self, user_id: str) -> Optional[MeasurementSession]:
        """Return the most recent session for a user, or ``None``."""
        return await self._repo.get_latest_by_user(user_id)

    # ------------------------------------------------------------------ #
    # Writes
    # ------------------------------------------------------------------ #
    async def record_session(
        self, user_id: str, data: MeasurementSessionCreate
    ) -> MeasurementSession:
        """Create or update the measurement session for a user on the given date.

        Upsert semantics: if a session already exists for the ``(user_id, date)``
        pair, the measurement values are merged (only non-``None`` fields from
        *data* overwrite existing values).
        """
        existing = await self._repo.get_by_user_and_date(user_id, data.date)
        if existing is not None:
            update_fields = data.model_dump(exclude={"date"}, exclude_none=True)
            if update_fields:
                return await self._repo.update(existing, update_fields)
            return existing

        session = MeasurementSession(
            user_id=user_id,
            date=data.date,
            waist_in=data.waist_in,
            bicep_in=data.bicep_in,
            quad_in=data.quad_in,
        )
        return await self._repo.create(session)

    async def update_session(
        self, session_id: str, data: MeasurementSessionUpdate
    ) -> MeasurementSession:
        """Apply a partial update to an existing measurement session."""
        session = await self.get_by_id(session_id)
        update_fields = data.model_dump(exclude_unset=True)
        if not update_fields:
            return session
        return await self._repo.update(session, update_fields)

    async def delete_session(self, session_id: str) -> None:
        """Delete a measurement session by ID."""
        session = await self.get_by_id(session_id)
        await self._repo.delete(session)
