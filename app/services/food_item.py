"""
app/services/food_item.py
-------------------------
Business logic for FoodItems.
"""

from typing import Optional, Sequence

from app.core.exceptions import AlreadyExistsError, AuthorizationError, NotFoundError
from app.models.food_item import FoodItem
from app.repositories.food_item import FoodItemRepository
from app.schemas.food_item import FoodItemCreate, FoodItemUpdate
from app.services.base import BaseService


class FoodItemService(BaseService):
    def __init__(self, food_repo: FoodItemRepository) -> None:
        self._repo = food_repo

    

    async def get_by_id(self, food_id: str) -> FoodItem:
        """Return a food item by primary key or raise :class:`NotFoundError`."""
        item = await self._repo.get_by_id(food_id)
        if item is None:
            raise NotFoundError(f"FoodItem with id '{food_id}' not found.")
        return item

    async def search_foods(self, query: str, user_id: str, limit: int = 50) -> Sequence[FoodItem]:
        """Search foods, shadowing globals with user overrides."""
        return await self._repo.search_by_name(query, user_id, limit=limit)

    async def get_food_for_user(self, food_id: str, user_id: str) -> FoodItem:
        food = await self._repo.get_by_id(food_id)
        if not food:
            raise NotFoundError("Food item not found.")
        if food.user_id is not None and food.user_id != user_id:
            raise AuthorizationError("You do not have permission to access this food item.")
        return food

    async def get_or_create_food(self, name: str, unit: str, user_id: str) -> FoodItem:
        """
        Lookup a food item. If it does not exist globally or as an override,
        delegate to an AI provider.
        """
        existing = await self._repo.get_by_name_and_unit(name, unit, user_id=user_id)
        if existing:
            return existing

        raise NotImplementedError("AI nutrition lookup is not yet implemented.")

    async def create_override(self, user_id: str, data: FoodItemCreate) -> FoodItem:
        """Create a personal food override."""
        existing = await self._repo.get_by_name_and_unit(data.name, data.unit, user_id=user_id)
        if existing and existing.user_id == user_id:
            raise AlreadyExistsError("You already have an override for this food and unit.")
            
        new_food = FoodItem(
            **data.model_dump(),
            user_id=user_id,
            source="MANUAL"
        )
        return await self._repo.create(new_food)

    async def update_override(self, item_id: str, user_id: str, data: FoodItemUpdate) -> FoodItem:
        """Update a personal override. Enforces ownership."""
        item = await self.get_by_id(item_id)
        if not item:
            raise NotFoundError("Food item not found.")
        if item.user_id != user_id:
            raise AuthorizationError("You do not have permission to modify this food item.")
            
        return await self._repo.update(item, data.model_dump(exclude_unset=True))

    async def delete_override(self, item_id: str, user_id: str) -> None:
        """Delete a personal override. Enforces ownership."""
        item = await self.get_by_id(item_id)
        if not item:
            raise NotFoundError("Food item not found.")
        if item.user_id != user_id:
            raise AuthorizationError("You do not have permission to delete this food item.")
            
        await self._repo.delete(item)
