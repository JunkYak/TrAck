"""
app/repositories/recipe.py
--------------------------
Data-access layer for :class:`Recipe` entities.
"""

from __future__ import annotations

from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.recipe import Recipe
from app.repositories.base import BaseRepository


class RecipeRepository(BaseRepository[Recipe, str]):
    model = Recipe

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get_by_id_with_ingredients(self, recipe_id: str) -> Optional[Recipe]:
        """Fetch a recipe fully eagerly-loaded with ingredients and food items."""
        stmt = (
            select(Recipe)
            .where(Recipe.id == recipe_id)
            .options(
                selectinload(Recipe.ingredients).selectinload(
                    getattr(Recipe.ingredients.property.mapper.class_, "food_item")
                )
            )
        )
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def get_by_user(self, user_id: str, limit: int = 100, offset: int = 0) -> Sequence[Recipe]:
        """Fetch paginated recipes for a user, fully loaded."""
        stmt = (
            select(Recipe)
            .where(Recipe.user_id == user_id)
            .options(
                selectinload(Recipe.ingredients).selectinload(
                    getattr(Recipe.ingredients.property.mapper.class_, "food_item")
                )
            )
            .order_by(Recipe.name.asc())
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()
