"""
app/schemas/weight_log.py
-------------------------
Pydantic schemas for the WeightLog domain.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pydantic import Field

from app.schemas.common import AppBaseModel


# ---------------------------------------------------------------------------
# Base
# ---------------------------------------------------------------------------
class WeightLogBase(AppBaseModel):
    """Fields shared across weight-log representations."""

    date: date
    weight_kg: float = Field(..., gt=0, description="Body weight in kilograms.")


# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------
class WeightLogCreate(WeightLogBase):
    """Payload for creating a new daily weight entry.

    ``user_id`` is not included here – it comes from the authenticated
    user context at the service / route level.
    """


# ---------------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------------
class WeightLogUpdate(AppBaseModel):
    """Partial update for a weight entry."""

    date: Optional[date] = None
    weight_kg: Optional[float] = Field(None, gt=0)


# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------
class WeightLogRead(WeightLogBase):
    """Public-facing weight-log representation."""

    id: str
    user_id: str
    created_at: datetime
