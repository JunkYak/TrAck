"""
app/core/dependencies.py
------------------------
FastAPI dependency providers (Depends-compatible callables).

Centralising dependencies here prevents circular imports and makes the
injection graph easy to reason about.
"""

from __future__ import annotations

from typing import AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.core.exceptions import TokenError
from app.core.security import decode_token
from app.database.session import get_db_session

# Re-export for convenience so routers only need to import from here.
__all__ = [
    "get_settings",
    "get_session",
    "get_current_token_payload",
    "get_current_user_id",
    "get_weight_log_service",
    "get_measurement_session_service",
    "get_exercise_service",
    "get_exercise_log_service",
    "get_food_item_service",
    "get_recipe_service",
    "get_meal_template_service",
    "get_daily_nutrition_log_service",
    "get_cardio_session_service",
]

_bearer = HTTPBearer(auto_error=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield an :class:`AsyncSession` for the current request lifecycle."""
    async for session in get_db_session():
        yield session


async def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> dict:
    """Decode and return the JWT payload from the Authorization header.

    Raises HTTP 401 if the token is missing or invalid.
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = decode_token(credentials.credentials)
    except (JWTError, TokenError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload


# TODO: Replace this stub with the real JWT-based implementation below
# once Google OAuth is fully implemented.
#
# async def get_current_user_id(
#     payload: dict = Depends(get_current_token_payload),
# ) -> str:
#     user_id: str | None = payload.get("sub")
#     if user_id is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Token payload missing 'sub' claim",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user_id

# ── DEV-ONLY STUB ────────────────────────────────────────────────────────
_DEV_TEST_USER_ID = "00000000-0000-0000-0000-000000000001"


async def get_current_user_id() -> str:
    """Return a fixed test user ID for development.

    .. warning::
        This bypasses all authentication.  **Must** be replaced with the
        JWT-based version above before deploying to production.
    """
    return _DEV_TEST_USER_ID


# ---------------------------------------------------------------------------
# WeightLog
# ---------------------------------------------------------------------------
def get_weight_log_repository(
    session: AsyncSession = Depends(get_session),
):
    """Provide a :class:`WeightLogRepository` bound to the request session."""
    from app.repositories.weight_log import WeightLogRepository

    return WeightLogRepository(session)


def get_weight_log_service(
    repo=Depends(get_weight_log_repository),
):
    """Provide a :class:`WeightLogService` with its repository injected."""
    from app.services.weight_log import WeightLogService

    return WeightLogService(repo)


# ---------------------------------------------------------------------------
# MeasurementSession
# ---------------------------------------------------------------------------
def get_measurement_session_repository(
    session: AsyncSession = Depends(get_session),
):
    """Provide a :class:`MeasurementSessionRepository` bound to the request session."""
    from app.repositories.measurement_session import MeasurementSessionRepository

    return MeasurementSessionRepository(session)


def get_measurement_session_service(
    repo=Depends(get_measurement_session_repository),
):
    """Provide a :class:`MeasurementSessionService` with its repository injected."""
    from app.services.measurement_session import MeasurementSessionService

    return MeasurementSessionService(repo)


# ---------------------------------------------------------------------------
# Exercise
# ---------------------------------------------------------------------------
def get_exercise_repository(
    session: AsyncSession = Depends(get_session),
):
    """Provide an :class:`ExerciseRepository` bound to the request session."""
    from app.repositories.exercise import ExerciseRepository

    return ExerciseRepository(session)


def get_exercise_service(
    repo=Depends(get_exercise_repository),
):
    """Provide an :class:`ExerciseService` with its repository injected."""
    from app.services.exercise import ExerciseService

    return ExerciseService(repo)


# ---------------------------------------------------------------------------
# ExerciseLog
# ---------------------------------------------------------------------------
def get_exercise_log_repository(
    session: AsyncSession = Depends(get_session),
):
    """Provide an :class:`ExerciseLogRepository` bound to the request session."""
    from app.repositories.exercise_log import ExerciseLogRepository

    return ExerciseLogRepository(session)


def get_exercise_log_service(
    repo=Depends(get_exercise_log_repository),
    exercise_service=Depends(get_exercise_service),
):
    """Provide an :class:`ExerciseLogService` with its repository injected."""
    from app.services.exercise_log import ExerciseLogService

    return ExerciseLogService(repo, exercise_service)


# ---------------------------------------------------------------------------
# FoodItem
# ---------------------------------------------------------------------------
def get_food_item_repository(
    session: AsyncSession = Depends(get_session),
):
    """Provide a :class:`FoodItemRepository` bound to the request session."""
    from app.repositories.food_item import FoodItemRepository

    return FoodItemRepository(session)


def get_food_item_service(
    repo=Depends(get_food_item_repository),
):
    """Provide a :class:`FoodItemService` with its repository injected."""
    from app.services.food_item import FoodItemService

    return FoodItemService(repo)


# ---------------------------------------------------------------------------
# Recipe
# ---------------------------------------------------------------------------
def get_recipe_repository(
    session: AsyncSession = Depends(get_session),
):
    """Provide a :class:`RecipeRepository` bound to the request session."""
    from app.repositories.recipe import RecipeRepository

    return RecipeRepository(session)


def get_recipe_service(
    repo=Depends(get_recipe_repository),
    food_repo=Depends(get_food_item_repository),
):
    """Provide a :class:`RecipeService` with its repositories injected."""
    from app.services.recipe import RecipeService

    return RecipeService(repo, food_repo)


# ---------------------------------------------------------------------------
# MealTemplate
# ---------------------------------------------------------------------------
def get_meal_template_repository(
    session: AsyncSession = Depends(get_session),
):
    """Provide a :class:`MealTemplateRepository` bound to the request session."""
    from app.repositories.meal_template import MealTemplateRepository

    return MealTemplateRepository(session)


def get_meal_template_service(
    repo=Depends(get_meal_template_repository),
    food_repo=Depends(get_food_item_repository),
    recipe_repo=Depends(get_recipe_repository),
):
    """Provide a :class:`MealTemplateService` with its repositories injected."""
    from app.services.meal_template import MealTemplateService

    return MealTemplateService(repo, food_repo, recipe_repo)


# ---------------------------------------------------------------------------
# DailyNutritionLog
# ---------------------------------------------------------------------------
def get_daily_nutrition_log_repository(
    session: AsyncSession = Depends(get_session),
):
    """Provide a :class:`DailyNutritionLogRepository` bound to the request session."""
    from app.repositories.nutrition_log import DailyNutritionLogRepository

    return DailyNutritionLogRepository(session)


def get_daily_nutrition_log_entry_repository(
    session: AsyncSession = Depends(get_session),
):
    """Provide a :class:`DailyNutritionLogEntryRepository` bound to the request session."""
    from app.repositories.nutrition_log import DailyNutritionLogEntryRepository

    return DailyNutritionLogEntryRepository(session)


def get_daily_nutrition_log_item_repository(
    session: AsyncSession = Depends(get_session),
):
    """Provide a :class:`DailyNutritionLogItemRepository` bound to the request session."""
    from app.repositories.nutrition_log import DailyNutritionLogItemRepository

    return DailyNutritionLogItemRepository(session)


def get_daily_nutrition_log_service(
    repo=Depends(get_daily_nutrition_log_repository),
    entry_repo=Depends(get_daily_nutrition_log_entry_repository),
    item_repo=Depends(get_daily_nutrition_log_item_repository),
    food_repo=Depends(get_food_item_repository),
):
    """Provide a :class:`DailyNutritionLogService` with its repositories injected."""
    from app.services.nutrition_log import DailyNutritionLogService

    return DailyNutritionLogService(repo, entry_repo, item_repo, food_repo)


# ---------------------------------------------------------------------------
# CardioSession
# ---------------------------------------------------------------------------
def get_cardio_session_repository(
    session: AsyncSession = Depends(get_session),
):
    """Provide a :class:`CardioSessionRepository` bound to the request session."""
    from app.repositories.cardio import CardioSessionRepository

    return CardioSessionRepository(session)


def get_cardio_session_service(
    repo=Depends(get_cardio_session_repository),
    weight_repo=Depends(get_weight_log_repository),
):
    """Provide a :class:`CardioSessionService` with its repositories injected."""
    from app.services.cardio import CardioSessionService

    return CardioSessionService(repo, weight_repo)
