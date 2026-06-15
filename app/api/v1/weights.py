"""
app/api/v1/weights.py
---------------------
REST endpoints for the WeightLog domain.

All routes are scoped to the authenticated user via ``get_current_user_id``
and delegate business logic to :class:`WeightLogService`.
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, Query, status

from app.core.dependencies import get_current_user_id, get_weight_log_service
from app.schemas.weight_log import WeightLogCreate, WeightLogRead, WeightLogUpdate
from app.services.weight_log import WeightLogService

router = APIRouter(prefix="/weights", tags=["weights"])


# ---------------------------------------------------------------------------
# POST /api/v1/weights
# ---------------------------------------------------------------------------
@router.post(
    "",
    response_model=WeightLogRead,
    status_code=status.HTTP_201_CREATED,
    summary="Log today's weight",
    description=(
        "Create a new weight entry for the authenticated user. "
        "If an entry already exists for the given date it will be updated "
        "(upsert semantics)."
    ),
)
async def create_weight(
    data: WeightLogCreate,
    user_id: str = Depends(get_current_user_id),
    service: WeightLogService = Depends(get_weight_log_service),
) -> WeightLogRead:
    entry = await service.log_weight(user_id, data)
    return WeightLogRead.model_validate(entry)


# ---------------------------------------------------------------------------
# GET /api/v1/weights
# ---------------------------------------------------------------------------
@router.get(
    "",
    response_model=List[WeightLogRead],
    status_code=status.HTTP_200_OK,
    summary="List weight entries",
    description="Return paginated weight entries for the authenticated user, newest first.",
)
async def list_weights(
    limit: int = Query(100, ge=1, le=500, description="Max entries to return."),
    offset: int = Query(0, ge=0, description="Number of entries to skip."),
    user_id: str = Depends(get_current_user_id),
    service: WeightLogService = Depends(get_weight_log_service),
) -> List[WeightLogRead]:
    entries = await service.list_by_user(user_id, limit=limit, offset=offset)
    return [WeightLogRead.model_validate(e) for e in entries]


# ---------------------------------------------------------------------------
# GET /api/v1/weights/latest
# ---------------------------------------------------------------------------
@router.get(
    "/latest",
    response_model=WeightLogRead,
    status_code=status.HTTP_200_OK,
    summary="Get latest weight entry",
    description="Return the most recent weight entry for the authenticated user.",
)
async def get_latest_weight(
    user_id: str = Depends(get_current_user_id),
    service: WeightLogService = Depends(get_weight_log_service),
) -> WeightLogRead:
    entries = await service.list_by_user(user_id, limit=1, offset=0)
    if not entries:
        from app.core.exceptions import NotFoundError

        raise NotFoundError("No weight entries found.")
    return WeightLogRead.model_validate(entries[0])


# ---------------------------------------------------------------------------
# PUT /api/v1/weights/{weight_id}
# ---------------------------------------------------------------------------
@router.put(
    "/{weight_id}",
    response_model=WeightLogRead,
    status_code=status.HTTP_200_OK,
    summary="Update a weight entry",
    description="Partially update an existing weight entry by ID.",
)
async def update_weight(
    weight_id: str,
    data: WeightLogUpdate,
    user_id: str = Depends(get_current_user_id),
    service: WeightLogService = Depends(get_weight_log_service),
) -> WeightLogRead:
    # Fetch first to verify the entry belongs to the authenticated user.
    entry = await service.get_by_id(weight_id)
    if entry.user_id != user_id:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this entry.",
        )
    updated = await service.update_entry(weight_id, data)
    return WeightLogRead.model_validate(updated)


# ---------------------------------------------------------------------------
# DELETE /api/v1/weights/{weight_id}
# ---------------------------------------------------------------------------
@router.delete(
    "/{weight_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a weight entry",
    description="Delete an existing weight entry by ID.",
)
async def delete_weight(
    weight_id: str,
    user_id: str = Depends(get_current_user_id),
    service: WeightLogService = Depends(get_weight_log_service),
):
    # Verify ownership before deleting.
    entry = await service.get_by_id(weight_id)
    if entry.user_id != user_id:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this entry.",
        )
    await service.delete_entry(weight_id)
