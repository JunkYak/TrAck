"""
app/schemas/exercise_log.py
---------------------------
Pydantic schemas for the ExerciseLog domain.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pydantic import Field

from app.schemas.common import AppBaseModel


# ---------------------------------------------------------------------------
# Base
# ---------------------------------------------------------------------------
class ExerciseLogBase(AppBaseModel):
    """Fields shared across exercise-log representations."""

    log_date: date
    weight_kg: float = Field(..., gt=0, description="Weight in kilograms.")
    reps: int = Field(..., gt=0, description="Number of repetitions.")
    notes: Optional[str] = None


# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------
class ExerciseLogCreate(ExerciseLogBase):
    """Payload for creating a new exercise log entry.

    ``user_id`` and ``exercise_id`` come from the route path and
    authenticated user context.
    """


# ---------------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------------
class ExerciseLogUpdate(AppBaseModel):
    """Partial update for an exercise log entry."""

    log_date: Optional[date] = None
    weight_kg: Optional[float] = Field(None, gt=0)
    reps: Optional[int] = Field(None, gt=0)
    notes: Optional[str] = None


# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------
class ExerciseLogRead(ExerciseLogBase):
    """Public-facing exercise-log representation."""

    id: str
    user_id: str
    exercise_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
