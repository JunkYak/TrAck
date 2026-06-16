"""
app/api/v1/recipes.py
---------------------
REST endpoints for the Recipe domain.

All routes are scoped to the authenticated user via ``get_current_user_id``
and delegate business logic to :class:`RecipeService`.
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, Query, status

from app.core.dependencies import get_current_user_id, get_recipe_service
from app.schemas.recipe import RecipeCreate, RecipeRead, RecipeUpdate
from app.services.recipe import RecipeService

router = APIRouter(prefix="/recipes", tags=["recipes"])


# ---------------------------------------------------------------------------
# POST /api/v1/recipes
# ---------------------------------------------------------------------------
@router.post(
    "",
    response_model=RecipeRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new recipe",
    description="Create a new user-scoped recipe containing food items.",
)
async def create_recipe(
    data: RecipeCreate,
    user_id: str = Depends(get_current_user_id),
    service: RecipeService = Depends(get_recipe_service),
) -> RecipeRead:
    entry = await service.create_recipe(user_id, data)
    return RecipeRead.model_validate(entry)


# ---------------------------------------------------------------------------
# GET /api/v1/recipes
# ---------------------------------------------------------------------------
@router.get(
    "",
    response_model=List[RecipeRead],
    status_code=status.HTTP_200_OK,
    summary="List recipes",
    description="Return paginated recipes for the authenticated user, ordered by name.",
)
async def list_recipes(
    limit: int = Query(100, ge=1, le=500, description="Max results to return."),
    offset: int = Query(0, ge=0, description="Number of results to skip."),
    user_id: str = Depends(get_current_user_id),
    service: RecipeService = Depends(get_recipe_service),
) -> List[RecipeRead]:
    entries = await service.list_by_user(user_id, limit=limit, offset=offset)
    return [RecipeRead.model_validate(e) for e in entries]


# ---------------------------------------------------------------------------
# GET /api/v1/recipes/{recipe_id}
# ---------------------------------------------------------------------------
@router.get(
    "/{recipe_id}",
    response_model=RecipeRead,
    status_code=status.HTTP_200_OK,
    summary="Get a recipe",
    description="Return a single recipe by ID.",
)
async def get_recipe(
    recipe_id: str,
    user_id: str = Depends(get_current_user_id),
    service: RecipeService = Depends(get_recipe_service),
) -> RecipeRead:
    entry = await service.get_recipe_for_user(recipe_id, user_id)
    return RecipeRead.model_validate(entry)


# ---------------------------------------------------------------------------
# PUT /api/v1/recipes/{recipe_id}
# ---------------------------------------------------------------------------
@router.put(
    "/{recipe_id}",
    response_model=RecipeRead,
    status_code=status.HTTP_200_OK,
    summary="Update a recipe",
    description="Partially update an existing recipe by ID. Ingredients list is fully replaced if provided.",
)
async def update_recipe(
    recipe_id: str,
    data: RecipeUpdate,
    user_id: str = Depends(get_current_user_id),
    service: RecipeService = Depends(get_recipe_service),
) -> RecipeRead:
    entry = await service.update_recipe(recipe_id, user_id, data)
    return RecipeRead.model_validate(entry)


# ---------------------------------------------------------------------------
# DELETE /api/v1/recipes/{recipe_id}
# ---------------------------------------------------------------------------
@router.delete(
    "/{recipe_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a recipe",
    description="Delete an existing recipe by ID.",
)
async def delete_recipe(
    recipe_id: str,
    user_id: str = Depends(get_current_user_id),
    service: RecipeService = Depends(get_recipe_service),
):
    await service.delete_recipe(recipe_id, user_id)
