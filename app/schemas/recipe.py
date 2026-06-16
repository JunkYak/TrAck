"""
app/schemas/recipe.py
---------------------
Pydantic schemas for the Recipe domain.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import Field

from app.schemas.common import AppBaseModel
from app.schemas.food_item import FoodItemRead


# ---------------------------------------------------------------------------
# Recipe Ingredient
# ---------------------------------------------------------------------------
class RecipeIngredientBase(AppBaseModel):
    food_item_id: str
    quantity: float = Field(..., gt=0)


class RecipeIngredientCreate(RecipeIngredientBase):
    pass


class RecipeIngredientRead(RecipeIngredientBase):
    id: str
    food_item: FoodItemRead


# ---------------------------------------------------------------------------
# Recipe
# ---------------------------------------------------------------------------
class RecipeBase(AppBaseModel):
    name: str = Field(..., min_length=1, max_length=255)


class RecipeCreate(RecipeBase):
    ingredients: List[RecipeIngredientCreate] = Field(..., min_length=1)


class RecipeUpdate(AppBaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    ingredients: Optional[List[RecipeIngredientCreate]] = None


class RecipeRead(RecipeBase):
    id: str
    user_id: str
    ingredients: List[RecipeIngredientRead]
    created_at: datetime
    updated_at: Optional[datetime] = None
