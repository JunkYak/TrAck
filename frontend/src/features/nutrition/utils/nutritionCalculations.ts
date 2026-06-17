import { 
  FoodItemRead, 
  RecipeRead, 
  MealTemplateRead, 
  DailyNutritionLogEntryCreate,
  DailyNutritionLogItemCreate
} from '../types';

export const buildFoodEntry = (food: FoodItemRead, quantity: number = 1): DailyNutritionLogEntryCreate => {
  return {
    entry_name: food.name,
    entry_type: 'FOOD',
    items: [
      {
        food_name: food.name,
        quantity: quantity,
        unit: food.unit,
        calories: food.calories_per_unit * quantity,
        protein: food.protein_per_unit * quantity,
      }
    ]
  };
};

export const buildRecipeEntry = (recipe: RecipeRead, multiplier: number = 1): DailyNutritionLogEntryCreate => {
  const items: DailyNutritionLogItemCreate[] = recipe.ingredients.map(ing => ({
    food_name: ing.food_item.name,
    quantity: ing.quantity * multiplier,
    unit: ing.food_item.unit,
    calories: ing.food_item.calories_per_unit * ing.quantity * multiplier,
    protein: ing.food_item.protein_per_unit * ing.quantity * multiplier,
  }));

  return {
    entry_name: recipe.name,
    entry_type: 'RECIPE',
    items,
  };
};

