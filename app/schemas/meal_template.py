"""
app/schemas/meal_template.py
----------------------------
Pydantic schemas for the MealTemplate domain.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import Field

from app.schemas.common import AppBaseModel
from app.schemas.food_item import FoodItemRead
from app.schemas.recipe import RecipeRead


# ---------------------------------------------------------------------------
# Items
# ---------------------------------------------------------------------------
class MealTemplateFoodCreate(AppBaseModel):
    food_item_id: str
    quantity: float = Field(..., gt=0)


class MealTemplateFoodRead(MealTemplateFoodCreate):
    id: str
    food_item: FoodItemRead


class MealTemplateRecipeCreate(AppBaseModel):
    recipe_id: str
    multiplier: float = Field(1.0, gt=0)


class MealTemplateRecipeRead(MealTemplateRecipeCreate):
    id: str
    recipe: RecipeRead


# ---------------------------------------------------------------------------
# Template
# ---------------------------------------------------------------------------
class MealTemplateBase(AppBaseModel):
    name: str = Field(..., min_length=1, max_length=255)


class MealTemplateCreate(MealTemplateBase):
    foods: List[MealTemplateFoodCreate] = Field(default_factory=list)
    recipes: List[MealTemplateRecipeCreate] = Field(default_factory=list)


class MealTemplateUpdate(AppBaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    foods: Optional[List[MealTemplateFoodCreate]] = None
    recipes: Optional[List[MealTemplateRecipeCreate]] = None


class MealTemplateRead(MealTemplateBase):
    id: str
    user_id: str
    foods: List[MealTemplateFoodRead]
    recipes: List[MealTemplateRecipeRead]
    created_at: datetime
    updated_at: Optional[datetime] = None
