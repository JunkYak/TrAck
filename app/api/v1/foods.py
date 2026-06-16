"""
app/api/v1/foods.py
-------------------
REST endpoints for the FoodItem domain.

All routes are scoped to the authenticated user via ``get_current_user_id``
and delegate business logic to :class:`FoodItemService`.
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, Query, status

from app.core.dependencies import get_current_user_id, get_food_item_service
from app.schemas.food_item import FoodItemCreate, FoodItemRead, FoodItemUpdate
from app.services.food_item import FoodItemService

router = APIRouter(prefix="/foods", tags=["foods"])


# ---------------------------------------------------------------------------
# POST /api/v1/foods
# ---------------------------------------------------------------------------
@router.post(
    "",
    response_model=FoodItemRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a personal food override",
    description=(
        "Create a personal food item override for the authenticated user. "
        "The source is automatically set to MANUAL."
    ),
)
async def create_food(
    data: FoodItemCreate,
    user_id: str = Depends(get_current_user_id),
    service: FoodItemService = Depends(get_food_item_service),
) -> FoodItemRead:
    entry = await service.create_override(user_id, data)
    return FoodItemRead.model_validate(entry)


# ---------------------------------------------------------------------------
# GET /api/v1/foods/search
# ---------------------------------------------------------------------------
@router.get(
    "/search",
    response_model=List[FoodItemRead],
    status_code=status.HTTP_200_OK,
    summary="Search foods",
    description=(
        "Search food items by name. Returns both global foods and "
        "user overrides, with user overrides shadowing globals."
    ),
)
async def search_foods(
    q: str = Query(..., min_length=1, description="Search query string."),
    limit: int = Query(50, ge=1, le=200, description="Max results to return."),
    user_id: str = Depends(get_current_user_id),
    service: FoodItemService = Depends(get_food_item_service),
) -> List[FoodItemRead]:
    entries = await service.search_foods(q, user_id, limit=limit)
    return [FoodItemRead.model_validate(e) for e in entries]


# ---------------------------------------------------------------------------
# GET /api/v1/foods/{food_id}
# ---------------------------------------------------------------------------
@router.get(
    "/{food_id}",
    response_model=FoodItemRead,
    status_code=status.HTTP_200_OK,
    summary="Get a food item",
    description="Return a single food item by ID. Global foods and user-owned foods are accessible.",
)
async def get_food(
    food_id: str,
    user_id: str = Depends(get_current_user_id),
    service: FoodItemService = Depends(get_food_item_service),
) -> FoodItemRead:
    entry = await service.get_food_for_user(food_id, user_id)
    return FoodItemRead.model_validate(entry)


# ---------------------------------------------------------------------------
# PUT /api/v1/foods/{food_id}
# ---------------------------------------------------------------------------
@router.put(
    "/{food_id}",
    response_model=FoodItemRead,
    status_code=status.HTTP_200_OK,
    summary="Update a personal food override",
    description="Partially update an existing personal food override by ID.",
)
async def update_food(
    food_id: str,
    data: FoodItemUpdate,
    user_id: str = Depends(get_current_user_id),
    service: FoodItemService = Depends(get_food_item_service),
) -> FoodItemRead:
    entry = await service.update_override(food_id, user_id, data)
    return FoodItemRead.model_validate(entry)


# ---------------------------------------------------------------------------
# DELETE /api/v1/foods/{food_id}
# ---------------------------------------------------------------------------
@router.delete(
    "/{food_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a personal food override",
    description="Delete an existing personal food override by ID.",
)
async def delete_food(
    food_id: str,
    user_id: str = Depends(get_current_user_id),
    service: FoodItemService = Depends(get_food_item_service),
):
    await service.delete_override(food_id, user_id)
