"""
app/schemas/measurement_session.py
----------------------------------
Pydantic schemas for the MeasurementSession domain.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pydantic import Field

from app.schemas.common import AppBaseModel


# ---------------------------------------------------------------------------
# Base
# ---------------------------------------------------------------------------
class MeasurementSessionBase(AppBaseModel):
    """Fields shared across measurement-session representations."""

    date: date
    waist_in: Optional[float] = Field(None, gt=0, description="Waist in inches.")
    bicep_in: Optional[float] = Field(None, gt=0, description="Bicep in inches.")
    quad_in: Optional[float] = Field(None, gt=0, description="Quad in inches.")


# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------
class MeasurementSessionCreate(MeasurementSessionBase):
    """Payload for creating a new weekly measurement session.

    ``user_id`` comes from the authenticated user context.
    """


# ---------------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------------
class MeasurementSessionUpdate(AppBaseModel):
    """Partial update for a measurement session."""

    date: Optional[date] = None
    waist_in: Optional[float] = Field(None, gt=0)
    bicep_in: Optional[float] = Field(None, gt=0)
    quad_in: Optional[float] = Field(None, gt=0)


# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------
class MeasurementSessionRead(MeasurementSessionBase):
    """Public-facing measurement-session representation."""

    id: str
    user_id: str
    created_at: datetime
