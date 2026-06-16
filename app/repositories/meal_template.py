"""
app/repositories/meal_template.py
---------------------------------
Data-access layer for :class:`MealTemplate` entities.
"""

from __future__ import annotations

from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.meal_template import MealTemplate, MealTemplateRecipe
from app.models.recipe import Recipe
from app.repositories.base import BaseRepository


class MealTemplateRepository(BaseRepository[MealTemplate, str]):
    model = MealTemplate

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get_by_id_fully_loaded(self, template_id: str) -> Optional[MealTemplate]:
        """Fetch a meal template fully loaded with its foods and recipes."""
        stmt = (
            select(MealTemplate)
            .where(MealTemplate.id == template_id)
            .options(
                selectinload(MealTemplate.foods).selectinload(
                    getattr(MealTemplate.foods.property.mapper.class_, "food_item")
                ),
                selectinload(MealTemplate.recipes)
                .selectinload(MealTemplateRecipe.recipe)
                .selectinload(Recipe.ingredients)
                .selectinload(getattr(Recipe.ingredients.property.mapper.class_, "food_item")),
            )
        )
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def get_by_user(self, user_id: str, limit: int = 100, offset: int = 0) -> Sequence[MealTemplate]:
        """Fetch paginated meal templates for a user."""
        stmt = (
            select(MealTemplate)
            .where(MealTemplate.user_id == user_id)
            .options(
                selectinload(MealTemplate.foods).selectinload(
                    getattr(MealTemplate.foods.property.mapper.class_, "food_item")
                ),
                selectinload(MealTemplate.recipes)
                .selectinload(MealTemplateRecipe.recipe)
                .selectinload(Recipe.ingredients)
                .selectinload(getattr(Recipe.ingredients.property.mapper.class_, "food_item")),
            )
            .order_by(MealTemplate.name.asc())
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()
