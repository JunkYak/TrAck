"""
app/schemas/food_item.py
------------------------
Pydantic schemas for the FoodItem domain.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import Field

from app.schemas.common import AppBaseModel


# ---------------------------------------------------------------------------
# Base
# ---------------------------------------------------------------------------
class FoodItemBase(AppBaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    unit: str = Field(..., description="Supported units: g, ml, count")
    calories_per_unit: float = Field(..., ge=0)
    protein_per_unit: float = Field(..., ge=0)


# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------
class FoodItemCreate(FoodItemBase):
    """Payload for creating a new food item (global or override)."""
    # source is injected by service (AI or MANUAL)


# ---------------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------------
class FoodItemUpdate(AppBaseModel):
    """Partial update for a food item."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    unit: Optional[str] = None
    calories_per_unit: Optional[float] = Field(None, ge=0)
    protein_per_unit: Optional[float] = Field(None, ge=0)


# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------
class FoodItemRead(FoodItemBase):
    id: str
    user_id: Optional[str] = None
    source: str
    created_at: datetime
    updated_at: Optional[datetime] = None
