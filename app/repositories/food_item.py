"""
app/repositories/food_item.py
-----------------------------
Data-access layer for :class:`FoodItem` entities.

Extends :class:`BaseRepository` with global vs user override lookup logic.
"""

from __future__ import annotations

from typing import Optional, Sequence

from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.food_item import FoodItem
from app.repositories.base import BaseRepository


class FoodItemRepository(BaseRepository[FoodItem, str]):
    model = FoodItem

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get_by_name_and_unit(
        self, name: str, unit: str, user_id: Optional[str] = None
    ) -> Optional[FoodItem]:
        """Fetch a specific food by name and unit.
        
        Prioritizes the user override if user_id is provided and an
        override exists. Otherwise returns the global item.
        """
        # We can fetch both and resolve in python, or write a complex query.
        # Fetching both is safer and cleaner in SQLAlchemy 2.0.
        conditions = [FoodItem.user_id.is_(None)]
        if user_id:
            conditions.append(FoodItem.user_id == user_id)
            
        stmt = select(FoodItem).where(
            FoodItem.name == name,
            FoodItem.unit == unit,
            or_(*conditions)
        )
        
        result = await self._session.execute(stmt)
        items = result.scalars().all()
        
        if not items:
            return None
            
        # Priority 1: User override
        if user_id:
            for item in items:
                if item.user_id == user_id:
                    return item
                    
        # Priority 2: Global
        for item in items:
            if item.user_id is None:
                return item
                
        return None

    async def search_by_name(
        self, name_query: str, user_id: Optional[str] = None, limit: int = 50
    ) -> Sequence[FoodItem]:
        """Search foods by name, correctly shadowing global items with user overrides."""
        conditions = [FoodItem.user_id.is_(None)]
        if user_id:
            conditions.append(FoodItem.user_id == user_id)
            
        stmt = (
            select(FoodItem)
            .where(
                FoodItem.name.ilike(f"%{name_query}%"),
                or_(*conditions)
            )
            .limit(limit * 2) # Fetch extra to account for deduplication
        )
        
        result = await self._session.execute(stmt)
        items = result.scalars().all()
        
        # Deduplication / Shadowing logic
        # Key: (name, unit)
        deduped: dict[tuple[str, str], FoodItem] = {}
        
        for item in items:
            key = (item.name.lower(), item.unit.lower())
            existing = deduped.get(key)
            
            if not existing:
                deduped[key] = item
            elif existing.user_id is None and item.user_id == user_id:
                # Override the global one with the user's specific one
                deduped[key] = item
                
        # Sort and limit
        final_list = list(deduped.values())
        final_list.sort(key=lambda x: x.name)
        return final_list[:limit]
