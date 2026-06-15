"""
app/schemas/exercise.py
-----------------------
Pydantic schemas for the Exercise domain.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import Field

from app.schemas.common import AppBaseModel


# ---------------------------------------------------------------------------
# Base
# ---------------------------------------------------------------------------
class ExerciseBase(AppBaseModel):
    """Fields shared across exercise representations."""

    name: str = Field(..., min_length=1, max_length=255)


# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------
class ExerciseCreate(ExerciseBase):
    """Payload for creating a new user-defined exercise."""


# ---------------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------------
class ExerciseUpdate(AppBaseModel):
    """Partial update for an exercise (rename)."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)


# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------
class ExerciseRead(ExerciseBase):
    """Public-facing exercise representation."""

    id: str
    user_id: str
    is_archived: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
