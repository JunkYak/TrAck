"""
app/services/meal_template.py
-----------------------------
Business logic for MealTemplates.
"""

from typing import Sequence

from app.core.exceptions import AuthorizationError, NotFoundError
from app.models.meal_template import MealTemplate, MealTemplateFood, MealTemplateRecipe
from app.repositories.food_item import FoodItemRepository
from app.repositories.meal_template import MealTemplateRepository
from app.repositories.recipe import RecipeRepository
from app.schemas.meal_template import MealTemplateCreate, MealTemplateUpdate
from app.services.base import BaseService


class MealTemplateService(BaseService):
    def __init__(
        self,
        repository: MealTemplateRepository,
        food_repo: FoodItemRepository,
        recipe_repo: RecipeRepository,
    ) -> None:
        self._repo = repository
        self._food_repo = food_repo
        self._recipe_repo = recipe_repo


    async def list_by_user(self, user_id: str, limit: int = 100, offset: int = 0) -> Sequence[MealTemplate]:
        return await self._repo.get_by_user(user_id, limit, offset)

    async def get_template_for_user(self, template_id: str, user_id: str) -> MealTemplate:
        template = await self._repo.get_by_id_fully_loaded(template_id)
        if not template:
            raise NotFoundError("MealTemplate not found.")
        if template.user_id != user_id:
            raise AuthorizationError("You do not have permission to access this template.")
        return template

    async def create_template(self, user_id: str, data: MealTemplateCreate) -> MealTemplate:
        template = MealTemplate(name=data.name, user_id=user_id)
        template = await self._repo.create(template)

        for food_in in data.foods:
            food = await self._food_repo.get_by_id(food_in.food_item_id)
            if not food:
                raise NotFoundError(f"Food item {food_in.food_item_id} not found.")
            if food.user_id is not None and food.user_id != user_id:
                raise AuthorizationError(f"Cannot use private food item {food_in.food_item_id} belonging to another user.")
            template.foods.append(
                MealTemplateFood(
                    meal_template_id=template.id,
                    food_item_id=food_in.food_item_id,
                    quantity=food_in.quantity,
                )
            )

        for recipe_in in data.recipes:
            recipe = await self._recipe_repo.get_by_id(recipe_in.recipe_id)
            if not recipe:
                raise NotFoundError(f"Recipe {recipe_in.recipe_id} not found.")
            if recipe.user_id != user_id:
                raise AuthorizationError(f"Cannot use recipe {recipe_in.recipe_id} belonging to another user.")
            
            template.recipes.append(
                MealTemplateRecipe(
                    meal_template_id=template.id,
                    recipe_id=recipe_in.recipe_id,
                    multiplier=recipe_in.multiplier,
                )
            )
        await self._repo.save(template)
        return await self.get_template_for_user(template.id, user_id)

    async def update_template(
        self,
        template_id: str,
        user_id: str,
        data: MealTemplateUpdate,
    ) -> MealTemplate:
        template = await self.get_template_for_user(template_id, user_id)
        update_data = {}

        if data.name is not None:
            update_data["name"] = data.name

        if data.foods is not None:
            template.foods.clear()

            # Flush DELETEs before rebuilding collection
            await self._repo.save(template)

            new_foods = []

            for food_in in data.foods:
                food = await self._food_repo.get_by_id(food_in.food_item_id)

                if not food:
                    raise NotFoundError(
                        f"Food item {food_in.food_item_id} not found."
                    )

                if food.user_id is not None and food.user_id != user_id:
                    raise AuthorizationError(
                        f"Cannot use private food item "
                        f"{food_in.food_item_id} belonging to another user."
                    )

                new_foods.append(
                    MealTemplateFood(
                        meal_template_id=template.id,
                        food_item_id=food_in.food_item_id,
                        quantity=food_in.quantity,
                    )
                )

            update_data["foods"] = new_foods

        if data.recipes is not None:
            new_recipes = []

            for recipe_in in data.recipes:
                recipe = await self._recipe_repo.get_by_id(recipe_in.recipe_id)

                if not recipe:
                    raise NotFoundError(
                        f"Recipe {recipe_in.recipe_id} not found."
                    )

                if recipe.user_id != user_id:
                    raise AuthorizationError(
                        f"Cannot use recipe "
                        f"{recipe_in.recipe_id} belonging to another user."
                    )

                new_recipes.append(
                    MealTemplateRecipe(
                        meal_template_id=template.id,
                        recipe_id=recipe_in.recipe_id,
                        multiplier=recipe_in.multiplier,
                    )
                )

            update_data["recipes"] = new_recipes

        await self._repo.update(template, update_data)

        return await self.get_template_for_user(
            template.id,
            user_id,
        )

    async def delete_template(self, template_id: str, user_id: str) -> None:
        template = await self.get_template_for_user(template_id, user_id)
        await self._repo.delete(template)
