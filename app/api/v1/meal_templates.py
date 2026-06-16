"""
app/api/v1/meal_templates.py
----------------------------
REST endpoints for the MealTemplate domain.

All routes are scoped to the authenticated user via ``get_current_user_id``
and delegate business logic to :class:`MealTemplateService`.
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, Query, status

from app.core.dependencies import get_current_user_id, get_meal_template_service
from app.schemas.meal_template import MealTemplateCreate, MealTemplateRead, MealTemplateUpdate
from app.services.meal_template import MealTemplateService

router = APIRouter(prefix="/meal-templates", tags=["meal-templates"])


# ---------------------------------------------------------------------------
# POST /api/v1/meal-templates
# ---------------------------------------------------------------------------
@router.post(
    "",
    response_model=MealTemplateRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new meal template",
    description="Create a new user-scoped meal template containing food items and recipes.",
)
async def create_template(
    data: MealTemplateCreate,
    user_id: str = Depends(get_current_user_id),
    service: MealTemplateService = Depends(get_meal_template_service),
) -> MealTemplateRead:
    entry = await service.create_template(user_id, data)
    return MealTemplateRead.model_validate(entry)


# ---------------------------------------------------------------------------
# GET /api/v1/meal-templates
# ---------------------------------------------------------------------------
@router.get(
    "",
    response_model=List[MealTemplateRead],
    status_code=status.HTTP_200_OK,
    summary="List meal templates",
    description="Return paginated meal templates for the authenticated user, ordered by name.",
)
async def list_templates(
    limit: int = Query(100, ge=1, le=500, description="Max results to return."),
    offset: int = Query(0, ge=0, description="Number of results to skip."),
    user_id: str = Depends(get_current_user_id),
    service: MealTemplateService = Depends(get_meal_template_service),
) -> List[MealTemplateRead]:
    entries = await service.list_by_user(user_id, limit=limit, offset=offset)
    return [MealTemplateRead.model_validate(e) for e in entries]


# ---------------------------------------------------------------------------
# GET /api/v1/meal-templates/{template_id}
# ---------------------------------------------------------------------------
@router.get(
    "/{template_id}",
    response_model=MealTemplateRead,
    status_code=status.HTTP_200_OK,
    summary="Get a meal template",
    description="Return a single meal template by ID.",
)
async def get_template(
    template_id: str,
    user_id: str = Depends(get_current_user_id),
    service: MealTemplateService = Depends(get_meal_template_service),
) -> MealTemplateRead:
    entry = await service.get_template_for_user(template_id, user_id)
    return MealTemplateRead.model_validate(entry)


# ---------------------------------------------------------------------------
# PUT /api/v1/meal-templates/{template_id}
# ---------------------------------------------------------------------------
@router.put(
    "/{template_id}",
    response_model=MealTemplateRead,
    status_code=status.HTTP_200_OK,
    summary="Update a meal template",
    description="Partially update an existing meal template by ID. Foods and recipes lists are fully replaced if provided.",
)
async def update_template(
    template_id: str,
    data: MealTemplateUpdate,
    user_id: str = Depends(get_current_user_id),
    service: MealTemplateService = Depends(get_meal_template_service),
) -> MealTemplateRead:
    entry = await service.update_template(template_id, user_id, data)
    return MealTemplateRead.model_validate(entry)


# ---------------------------------------------------------------------------
# DELETE /api/v1/meal-templates/{template_id}
# ---------------------------------------------------------------------------
@router.delete(
    "/{template_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a meal template",
    description="Delete an existing meal template by ID.",
)
async def delete_template(
    template_id: str,
    user_id: str = Depends(get_current_user_id),
    service: MealTemplateService = Depends(get_meal_template_service),
):
    await service.delete_template(template_id, user_id)
