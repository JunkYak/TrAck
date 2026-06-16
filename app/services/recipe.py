"""
app/services/recipe.py
----------------------
Business logic for Recipes.
"""

from typing import Sequence

from app.core.exceptions import AuthorizationError, NotFoundError
from app.models.recipe import Recipe, RecipeIngredient
from app.repositories.food_item import FoodItemRepository
from app.repositories.recipe import RecipeRepository
from app.schemas.recipe import RecipeCreate, RecipeUpdate
from app.services.base import BaseService


class RecipeService(BaseService):
    def __init__(
        self,
        repository: RecipeRepository,
        food_repo: FoodItemRepository,
    ) -> None:
        self._repo = repository
        self._food_repo = food_repo

    async def list_by_user(self, user_id: str, limit: int = 100, offset: int = 0) -> Sequence[Recipe]:
        return await self._repo.get_by_user(user_id, limit, offset)

    async def get_recipe_for_user(self, recipe_id: str, user_id: str) -> Recipe:
        recipe = await self._repo.get_by_id_with_ingredients(recipe_id)
        if not recipe:
            raise NotFoundError("Recipe not found.")
        if recipe.user_id != user_id:
            raise AuthorizationError("You do not have permission to access this recipe.")
        return recipe

    async def create_recipe(self, user_id: str, data: RecipeCreate) -> Recipe:
        # Validate food items exist
        for ingredient in data.ingredients:
            food = await self._food_repo.get_by_id(ingredient.food_item_id)
            if not food:
                raise NotFoundError(f"Food item {ingredient.food_item_id} not found.")
            if food.user_id is not None and food.user_id != user_id:
                raise AuthorizationError(f"Cannot use private food item {ingredient.food_item_id} belonging to another user.")

        # Create recipe
        recipe = Recipe(name=data.name, user_id=user_id)
        recipe = await self._repo.create(recipe)

        # Add ingredients
        for ingredient in data.ingredients:
            recipe.ingredients.append(
                RecipeIngredient(
                    recipe_id=recipe.id,
                    food_item_id=ingredient.food_item_id,
                    quantity=ingredient.quantity,
                )
            )
        await self._repo.save(recipe)

        # Commit via repo implicitly or let flush happen
        return await self.get_recipe_for_user(recipe.id, user_id)

    async def update_recipe(self, recipe_id: str, user_id: str, data: RecipeUpdate) -> Recipe:
        recipe = await self.get_recipe_for_user(recipe_id, user_id)

        update_data = {}
        if data.name is not None:
            update_data["name"] = data.name

        if data.ingredients is not None:
            # Replace ingredients entirely
            recipe.ingredients.clear()

            # Flush DELETEs first
            await self._repo.save(recipe)

            new_ingredients = []

            for ingredient in data.ingredients:
                food = await self._food_repo.get_by_id(ingredient.food_item_id)

                if not food:
                    raise NotFoundError(
                        f"Food item {ingredient.food_item_id} not found."
                    )

                if food.user_id is not None and food.user_id != user_id:
                    raise AuthorizationError(
                        f"Cannot use private food item {ingredient.food_item_id} belonging to another user."
                    )

                new_ingredients.append(
                    RecipeIngredient(
                        recipe_id=recipe.id,
                        food_item_id=ingredient.food_item_id,
                        quantity=ingredient.quantity,
                    )
                )

            update_data["ingredients"] = new_ingredients

        await self._repo.update(recipe, update_data)
        return await self.get_recipe_for_user(recipe.id, user_id)

    async def delete_recipe(self, recipe_id: str, user_id: str) -> None:
        recipe = await self.get_recipe_for_user(recipe_id, user_id)
        await self._repo.delete(recipe)
