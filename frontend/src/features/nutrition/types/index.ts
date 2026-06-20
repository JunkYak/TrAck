export interface FoodItemCreate {
  name: string;
  unit: string;
  calories_per_unit: number;
  protein_per_unit: number;
}

export interface FoodItemUpdate {
  name?: string;
  unit?: string;
  calories_per_unit?: number;
  protein_per_unit?: number;
}

export interface FoodItemRead extends FoodItemCreate {
  id: string;
  user_id: string | null;
  source: string;
  created_at: string;
  updated_at: string | null;
}

// Recipes
export interface RecipeIngredientCreate {
  food_item_id: string;
  quantity: number;
}

export interface RecipeIngredientRead {
  id: string;
  food_item_id: string;
  quantity: number;
  food_item: FoodItemRead;
}

export interface RecipeCreate {
  name: string;
  ingredients: RecipeIngredientCreate[];
}

export interface RecipeUpdate {
  name?: string;
  ingredients?: RecipeIngredientCreate[];
}

export interface RecipeRead {
  id: string;
  name: string;
  user_id: string;
  ingredients: RecipeIngredientRead[];
  created_at: string;
  updated_at: string | null;
}

// Meal Templates
export interface MealTemplateFoodCreate {
  food_item_id: string;
  quantity: number;
}

export interface MealTemplateFoodRead extends MealTemplateFoodCreate {
  id: string;
  food_item: FoodItemRead;
}

export interface MealTemplateRecipeCreate {
  recipe_id: string;
  multiplier: number;
}

export interface MealTemplateRecipeRead extends MealTemplateRecipeCreate {
  id: string;
  recipe: RecipeRead;
}

export interface MealTemplateCreate {
  name: string;
  foods: MealTemplateFoodCreate[];
  recipes: MealTemplateRecipeCreate[];
}

export interface MealTemplateUpdate {
  name?: string;
  foods?: MealTemplateFoodCreate[];
  recipes?: MealTemplateRecipeCreate[];
}

export interface MealTemplateRead {
  id: string;
  name: string;
  user_id: string;
  foods: MealTemplateFoodRead[];
  recipes: MealTemplateRecipeRead[];
  created_at: string;
  updated_at: string | null;
}

// Nutrition Logs
export interface DailyNutritionLogItemCreate {
  food_name: string;
  quantity: number;
  unit: string;
  calories: number;
  protein: number;
}

export interface DailyNutritionLogItemUpdate {
  quantity?: number;
  calories?: number;
  protein?: number;
}

export interface DailyNutritionLogItemRead extends DailyNutritionLogItemCreate {
  id: string;
  entry_id: string;
  created_at: string;
}

export interface DailyNutritionLogEntryCreate {
  entry_name: string;
  entry_type: string; // 'FOOD', 'RECIPE', 'TEMPLATE', 'CUSTOM'
  items: DailyNutritionLogItemCreate[];
}

export interface DailyNutritionLogEntryRead {
  id: string;
  log_id: string;
  entry_name: string;
  entry_type: string;
  items: DailyNutritionLogItemRead[];
  created_at: string;
}

export interface DailyNutritionLogRead {
  id: string;
  user_id: string;
  date: string;
  entries: DailyNutritionLogEntryRead[];
  created_at: string;
  updated_at: string | null;
}

export interface DailyNutritionLogSummaryRead {
  date: string;
  total_calories: number;
  total_protein: number;
}
