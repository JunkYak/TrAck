"""Repositories package – data access layer."""

from app.repositories.base import BaseRepository  # noqa: F401
from app.repositories.exercise import ExerciseRepository  # noqa: F401
from app.repositories.exercise_log import ExerciseLogRepository  # noqa: F401
from app.repositories.food_item import FoodItemRepository  # noqa: F401
from app.repositories.meal_template import MealTemplateRepository  # noqa: F401
from app.repositories.measurement_session import MeasurementSessionRepository  # noqa: F401
from app.repositories.nutrition_log import (  # noqa: F401
    DailyNutritionLogEntryRepository,
    DailyNutritionLogItemRepository,
    DailyNutritionLogRepository,
)
from app.repositories.recipe import RecipeRepository  # noqa: F401
from app.repositories.user import UserRepository  # noqa: F401
from app.repositories.weight_log import WeightLogRepository  # noqa: F401

__all__ = [
    "BaseRepository",
    "DailyNutritionLogEntryRepository",
    "DailyNutritionLogItemRepository",
    "DailyNutritionLogRepository",
    "ExerciseRepository",
    "ExerciseLogRepository",
    "FoodItemRepository",
    "MealTemplateRepository",
    "MeasurementSessionRepository",
    "RecipeRepository",
    "UserRepository",
    "WeightLogRepository",
]
