"""Schemas package – Pydantic request/response models."""

from app.schemas.common import (  # noqa: F401
    AppBaseModel,
    HealthResponse,
    MessageResponse,
    PaginatedResponse,
)
from app.schemas.exercise import (  # noqa: F401
    ExerciseBase,
    ExerciseCreate,
    ExerciseRead,
    ExerciseUpdate,
)
from app.schemas.exercise_log import (  # noqa: F401
    ExerciseLogBase,
    ExerciseLogCreate,
    ExerciseLogRead,
    ExerciseLogUpdate,
)
from app.schemas.food_item import (  # noqa: F401
    FoodItemBase,
    FoodItemCreate,
    FoodItemRead,
    FoodItemUpdate,
)
from app.schemas.meal_template import (  # noqa: F401
    MealTemplateBase,
    MealTemplateCreate,
    MealTemplateFoodCreate,
    MealTemplateFoodRead,
    MealTemplateRead,
    MealTemplateRecipeCreate,
    MealTemplateRecipeRead,
    MealTemplateUpdate,
)
from app.schemas.measurement_session import (  # noqa: F401
    MeasurementSessionBase,
    MeasurementSessionCreate,
    MeasurementSessionRead,
    MeasurementSessionUpdate,
)
from app.schemas.nutrition_log import (  # noqa: F401
    DailyNutritionLogEntryBase,
    DailyNutritionLogEntryCreate,
    DailyNutritionLogEntryRead,
    DailyNutritionLogItemBase,
    DailyNutritionLogItemCreate,
    DailyNutritionLogItemRead,
    DailyNutritionLogItemUpdate,
    DailyNutritionLogRead,
)
from app.schemas.recipe import (  # noqa: F401
    RecipeBase,
    RecipeCreate,
    RecipeIngredientBase,
    RecipeIngredientCreate,
    RecipeIngredientRead,
    RecipeRead,
    RecipeUpdate,
)
from app.schemas.user import (  # noqa: F401
    UserBase,
    UserCreate,
    UserInDB,
    UserRead,
    UserUpdate,
)
from app.schemas.weight_log import (  # noqa: F401
    WeightLogBase,
    WeightLogCreate,
    WeightLogRead,
    WeightLogUpdate,
)

__all__ = [
    "AppBaseModel",
    "HealthResponse",
    "ExerciseBase",
    "ExerciseCreate",
    "ExerciseRead",
    "ExerciseUpdate",
    "ExerciseLogBase",
    "ExerciseLogCreate",
    "ExerciseLogRead",
    "ExerciseLogUpdate",
    "FoodItemBase",
    "FoodItemCreate",
    "FoodItemRead",
    "FoodItemUpdate",
    "MealTemplateBase",
    "MealTemplateCreate",
    "MealTemplateFoodCreate",
    "MealTemplateFoodRead",
    "MealTemplateRead",
    "MealTemplateRecipeCreate",
    "MealTemplateRecipeRead",
    "MealTemplateUpdate",
    "MeasurementSessionBase",
    "MeasurementSessionCreate",
    "MeasurementSessionRead",
    "MeasurementSessionUpdate",
    "MessageResponse",
    "DailyNutritionLogEntryBase",
    "DailyNutritionLogEntryCreate",
    "DailyNutritionLogEntryRead",
    "DailyNutritionLogItemBase",
    "DailyNutritionLogItemCreate",
    "DailyNutritionLogItemRead",
    "DailyNutritionLogItemUpdate",
    "DailyNutritionLogRead",
    "PaginatedResponse",
    "RecipeBase",
    "RecipeCreate",
    "RecipeIngredientBase",
    "RecipeIngredientCreate",
    "RecipeIngredientRead",
    "RecipeRead",
    "RecipeUpdate",
    "UserBase",
    "UserCreate",
    "UserInDB",
    "UserRead",
    "UserUpdate",
    "WeightLogBase",
    "WeightLogCreate",
    "WeightLogRead",
    "WeightLogUpdate",
]
