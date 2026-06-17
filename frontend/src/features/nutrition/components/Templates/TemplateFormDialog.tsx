import { useState, useEffect, useRef, useMemo } from 'react';
import * as Dialog from '@radix-ui/react-dialog';
import { useForm, useFieldArray, useWatch } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { MealTemplateRead, FoodItemRead, RecipeRead } from '../../types';
import { useCreateTemplate, useUpdateTemplate, useFoods, useRecipes } from '../../api/nutrition';
import { useDebounce } from '../../../../hooks/useDebounce';

const templateSchema = z.object({
  name: z.string().min(1, 'Name is required').max(255),
  foods: z.array(z.object({
    food_item_id: z.string(),
    quantity: z.number().min(0.01, 'Quantity must be > 0'),
    food_item: z.any(), // Stored for UI preview purposes
  })),
  recipes: z.array(z.object({
    recipe_id: z.string(),
    multiplier: z.number().min(0.01, 'Multiplier must be > 0'),
    recipe: z.any(), // Stored for UI preview purposes
  }))
});

type TemplateFormValues = z.infer<typeof templateSchema>;

interface TemplateFormDialogProps {
  isOpen: boolean;
  onOpenChange: (open: boolean) => void;
  templateToEdit?: MealTemplateRead | null;
}

export const TemplateFormDialog = ({ isOpen, onOpenChange, templateToEdit }: TemplateFormDialogProps) => {
  const createMutation = useCreateTemplate();
  const updateMutation = useUpdateTemplate();

  const { register, control, handleSubmit, reset, formState: { errors } } = useForm<TemplateFormValues>({
    resolver: zodResolver(templateSchema),
    defaultValues: {
      name: '',
      foods: [],
      recipes: [],
    }
  });

  const { fields: foodFields, append: appendFood, remove: removeFood } = useFieldArray({
    control,
    name: "foods"
  });

  const { fields: recipeFields, append: appendRecipe, remove: removeRecipe } = useFieldArray({
    control,
    name: "recipes"
  });

  // Watch to calculate live macros
  const currentFoods = useWatch({ control, name: "foods" }) || [];
  const currentRecipes = useWatch({ control, name: "recipes" }) || [];

  const { totalCalories, totalProtein } = useMemo(() => {
    let cal = 0;
    let prot = 0;

    currentFoods.forEach(tf => {
      const qty = parseFloat(tf.quantity as any) || 0;
      cal += qty * ((tf.food_item as FoodItemRead)?.calories_per_unit || 0);
      prot += qty * ((tf.food_item as FoodItemRead)?.protein_per_unit || 0);
    });

    currentRecipes.forEach(tr => {
      const mult = parseFloat(tr.multiplier as any) || 0;
      (tr.recipe as RecipeRead)?.ingredients?.forEach(ing => {
        cal += ing.quantity * mult * ing.food_item.calories_per_unit;
        prot += ing.quantity * mult * ing.food_item.protein_per_unit;
      });
    });

    return { totalCalories: cal, totalProtein: prot };
  }, [currentFoods, currentRecipes]);

  // Food Search
  const [foodSearch, setFoodSearch] = useState('');
  const foodSearchInputRef = useRef<HTMLInputElement>(null);
  const debouncedFoodSearch = useDebounce(foodSearch, 300);
  const { data: foodSearchResults, isLoading: isFoodSearchLoading } = useFoods(debouncedFoodSearch);

  // Recipe List (Recipes are small enough we can just render a dropdown or searchable select)
  const { data: allRecipes } = useRecipes();
  const [recipeSearch, setRecipeSearch] = useState('');
  const recipeSearchInputRef = useRef<HTMLInputElement>(null);

  const filteredRecipes = useMemo(() => {
    if (!allRecipes) return [];
    if (!recipeSearch) return allRecipes;
    return allRecipes.filter(r => r.name.toLowerCase().includes(recipeSearch.toLowerCase()));
  }, [allRecipes, recipeSearch]);

  useEffect(() => {
    if (templateToEdit && isOpen) {
      reset({
        name: templateToEdit.name,
        foods: templateToEdit.foods.map(tf => ({
          food_item_id: tf.food_item_id,
          quantity: tf.quantity,
          food_item: tf.food_item
        })),
        recipes: templateToEdit.recipes.map(tr => ({
          recipe_id: tr.recipe_id,
          multiplier: tr.multiplier,
          recipe: tr.recipe
        }))
      });
      setFoodSearch('');
      setRecipeSearch('');
    } else if (isOpen && !templateToEdit) {
      reset({ name: '', foods: [], recipes: [] });
      setFoodSearch('');
      setRecipeSearch('');
    }
  }, [templateToEdit, isOpen, reset]);

  const handleAddFood = (food: FoodItemRead) => {
    appendFood({
      food_item_id: food.id,
      quantity: 100, // Default 100g or 1 unit
      food_item: food
    });
    setFoodSearch('');
    foodSearchInputRef.current?.focus();
  };

  const handleAddRecipe = (recipe: RecipeRead) => {
    appendRecipe({
      recipe_id: recipe.id,
      multiplier: 1.0,
      recipe: recipe
    });
    setRecipeSearch('');
    recipeSearchInputRef.current?.focus();
  };

  const onSubmit = (data: TemplateFormValues) => {
    // Strip UI objects out of payload
    const payloadFoods = data.foods.map(tf => ({
      food_item_id: tf.food_item_id,
      quantity: tf.quantity
    }));
    
    const payloadRecipes = data.recipes.map(tr => ({
      recipe_id: tr.recipe_id,
      multiplier: tr.multiplier
    }));

    // Must have at least 1 of either
    if (payloadFoods.length === 0 && payloadRecipes.length === 0) {
        alert("A template must contain at least one food or recipe.");
        return;
    }

    if (templateToEdit) {
      updateMutation.mutate({ 
        templateId: templateToEdit.id, 
        update: { name: data.name, foods: payloadFoods, recipes: payloadRecipes } 
      }, {
        onSuccess: () => onOpenChange(false)
      });
    } else {
      createMutation.mutate({ 
        name: data.name, 
        foods: payloadFoods, 
        recipes: payloadRecipes 
      }, {
        onSuccess: () => onOpenChange(false)
      });
    }
  };

  const isPending = createMutation.isPending || updateMutation.isPending;

  return (
    <Dialog.Root open={isOpen} onOpenChange={onOpenChange}>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-black/80 backdrop-blur-sm z-40" />
        <Dialog.Content className="fixed bottom-0 left-0 right-0 md:top-[50%] md:left-[50%] md:translate-x-[-50%] md:translate-y-[-50%] md:bottom-auto w-full md:max-w-3xl bg-[#121212] border-t md:border border-[#2A2A2A] p-6 rounded-t-2xl md:rounded-xl shadow-2xl z-50 max-h-[90vh] flex flex-col">
          <Dialog.Title className="text-xl font-bold text-white mb-4">
            {templateToEdit ? 'Edit Template' : 'Create Template'}
          </Dialog.Title>

          {/* Sticky Macro Bar */}
          <div className="bg-[#1A1A1A] rounded-lg p-4 mb-6 border border-[#2A2A2A] flex justify-between items-center shrink-0">
            <div>
              <span className="text-gray-400 text-sm font-bold block mb-1">Total Calories</span>
              <span className="text-2xl font-black text-amber-500">{Math.round(totalCalories)} <span className="text-sm font-bold text-amber-500/80">kcal</span></span>
            </div>
            <div className="text-right">
              <span className="text-gray-400 text-sm font-bold block mb-1">Total Protein</span>
              <span className="text-xl font-bold text-gray-200">{Math.round(totalProtein)}g</span>
            </div>
          </div>
          
          <div className="overflow-y-auto flex-1 pr-2 custom-scrollbar">
            <form id="template-form" onSubmit={handleSubmit(onSubmit)} className="space-y-6">
              <div>
                <label className="block text-sm font-bold text-gray-400 mb-2">Template Name</label>
                <input
                  {...register('name')}
                  className="w-full bg-[#1A1A1A] text-white p-3 rounded-lg border border-[#2A2A2A] focus:border-amber-500 outline-none"
                  placeholder="e.g., Standard Bodybuilding Breakfast"
                />
                {errors.name && <p className="text-red-500 text-xs mt-1">{errors.name.message}</p>}
              </div>

              {/* Foods Section */}
              <div className="bg-[#161616] border border-[#2A2A2A] rounded-xl p-4">
                <h3 className="text-md font-bold text-emerald-400 mb-4">Included Foods</h3>
                
                {foodFields.length === 0 ? (
                  <div className="p-4 bg-[#0A0A0A] border border-dashed border-[#2A2A2A] rounded-xl text-center text-sm text-gray-500 mb-4">
                    No individual foods added yet.
                  </div>
                ) : (
                  <div className="space-y-3 mb-4">
                    {foodFields.map((field, index) => (
                      <div key={field.id} className="flex items-center gap-3 bg-[#1A1A1A] p-3 rounded-lg border border-[#2A2A2A]">
                        <div className="flex-1">
                          <div className="font-bold text-white text-sm">{(field.food_item as FoodItemRead).name}</div>
                          <div className="text-xs text-gray-500">
                            {(field.food_item as FoodItemRead).calories_per_unit} kcal / {(field.food_item as FoodItemRead).unit}
                          </div>
                        </div>
                        <div className="w-24">
                          <input
                            type="number"
                            step="any"
                            {...register(`foods.${index}.quantity`, { valueAsNumber: true })}
                            className="w-full bg-[#0A0A0A] text-white p-2 rounded-lg border border-[#2A2A2A] focus:border-amber-500 outline-none text-right"
                          />
                        </div>
                        <div className="text-sm text-gray-500 w-8 text-center">
                          {(field.food_item as FoodItemRead).unit}
                        </div>
                        <button
                          type="button"
                          onClick={() => removeFood(index)}
                          className="p-2 text-gray-500 hover:text-red-500 hover:bg-[#2A2A2A] rounded-lg transition-all"
                          title="Remove food"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                          </svg>
                        </button>
                      </div>
                    ))}
                  </div>
                )}
                
                {/* Food Search Panel */}
                <div className="mt-4 border-t border-[#2A2A2A] pt-4">
                  <input
                    ref={foodSearchInputRef}
                    type="text"
                    value={foodSearch}
                    onChange={(e) => setFoodSearch(e.target.value)}
                    placeholder="Search foods to add..."
                    className="w-full bg-[#0A0A0A] text-white p-3 rounded-lg border border-[#2A2A2A] focus:border-emerald-500 outline-none mb-3"
                  />
                  {debouncedFoodSearch && (
                    <div className="bg-[#0A0A0A] rounded-lg border border-[#2A2A2A] max-h-48 overflow-y-auto custom-scrollbar">
                      {isFoodSearchLoading ? (
                        <div className="p-3 text-center text-sm text-gray-500">Searching...</div>
                      ) : foodSearchResults?.length === 0 ? (
                        <div className="p-3 text-center text-sm text-gray-500">No foods found.</div>
                      ) : (
                        foodSearchResults?.map((food) => (
                          <button
                            key={food.id}
                            type="button"
                            onClick={() => handleAddFood(food)}
                            className="w-full text-left p-3 border-b border-[#1A1A1A] last:border-0 hover:bg-[#1A1A1A] transition-colors flex justify-between items-center"
                          >
                            <span className="font-bold text-white text-sm">{food.name}</span>
                            <span className="text-xs text-emerald-500">{food.calories_per_unit} kcal/{food.unit}</span>
                          </button>
                        ))
                      )}
                    </div>
                  )}
                </div>
              </div>

              {/* Recipes Section */}
              <div className="bg-[#161616] border border-[#2A2A2A] rounded-xl p-4">
                <h3 className="text-md font-bold text-blue-400 mb-4">Included Recipes</h3>
                
                {recipeFields.length === 0 ? (
                  <div className="p-4 bg-[#0A0A0A] border border-dashed border-[#2A2A2A] rounded-xl text-center text-sm text-gray-500 mb-4">
                    No recipes added yet.
                  </div>
                ) : (
                  <div className="space-y-3 mb-4">
                    {recipeFields.map((field, index) => (
                      <div key={field.id} className="flex items-center gap-3 bg-[#1A1A1A] p-3 rounded-lg border border-[#2A2A2A]">
                        <div className="flex-1">
                          <div className="font-bold text-white text-sm">{(field.recipe as RecipeRead).name}</div>
                          <div className="text-xs text-gray-500">
                            {(field.recipe as RecipeRead).ingredients.length} ingredients
                          </div>
                        </div>
                        <div className="w-24">
                          <input
                            type="number"
                            step="any"
                            {...register(`recipes.${index}.multiplier`, { valueAsNumber: true })}
                            className="w-full bg-[#0A0A0A] text-white p-2 rounded-lg border border-[#2A2A2A] focus:border-amber-500 outline-none text-right"
                          />
                        </div>
                        <div className="text-sm text-gray-500 w-8 text-center">
                          servings
                        </div>
                        <button
                          type="button"
                          onClick={() => removeRecipe(index)}
                          className="p-2 text-gray-500 hover:text-red-500 hover:bg-[#2A2A2A] rounded-lg transition-all"
                          title="Remove recipe"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                          </svg>
                        </button>
                      </div>
                    ))}
                  </div>
                )}
                
                {/* Recipe Search Panel */}
                <div className="mt-4 border-t border-[#2A2A2A] pt-4">
                  <input
                    ref={recipeSearchInputRef}
                    type="text"
                    value={recipeSearch}
                    onChange={(e) => setRecipeSearch(e.target.value)}
                    placeholder="Search recipes to add..."
                    className="w-full bg-[#0A0A0A] text-white p-3 rounded-lg border border-[#2A2A2A] focus:border-blue-500 outline-none mb-3"
                  />
                  {recipeSearch && (
                    <div className="bg-[#0A0A0A] rounded-lg border border-[#2A2A2A] max-h-48 overflow-y-auto custom-scrollbar">
                      {filteredRecipes.length === 0 ? (
                        <div className="p-3 text-center text-sm text-gray-500">No recipes found.</div>
                      ) : (
                        filteredRecipes.map((recipe) => (
                          <button
                            key={recipe.id}
                            type="button"
                            onClick={() => handleAddRecipe(recipe)}
                            className="w-full text-left p-3 border-b border-[#1A1A1A] last:border-0 hover:bg-[#1A1A1A] transition-colors flex justify-between items-center"
                          >
                            <span className="font-bold text-white text-sm">{recipe.name}</span>
                            <span className="text-xs text-blue-500">{recipe.ingredients.length} ingredients</span>
                          </button>
                        ))
                      )}
                    </div>
                  )}
                </div>
              </div>

              {(createMutation.isError || updateMutation.isError) && (
                <p className="text-red-500 text-sm mt-2">An error occurred while saving.</p>
              )}
            </form>
          </div>

          <div className="flex justify-end space-x-3 mt-6 pt-4 border-t border-[#2A2A2A] shrink-0">
            <Dialog.Close asChild>
              <button type="button" className="px-6 py-3 text-gray-400 hover:text-white font-bold transition-colors">
                Cancel
              </button>
            </Dialog.Close>
            <button
              type="submit"
              form="template-form"
              disabled={isPending}
              className="px-6 py-3 bg-amber-500 hover:bg-amber-400 text-black font-bold rounded-lg transition-colors"
            >
              {isPending ? 'Saving...' : 'Save Template'}
            </button>
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
};
