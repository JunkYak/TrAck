"""
app/api/v1/exercises.py
-----------------------
REST endpoints for the Exercise and ExerciseLog domains.

All routes are scoped to the authenticated user via ``get_current_user_id``
and delegate business logic to :class:`ExerciseService` and
:class:`ExerciseLogService`.
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.dependencies import (
    get_current_user_id,
    get_exercise_log_service,
    get_exercise_service,
)
from app.schemas.exercise import ExerciseCreate, ExerciseRead, ExerciseUpdate
from app.schemas.exercise_log import (
    ExerciseLogCreate,
    ExerciseLogRead,
    ExerciseLogUpdate,
)
from app.services.exercise import ExerciseService
from app.services.exercise_log import ExerciseLogService

router = APIRouter(prefix="/exercises", tags=["exercises"])


# =========================================================================== #
# Exercise Catalog
# =========================================================================== #

@router.post(
    "",
    response_model=ExerciseRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new exercise",
    description="Create a new user-defined exercise. Name must be unique for the user.",
)
async def create_exercise(
    data: ExerciseCreate,
    user_id: str = Depends(get_current_user_id),
    service: ExerciseService = Depends(get_exercise_service),
) -> ExerciseRead:
    entry = await service.create_exercise(user_id, data)
    return ExerciseRead.model_validate(entry)


@router.get(
    "",
    response_model=List[ExerciseRead],
    status_code=status.HTTP_200_OK,
    summary="List exercises",
    description="Return paginated exercises for the authenticated user, ordered by name. By default, returns only active exercises.",
)
async def list_exercises(
    archived: bool = Query(False, description="Set to true to retrieve archived exercises instead of active ones."),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    user_id: str = Depends(get_current_user_id),
    service: ExerciseService = Depends(get_exercise_service),
) -> List[ExerciseRead]:
    if archived:
        entries = await service.list_archived_by_user(user_id, limit=limit, offset=offset)
    else:
        entries = await service.list_active_by_user(user_id, limit=limit, offset=offset)
    return [ExerciseRead.model_validate(e) for e in entries]


@router.put(
    "/{exercise_id}",
    response_model=ExerciseRead,
    status_code=status.HTTP_200_OK,
    summary="Update an exercise",
    description="Rename an exercise. The new name must not collide with existing exercises.",
)
async def update_exercise(
    exercise_id: str,
    data: ExerciseUpdate,
    user_id: str = Depends(get_current_user_id),
    service: ExerciseService = Depends(get_exercise_service),
) -> ExerciseRead:
    entry = await service.get_by_id(exercise_id)
    if entry.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this exercise.",
        )
    updated = await service.update_exercise(exercise_id, data)
    return ExerciseRead.model_validate(updated)


@router.post(
    "/{exercise_id}/archive",
    response_model=ExerciseRead,
    status_code=status.HTTP_200_OK,
    summary="Archive an exercise",
    description="Soft-delete an exercise. Historical logs are preserved.",
)
async def archive_exercise(
    exercise_id: str,
    user_id: str = Depends(get_current_user_id),
    service: ExerciseService = Depends(get_exercise_service),
) -> ExerciseRead:
    entry = await service.get_by_id(exercise_id)
    if entry.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to archive this exercise.",
        )
    archived = await service.archive_exercise(exercise_id)
    return ExerciseRead.model_validate(archived)


@router.post(
    "/{exercise_id}/restore",
    response_model=ExerciseRead,
    status_code=status.HTTP_200_OK,
    summary="Restore an exercise",
    description="Restore a previously archived exercise.",
)
async def restore_exercise(
    exercise_id: str,
    user_id: str = Depends(get_current_user_id),
    service: ExerciseService = Depends(get_exercise_service),
) -> ExerciseRead:
    entry = await service.get_by_id(exercise_id)
    if entry.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to restore this exercise.",
        )
    restored = await service.restore_exercise(exercise_id)
    return ExerciseRead.model_validate(restored)


# =========================================================================== #
# Exercise Logs
# =========================================================================== #

@router.post(
    "/{exercise_id}/logs",
    response_model=ExerciseLogRead,
    status_code=status.HTTP_201_CREATED,
    summary="Log best set",
    description="Record the best set for an exercise. If a log already exists for the given date, it is updated (upsert semantics).",
)
async def create_exercise_log(
    exercise_id: str,
    data: ExerciseLogCreate,
    user_id: str = Depends(get_current_user_id),
    service: ExerciseLogService = Depends(get_exercise_log_service),
) -> ExerciseLogRead:
    entry = await service.log_best_set(user_id, exercise_id, data)
    return ExerciseLogRead.model_validate(entry)


@router.get(
    "/{exercise_id}/logs",
    response_model=List[ExerciseLogRead],
    status_code=status.HTTP_200_OK,
    summary="List exercise logs",
    description="Return paginated log entries for a specific exercise, newest first.",
)
async def list_exercise_logs(
    exercise_id: str,
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    user_id: str = Depends(get_current_user_id),
    service: ExerciseLogService = Depends(get_exercise_log_service),
    exercise_service: ExerciseService = Depends(get_exercise_service),
) -> List[ExerciseLogRead]:
    # Ensure exercise belongs to user
    entry = await exercise_service.get_by_id(exercise_id)
    if entry.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view logs for this exercise.",
        )
    entries = await service.list_by_exercise(exercise_id, limit=limit, offset=offset)
    return [ExerciseLogRead.model_validate(e) for e in entries]


@router.get(
    "/logs/latest",
    response_model=List[ExerciseLogRead],
    status_code=status.HTTP_200_OK,
    summary="Get latest logs across all exercises",
    description="Return the most recent log entry for each of the authenticated user's exercises.",
)
async def get_latest_exercise_logs(
    user_id: str = Depends(get_current_user_id),
    service: ExerciseLogService = Depends(get_exercise_log_service),
) -> List[ExerciseLogRead]:
    entries = await service.get_latest_logs(user_id)
    return [ExerciseLogRead.model_validate(e) for e in entries]


@router.put(
    "/logs/{log_id}",
    response_model=ExerciseLogRead,
    status_code=status.HTTP_200_OK,
    summary="Update a log entry",
    description="Partially update an existing exercise log.",
)
async def update_exercise_log(
    log_id: str,
    data: ExerciseLogUpdate,
    user_id: str = Depends(get_current_user_id),
    service: ExerciseLogService = Depends(get_exercise_log_service),
) -> ExerciseLogRead:
    entry = await service.get_by_id(log_id)
    if entry.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this log entry.",
        )
    updated = await service.update_log(log_id, data)
    return ExerciseLogRead.model_validate(updated)


@router.delete(
    "/logs/{log_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a log entry",
    description="Delete an existing exercise log entry by ID.",
)
async def delete_exercise_log(
    log_id: str,
    user_id: str = Depends(get_current_user_id),
    service: ExerciseLogService = Depends(get_exercise_log_service),
):
    entry = await service.get_by_id(log_id)
    if entry.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this log entry.",
        )
    await service.delete_log(log_id)
