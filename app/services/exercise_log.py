"""
app/services/exercise_log.py
----------------------------
Business-logic layer for the ExerciseLog domain.

Enforces the "one best set per exercise per date" rule using upsert semantics.
Unlike the previous plan, this uses the exact log_date provided by the user,
not an ISO week calculation.
"""

from __future__ import annotations

from datetime import date
from typing import Sequence

from app.core.exceptions import NotFoundError
from app.models.exercise_log import ExerciseLog
from app.repositories.exercise_log import ExerciseLogRepository
from app.schemas.exercise_log import ExerciseLogCreate, ExerciseLogUpdate
from app.services.base import BaseService
from app.services.exercise import ExerciseService


class ExerciseLogService(BaseService):
    """High-level operations on :class:`ExerciseLog` entities."""

    def __init__(
        self,
        log_repo: ExerciseLogRepository,
        exercise_service: ExerciseService,
    ) -> None:
        self._repo = log_repo
        self._exercise_service = exercise_service

    # ------------------------------------------------------------------ #
    # Reads
    # ------------------------------------------------------------------ #
    async def get_by_id(self, log_id: str) -> ExerciseLog:
        """Return a log entry by primary key or raise :class:`NotFoundError`."""
        entry = await self._repo.get_by_id(log_id)
        if entry is None:
            raise NotFoundError(f"ExerciseLog with id '{log_id}' not found.")
        return entry

    async def list_by_exercise(
        self, exercise_id: str, *, limit: int = 100, offset: int = 0
    ) -> Sequence[ExerciseLog]:
        """Return paginated log entries for a specific exercise."""
        # Ensure the exercise exists
        await self._exercise_service.get_by_id(exercise_id)
        return await self._repo.get_by_exercise(
            exercise_id, limit=limit, offset=offset
        )

    async def get_latest_logs(self, user_id: str) -> Sequence[ExerciseLog]:
        """Return the most recent log entry for each of the user's exercises."""
        return await self._repo.get_latest_per_exercise(user_id)

    # ------------------------------------------------------------------ #
    # Writes
    # ------------------------------------------------------------------ #
    async def log_best_set(
        self, user_id: str, exercise_id: str, data: ExerciseLogCreate
    ) -> ExerciseLog:
        """Create or update the log entry for an exercise on the given date.

        Implements upsert semantics: if an entry already exists for the
        ``(user_id, exercise_id, log_date)`` combination, it is updated.
        """
        # Validate exercise exists and belongs to the user
        exercise = await self._exercise_service.get_by_id(exercise_id)
        if exercise.user_id != user_id:
            from app.core.exceptions import AuthorizationError

            raise AuthorizationError("You do not have permission for this exercise.")

        existing = await self._repo.get_by_user_exercise_and_date(
            user_id, exercise_id, data.log_date
        )
        
        if existing is not None:
            return await self._repo.update(
                existing, 
                {
                    "weight_kg": data.weight_kg,
                    "reps": data.reps,
                    "notes": data.notes,
                }
            )

        entry = ExerciseLog(
            user_id=user_id,
            exercise_id=exercise_id,
            log_date=data.log_date,
            weight_kg=data.weight_kg,
            reps=data.reps,
            notes=data.notes,
        )
        return await self._repo.create(entry)

    async def update_log(self, log_id: str, data: ExerciseLogUpdate) -> ExerciseLog:
        """Apply a partial update to an existing log entry."""
        entry = await self.get_by_id(log_id)
        update_fields = data.model_dump(exclude_unset=True)
        if not update_fields:
            return entry
        return await self._repo.update(entry, update_fields)

    async def delete_log(self, log_id: str) -> None:
        """Delete an exercise log entry by ID."""
        entry = await self.get_by_id(log_id)
        await self._repo.delete(entry)
