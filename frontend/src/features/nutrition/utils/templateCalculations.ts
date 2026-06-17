import { MealTemplateRead, DailyNutritionLogEntryCreate, DailyNutritionLogItemCreate } from '../types';

export const calculateTemplateMacros = (template: MealTemplateRead) => {
  let calories = 0;
  let protein = 0;

  // Add direct foods
  template.foods.forEach(tf => {
    calories += tf.food_item.calories_per_unit * tf.quantity;
    protein += tf.food_item.protein_per_unit * tf.quantity;
  });

  // Add recipes
  template.recipes.forEach(tr => {
    tr.recipe.ingredients.forEach(ing => {
      calories += ing.food_item.calories_per_unit * ing.quantity * tr.multiplier;
      protein += ing.food_item.protein_per_unit * ing.quantity * tr.multiplier;
    });
  });

  return { calories, protein };
};

export const flattenTemplateForLog = (template: MealTemplateRead): DailyNutritionLogEntryCreate => {
  const items: DailyNutritionLogItemCreate[] = [];

  // Flatten direct foods attached to template
  template.foods.forEach(tf => {
    items.push({
      food_name: tf.food_item.name,
      quantity: tf.quantity,
      unit: tf.food_item.unit,
      calories: tf.food_item.calories_per_unit * tf.quantity,
      protein: tf.food_item.protein_per_unit * tf.quantity,
    });
  });

  // Flatten nested recipes inside template
  template.recipes.forEach(tr => {
    tr.recipe.ingredients.forEach(ing => {
      items.push({
        food_name: ing.food_item.name,
        quantity: ing.quantity * tr.multiplier,
        unit: ing.food_item.unit,
        calories: ing.food_item.calories_per_unit * ing.quantity * tr.multiplier,
        protein: ing.food_item.protein_per_unit * ing.quantity * tr.multiplier,
      });
    });
  });

  return {
    entry_name: template.name,
    entry_type: 'TEMPLATE',
    items,
  };
};
