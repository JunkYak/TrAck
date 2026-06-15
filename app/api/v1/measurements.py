"""
app/api/v1/measurements.py
--------------------------
REST endpoints for the MeasurementSession domain.

All routes are scoped to the authenticated user via ``get_current_user_id``
and delegate business logic to :class:`MeasurementSessionService`.
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, Query, status

from app.core.dependencies import (
    get_current_user_id,
    get_measurement_session_service,
)
from app.schemas.measurement_session import (
    MeasurementSessionCreate,
    MeasurementSessionRead,
    MeasurementSessionUpdate,
)
from app.services.measurement_session import MeasurementSessionService

router = APIRouter(prefix="/measurements", tags=["measurements"])


# ---------------------------------------------------------------------------
# POST /api/v1/measurements
# ---------------------------------------------------------------------------
@router.post(
    "",
    response_model=MeasurementSessionRead,
    status_code=status.HTTP_201_CREATED,
    summary="Record a measurement session",
    description=(
        "Create a new measurement session for the authenticated user. "
        "If a session already exists for the given date, the submitted "
        "values are merged into the existing record (upsert semantics)."
    ),
)
async def create_measurement(
    data: MeasurementSessionCreate,
    user_id: str = Depends(get_current_user_id),
    service: MeasurementSessionService = Depends(get_measurement_session_service),
) -> MeasurementSessionRead:
    entry = await service.record_session(user_id, data)
    return MeasurementSessionRead.model_validate(entry)


# ---------------------------------------------------------------------------
# GET /api/v1/measurements
# ---------------------------------------------------------------------------
@router.get(
    "",
    response_model=List[MeasurementSessionRead],
    status_code=status.HTTP_200_OK,
    summary="List measurement sessions",
    description="Return paginated measurement sessions for the authenticated user, newest first.",
)
async def list_measurements(
    limit: int = Query(100, ge=1, le=500, description="Max sessions to return."),
    offset: int = Query(0, ge=0, description="Number of sessions to skip."),
    user_id: str = Depends(get_current_user_id),
    service: MeasurementSessionService = Depends(get_measurement_session_service),
) -> List[MeasurementSessionRead]:
    entries = await service.list_by_user(user_id, limit=limit, offset=offset)
    return [MeasurementSessionRead.model_validate(e) for e in entries]


# ---------------------------------------------------------------------------
# GET /api/v1/measurements/latest
# ---------------------------------------------------------------------------
@router.get(
    "/latest",
    response_model=MeasurementSessionRead,
    status_code=status.HTTP_200_OK,
    summary="Get latest measurement session",
    description="Return the most recent measurement session for the authenticated user.",
)
async def get_latest_measurement(
    user_id: str = Depends(get_current_user_id),
    service: MeasurementSessionService = Depends(get_measurement_session_service),
) -> MeasurementSessionRead:
    entry = await service.get_latest(user_id)
    if entry is None:
        from app.core.exceptions import NotFoundError

        raise NotFoundError("No measurement sessions found.")
    return MeasurementSessionRead.model_validate(entry)


# ---------------------------------------------------------------------------
# PUT /api/v1/measurements/{session_id}
# ---------------------------------------------------------------------------
@router.put(
    "/{session_id}",
    response_model=MeasurementSessionRead,
    status_code=status.HTTP_200_OK,
    summary="Update a measurement session",
    description="Partially update an existing measurement session by ID.",
)
async def update_measurement(
    session_id: str,
    data: MeasurementSessionUpdate,
    user_id: str = Depends(get_current_user_id),
    service: MeasurementSessionService = Depends(get_measurement_session_service),
) -> MeasurementSessionRead:
    # Fetch first to verify the session belongs to the authenticated user.
    entry = await service.get_by_id(session_id)
    if entry.user_id != user_id:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this session.",
        )
    updated = await service.update_session(session_id, data)
    return MeasurementSessionRead.model_validate(updated)


# ---------------------------------------------------------------------------
# DELETE /api/v1/measurements/{session_id}
# ---------------------------------------------------------------------------
@router.delete(
    "/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a measurement session",
    description="Delete an existing measurement session by ID.",
)
async def delete_measurement(
    session_id: str,
    user_id: str = Depends(get_current_user_id),
    service: MeasurementSessionService = Depends(get_measurement_session_service),
):
    # Verify ownership before deleting.
    entry = await service.get_by_id(session_id)
    if entry.user_id != user_id:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this session.",
        )
    await service.delete_session(session_id)
