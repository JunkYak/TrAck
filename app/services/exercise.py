"""
app/services/exercise.py
-------------------------
Business-logic layer for the Exercise domain.

Handles creation, updating, archiving, and restoring of exercises.
Exercises are never hard-deleted to preserve historical logs.
"""

from __future__ import annotations

from typing import Sequence

from app.core.exceptions import AlreadyExistsError, NotFoundError
from app.models.exercise import Exercise
from app.repositories.exercise import ExerciseRepository
from app.schemas.exercise import ExerciseCreate, ExerciseUpdate
from app.services.base import BaseService


class ExerciseService(BaseService):
    """High-level operations on :class:`Exercise` entities."""

    def __init__(self, exercise_repo: ExerciseRepository) -> None:
        self._repo = exercise_repo

    # ------------------------------------------------------------------ #
    # Reads
    # ------------------------------------------------------------------ #
    async def get_by_id(self, exercise_id: str) -> Exercise:
        """Return an exercise by primary key or raise :class:`NotFoundError`."""
        exercise = await self._repo.get_by_id(exercise_id)
        if exercise is None:
            raise NotFoundError(f"Exercise with id '{exercise_id}' not found.")
        return exercise

    async def list_active_by_user(
        self, user_id: str, *, limit: int = 100, offset: int = 0
    ) -> Sequence[Exercise]:
        """Return paginated non-archived exercises for a user."""
        return await self._repo.get_active_by_user(
            user_id, limit=limit, offset=offset
        )

    async def list_archived_by_user(
        self, user_id: str, *, limit: int = 100, offset: int = 0
    ) -> Sequence[Exercise]:
        """Return paginated archived exercises for a user."""
        return await self._repo.get_archived_by_user(
            user_id, limit=limit, offset=offset
        )

    # ------------------------------------------------------------------ #
    # Writes
    # ------------------------------------------------------------------ #
    async def create_exercise(
        self, user_id: str, data: ExerciseCreate
    ) -> Exercise:
        """Create a new user-defined exercise.

        Raises :class:`AlreadyExistsError` if the name is already in use
        by this user (even if archived).
        """
        if await self._repo.exists_by_user_and_name(user_id, data.name):
            raise AlreadyExistsError(
                f"An exercise named '{data.name}' already exists."
            )

        exercise = Exercise(user_id=user_id, name=data.name)
        return await self._repo.create(exercise)

    async def update_exercise(
        self, exercise_id: str, data: ExerciseUpdate
    ) -> Exercise:
        """Apply a partial update to an existing exercise (e.g., rename)."""
        exercise = await self.get_by_id(exercise_id)

        update_fields = data.model_dump(exclude_unset=True)
        if not update_fields:
            return exercise

        if "name" in update_fields and update_fields["name"] != exercise.name:
            if await self._repo.exists_by_user_and_name(
                exercise.user_id, update_fields["name"]
            ):
                raise AlreadyExistsError(
                    f"An exercise named '{update_fields['name']}' already exists."
                )

        return await self._repo.update(exercise, update_fields)

    async def archive_exercise(self, exercise_id: str) -> Exercise:
        """Soft-delete an exercise."""
        exercise = await self.get_by_id(exercise_id)
        if exercise.is_archived:
            return exercise
        return await self._repo.update(exercise, {"is_archived": True})

    async def restore_exercise(self, exercise_id: str) -> Exercise:
        """Restore an archived exercise."""
        exercise = await self.get_by_id(exercise_id)
        if not exercise.is_archived:
            return exercise
        return await self._repo.update(exercise, {"is_archived": False})
