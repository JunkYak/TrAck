"""
app/services/cardio.py
----------------------
Business logic for the Cardio domain.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Sequence

from app.core.exceptions import AuthorizationError, NotFoundError, ValidationError
from app.models.cardio import CardioSession
from app.repositories.cardio import CardioSessionRepository
from app.repositories.weight_log import WeightLogRepository
from app.schemas.cardio import CardioSessionCreate, CardioSessionUpdate
from app.services.base import BaseService


class CardioSessionService(BaseService):
    def __init__(
        self,
        repository: CardioSessionRepository,
        weight_repo: WeightLogRepository,
    ) -> None:
        self._repo = repository
        self._weight_repo = weight_repo

    async def get_session_for_user(self, session_id: str, user_id: str) -> CardioSession:
        entry = await self._repo.get_by_id(session_id)
        if not entry:
            raise NotFoundError("Cardio session not found.")
        if entry.user_id != user_id:
            raise AuthorizationError("You do not have permission to access this cardio session.")
        return entry

    async def list_by_user(self, user_id: str, limit: int = 100, offset: int = 0) -> Sequence[CardioSession]:
        return await self._repo.get_by_user(user_id, limit, offset)

    async def create_session(self, user_id: str, data: CardioSessionCreate) -> CardioSession:
        if data.distance_km <= 0 or data.duration_minutes <= 0:
            raise ValidationError("Distance and duration must be greater than zero.")

        # Fetch latest weight log using existing limits
        weight_logs = await self._weight_repo.get_by_user(user_id, limit=1)
        if not weight_logs:
            raise ValidationError("You must log your weight at least once before tracking cardio.")
        
        latest_weight = weight_logs[0].weight_kg

        average_pace = data.duration_minutes / data.distance_km
        estimated_calories = latest_weight * data.distance_km

        performed_at = data.performed_at or datetime.now(timezone.utc)

        session = CardioSession(
            user_id=user_id,
            run_type=data.run_type,
            distance_km=data.distance_km,
            duration_minutes=data.duration_minutes,
            average_pace=average_pace,
            body_weight_used=latest_weight,
            estimated_calories=estimated_calories,
            notes=data.notes,
            performed_at=performed_at,
        )

        return await self._repo.create(session)

    async def update_session(self, session_id: str, user_id: str, data: CardioSessionUpdate) -> CardioSession:
        if data.distance_km is not None and data.distance_km <= 0:
            raise ValidationError("Distance must be greater than zero.")
        if data.duration_minutes is not None and data.duration_minutes <= 0:
            raise ValidationError("Duration must be greater than zero.")

        session = await self.get_session_for_user(session_id, user_id)

        update_data = {}

        if data.run_type is not None:
            update_data["run_type"] = data.run_type

        if data.notes is not None:
            update_data["notes"] = data.notes

        if data.performed_at is not None:
            update_data["performed_at"] = data.performed_at

        distance_changed = data.distance_km is not None and data.distance_km != session.distance_km
        duration_changed = data.duration_minutes is not None and data.duration_minutes != session.duration_minutes

        new_distance = data.distance_km if data.distance_km is not None else session.distance_km
        new_duration = data.duration_minutes if data.duration_minutes is not None else session.duration_minutes

        if distance_changed:
            update_data["distance_km"] = new_distance
            update_data["estimated_calories"] = session.body_weight_used * new_distance

        if duration_changed:
            update_data["duration_minutes"] = new_duration

        if distance_changed or duration_changed:
            update_data["average_pace"] = new_duration / new_distance

        return await self._repo.update(session, update_data)

    async def delete_session(self, session_id: str, user_id: str) -> None:
        session = await self.get_session_for_user(session_id, user_id)
        await self._repo.delete(session)
