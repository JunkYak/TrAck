"""
app/schemas/nutrition_log.py
----------------------------
Pydantic schemas for the DailyNutritionLog domain.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional

from pydantic import Field

from app.schemas.common import AppBaseModel


# ---------------------------------------------------------------------------
# Log Item
# ---------------------------------------------------------------------------
class DailyNutritionLogItemBase(AppBaseModel):
    food_name: str
    quantity: float = Field(..., gt=0)
    unit: str
    calories: float = Field(..., ge=0)
    protein: float = Field(..., ge=0)


class DailyNutritionLogItemCreate(DailyNutritionLogItemBase):
    pass


class DailyNutritionLogItemUpdate(AppBaseModel):
    quantity: Optional[float] = Field(None, gt=0)
    calories: Optional[float] = Field(None, ge=0)
    protein: Optional[float] = Field(None, ge=0)


class DailyNutritionLogItemRead(DailyNutritionLogItemBase):
    id: str
    entry_id: str
    created_at: datetime


# ---------------------------------------------------------------------------
# Log Entry
# ---------------------------------------------------------------------------
class DailyNutritionLogEntryBase(AppBaseModel):
    entry_name: str
    entry_type: str = Field(..., description="FOOD, RECIPE, TEMPLATE, CUSTOM")


class DailyNutritionLogEntryCreate(DailyNutritionLogEntryBase):
    items: List[DailyNutritionLogItemCreate] = Field(..., min_length=1)


class DailyNutritionLogEntryRead(DailyNutritionLogEntryBase):
    id: str
    log_id: str
    items: List[DailyNutritionLogItemRead]
    created_at: datetime


# ---------------------------------------------------------------------------
# Log Container
# ---------------------------------------------------------------------------
class DailyNutritionLogRead(AppBaseModel):
    id: str
    user_id: str
    date: date
    entries: List[DailyNutritionLogEntryRead]
    created_at: datetime
    updated_at: Optional[datetime] = None
