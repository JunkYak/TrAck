"""
app/api/v1/nutrition_logs.py
----------------------------
REST endpoints for the DailyNutritionLog domain.

All routes are scoped to the authenticated user via ``get_current_user_id``
and delegate business logic to :class:`DailyNutritionLogService`.
"""

from __future__ import annotations

import datetime

from fastapi import APIRouter, Depends, Query, status

from app.core.dependencies import get_current_user_id, get_daily_nutrition_log_service
from app.schemas.nutrition_log import (
    DailyNutritionLogEntryCreate,
    DailyNutritionLogEntryRead,
    DailyNutritionLogItemRead,
    DailyNutritionLogItemUpdate,
    DailyNutritionLogRead,
)
from app.services.nutrition_log import DailyNutritionLogService

from typing import List
from app.schemas.nutrition_log import DailyNutritionLogSummaryRead

router = APIRouter(prefix="/nutrition-logs", tags=["nutrition-logs"])


# ---------------------------------------------------------------------------
# GET /api/v1/nutrition-logs/history
# ---------------------------------------------------------------------------
@router.get(
    "/history",
    response_model=List[DailyNutritionLogSummaryRead],
    status_code=status.HTTP_200_OK,
    summary="Get recent nutrition history",
    description="Returns a lightweight list of recent nutrition logs with aggregated macros.",
)
async def get_recent_history(
    limit: int = Query(7, ge=1, le=30, description="Number of logs to retrieve"),
    user_id: str = Depends(get_current_user_id),
    service: DailyNutritionLogService = Depends(get_daily_nutrition_log_service),
) -> List[DailyNutritionLogSummaryRead]:
    # We validate the raw dicts directly to the Pydantic schema
    logs = await service.get_recent_history(user_id, limit)
    return [DailyNutritionLogSummaryRead.model_validate(log) for log in logs]

# ---------------------------------------------------------------------------
# POST /api/v1/nutrition-logs/entries
# ---------------------------------------------------------------------------
@router.post(
    "/entries",
    response_model=DailyNutritionLogEntryRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a custom log entry",
    description="Create a new custom entry with items for a specific date.",
)
async def add_custom_entry(
    data: DailyNutritionLogEntryCreate,
    log_date: datetime.date = Query(..., description="The date to log the entry for (YYYY-MM-DD)."),
    user_id: str = Depends(get_current_user_id),
    service: DailyNutritionLogService = Depends(get_daily_nutrition_log_service),
) -> DailyNutritionLogEntryRead:
    entry = await service.add_custom_entry(user_id, log_date, data)
    return DailyNutritionLogEntryRead.model_validate(entry)


# ---------------------------------------------------------------------------
# GET /api/v1/nutrition-logs/{log_date}
# ---------------------------------------------------------------------------
@router.get(
    "/{log_date}",
    response_model=DailyNutritionLogRead,
    status_code=status.HTTP_200_OK,
    summary="Get or create a daily nutrition log",
    description="Return a daily nutrition log by date. Creates an empty log if it doesn't exist.",
)
async def get_or_create_daily_log(
    log_date: datetime.date,
    user_id: str = Depends(get_current_user_id),
    service: DailyNutritionLogService = Depends(get_daily_nutrition_log_service),
) -> DailyNutritionLogRead:
    entry = await service.get_or_create_daily_log(user_id, log_date)
    return DailyNutritionLogRead.model_validate(entry)


# ---------------------------------------------------------------------------
# PUT /api/v1/nutrition-logs/items/{item_id}
# ---------------------------------------------------------------------------
@router.put(
    "/items/{item_id}",
    response_model=DailyNutritionLogItemRead,
    status_code=status.HTTP_200_OK,
    summary="Update a nutrition log item",
    description="Update the quantity or nutrition data of a specific item in a log.",
)
async def update_item(
    item_id: str,
    data: DailyNutritionLogItemUpdate,
    user_id: str = Depends(get_current_user_id),
    service: DailyNutritionLogService = Depends(get_daily_nutrition_log_service),
) -> DailyNutritionLogItemRead:
    entry = await service.update_item(item_id, user_id, data)
    return DailyNutritionLogItemRead.model_validate(entry)


# ---------------------------------------------------------------------------
# DELETE /api/v1/nutrition-logs/items/{item_id}
# ---------------------------------------------------------------------------
@router.delete(
    "/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a nutrition log item",
    description="Delete a specific item from a log entry.",
)
async def delete_item(
    item_id: str,
    user_id: str = Depends(get_current_user_id),
    service: DailyNutritionLogService = Depends(get_daily_nutrition_log_service),
):
    await service.delete_item(item_id, user_id)


# ---------------------------------------------------------------------------
# DELETE /api/v1/nutrition-logs/entries/{entry_id}
# ---------------------------------------------------------------------------
@router.delete(
    "/entries/{entry_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a nutrition log entry",
    description="Delete an entire log entry and all its items.",
)
async def delete_entry(
    entry_id: str,
    user_id: str = Depends(get_current_user_id),
    service: DailyNutritionLogService = Depends(get_daily_nutrition_log_service),
):
    await service.delete_entry(entry_id, user_id)
