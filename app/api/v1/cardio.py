"""
app/api/v1/cardio.py
--------------------
REST endpoints for the Cardio domain.
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, Query, status

from app.core.dependencies import get_cardio_session_service, get_current_user_id
from app.schemas.cardio import CardioSessionCreate, CardioSessionRead, CardioSessionUpdate
from app.services.cardio import CardioSessionService

router = APIRouter(prefix="/cardio", tags=["cardio"])


@router.post(
    "",
    response_model=CardioSessionRead,
    status_code=status.HTTP_201_CREATED,
    summary="Log a cardio session",
)
async def create_session(
    data: CardioSessionCreate,
    user_id: str = Depends(get_current_user_id),
    service: CardioSessionService = Depends(get_cardio_session_service),
) -> CardioSessionRead:
    entry = await service.create_session(user_id, data)
    return CardioSessionRead.model_validate(entry)


@router.get(
    "",
    response_model=List[CardioSessionRead],
    status_code=status.HTTP_200_OK,
    summary="List cardio sessions",
)
async def list_sessions(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    user_id: str = Depends(get_current_user_id),
    service: CardioSessionService = Depends(get_cardio_session_service),
) -> List[CardioSessionRead]:
    entries = await service.list_by_user(user_id, limit=limit, offset=offset)
    return [CardioSessionRead.model_validate(e) for e in entries]


@router.get(
    "/{session_id}",
    response_model=CardioSessionRead,
    status_code=status.HTTP_200_OK,
    summary="Get a cardio session",
)
async def get_session(
    session_id: str,
    user_id: str = Depends(get_current_user_id),
    service: CardioSessionService = Depends(get_cardio_session_service),
) -> CardioSessionRead:
    entry = await service.get_session_for_user(session_id, user_id)
    return CardioSessionRead.model_validate(entry)


@router.put(
    "/{session_id}",
    response_model=CardioSessionRead,
    status_code=status.HTTP_200_OK,
    summary="Update a cardio session",
)
async def update_session(
    session_id: str,
    data: CardioSessionUpdate,
    user_id: str = Depends(get_current_user_id),
    service: CardioSessionService = Depends(get_cardio_session_service),
) -> CardioSessionRead:
    entry = await service.update_session(session_id, user_id, data)
    return CardioSessionRead.model_validate(entry)


@router.delete(
    "/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a cardio session",
)
async def delete_session(
    session_id: str,
    user_id: str = Depends(get_current_user_id),
    service: CardioSessionService = Depends(get_cardio_session_service),
):
    await service.delete_session(session_id, user_id)
