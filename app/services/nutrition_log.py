"""
app/services/nutrition_log.py
-----------------------------
Business logic for DailyNutritionLogs.

Responsible for flattening Recipes and MealTemplates into immutable snapshots.
"""

from datetime import date

from app.core.exceptions import AuthorizationError, NotFoundError
from app.models.nutrition_log import (
    DailyNutritionLog,
    DailyNutritionLogEntry,
    DailyNutritionLogItem,
)
from app.repositories.food_item import FoodItemRepository
from app.repositories.nutrition_log import (
    DailyNutritionLogEntryRepository,
    DailyNutritionLogItemRepository,
    DailyNutritionLogRepository,
)
from app.schemas.nutrition_log import (
    DailyNutritionLogEntryCreate,
    DailyNutritionLogItemUpdate,
)
from app.services.base import BaseService


class DailyNutritionLogService(BaseService):
    def __init__(
        self,
        repository: DailyNutritionLogRepository,
        entry_repo: DailyNutritionLogEntryRepository,
        item_repo: DailyNutritionLogItemRepository,
        food_repo: FoodItemRepository,
    ) -> None:
        self._repo = repository
        self._entry_repo = entry_repo
        self._item_repo = item_repo
        self._food_repo = food_repo

    async def get_recent_history(self, user_id: str, limit: int = 7) -> list[dict]:
        """Fetch server-aggregated macros for recent logs."""
        return await self._repo.get_recent_history(user_id, limit)


    async def get_or_create_daily_log(self, user_id: str, log_date: date) -> DailyNutritionLog:
        """Upsert pattern for daily container."""
        log = await self._repo.get_by_user_and_date(user_id, log_date)
        if not log:
            log = DailyNutritionLog(user_id=user_id, date=log_date)
            log = await self._repo.create(log)
        return log

    async def add_custom_entry(
        self, user_id: str, log_date: date, data: DailyNutritionLogEntryCreate
    ) -> DailyNutritionLogEntry:
        """
        Log a pre-flattened entry (used when the UI resolves a template/recipe 
        and allows the user to edit quantities before saving).
        """
        log = await self.get_or_create_daily_log(user_id, log_date)

        entry = DailyNutritionLogEntry(
            log_id=log.id,
            entry_name=data.entry_name,
            entry_type=data.entry_type,
        )
        entry = await self._entry_repo.create(entry)

        for item_in in data.items:
            item = DailyNutritionLogItem(
                entry_id=entry.id,
                food_name=item_in.food_name,
                quantity=item_in.quantity,
                unit=item_in.unit,
                calories=item_in.calories,
                protein=item_in.protein,
            )
            await self._item_repo.create(item)

        return await self._entry_repo.get_by_id_with_log(entry.id)  # type: ignore

    async def delete_entry(self, entry_id: str, user_id: str) -> None:
        """Delete an entire entry (e.g., Breakfast Shake) securely."""
        entry = await self._entry_repo.get_by_id_with_log(entry_id)
        if not entry:
            raise NotFoundError("Entry not found.")
        if entry.log.user_id != user_id:
            raise AuthorizationError("You do not have permission to delete this entry.")
        await self._entry_repo.delete(entry)

    async def update_item(self, item_id: str, user_id: str, data: DailyNutritionLogItemUpdate) -> DailyNutritionLogItem:
        """Manually update an immutable snapshot's quantities."""
        item = await self._item_repo.get_by_id_with_parents(item_id)
        if not item:
            raise NotFoundError("Item not found.")
        if item.entry.log.user_id != user_id:
            raise AuthorizationError("You do not have permission to modify this item.")

        update_data = data.model_dump(exclude_unset=True)
        return await self._item_repo.update(item, update_data)

    async def delete_item(self, item_id: str, user_id: str) -> None:
        """Remove a specific ingredient from an entry and clean up empty entries."""
        item = await self._item_repo.get_by_id_with_parents(item_id)
        if not item:
            raise NotFoundError("Item not found.")
        if item.entry.log.user_id != user_id:
            raise AuthorizationError("You do not have permission to delete this item.")
            
        entry = item.entry
        await self._item_repo.delete(item)
        
        remaining_items = await self._item_repo.filter_by(entry_id=entry.id)
        if not remaining_items:
            await self._entry_repo.delete(entry)
