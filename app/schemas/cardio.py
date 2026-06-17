"""
app/schemas/cardio.py
---------------------
Pydantic schemas for the Cardio domain.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import Field

from app.schemas.common import AppBaseModel
from app.models.cardio import RunType


class CardioSessionBase(AppBaseModel):
    run_type: RunType
    distance_km: float = Field(..., gt=0)
    duration_minutes: float = Field(..., gt=0)
    notes: Optional[str] = Field(None, max_length=500)
    performed_at: Optional[datetime] = None


class CardioSessionCreate(CardioSessionBase):
    pass


class CardioSessionUpdate(AppBaseModel):
    run_type: Optional[RunType] = None
    distance_km: Optional[float] = Field(None, gt=0)
    duration_minutes: Optional[float] = Field(None, gt=0)
    notes: Optional[str] = Field(None, max_length=500)
    performed_at: Optional[datetime] = None


class CardioSessionRead(CardioSessionBase):
    id: str
    user_id: str
    average_pace: float
    body_weight_used: float
    estimated_calories: float
    performed_at: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None
