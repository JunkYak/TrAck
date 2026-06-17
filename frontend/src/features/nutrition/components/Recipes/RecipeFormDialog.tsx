import { useState, useEffect, useRef, useMemo } from 'react';
import * as Dialog from '@radix-ui/react-dialog';
import { useForm, useFieldArray, useWatch } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { RecipeRead, FoodItemRead } from '../../types';
import { useCreateRecipe, useUpdateRecipe, useFoods } from '../../api/nutrition';
import { useDebounce } from '../../../../hooks/useDebounce';

const recipeSchema = z.object({
  name: z.string().min(1, 'Name is required').max(255),
  ingredients: z.array(z.object({
    food_item_id: z.string(),
    quantity: z.number().min(0.01, 'Quantity must be > 0'),
    food_item: z.any(), // Stored for UI preview purposes
  })).min(1, 'At least one ingredient is required')
});

type RecipeFormValues = z.infer<typeof recipeSchema>;

interface RecipeFormDialogProps {
  isOpen: boolean;
  onOpenChange: (open: boolean) => void;
  recipeToEdit?: RecipeRead | null;
}

export const RecipeFormDialog = ({ isOpen, onOpenChange, recipeToEdit }: RecipeFormDialogProps) => {
  const createMutation = useCreateRecipe();
  const updateMutation = useUpdateRecipe();

  const { register, control, handleSubmit, reset, formState: { errors } } = useForm<RecipeFormValues>({
    resolver: zodResolver(recipeSchema),
    defaultValues: {
      name: '',
      ingredients: [],
    }
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: "ingredients"
  });

  // Watch ingredients to calculate live macros
  const currentIngredients = useWatch({
    control,
    name: "ingredients",
  }) || [];

  const { totalCalories, totalProtein } = useMemo(() => {
    if (!currentIngredients) return { totalCalories: 0, totalProtein: 0 };
    return currentIngredients.reduce(
      (acc, ing) => {
        const qty = parseFloat(ing.quantity as any) || 0;
        acc.totalCalories += qty * (ing.food_item.calories_per_unit || 0);
        acc.totalProtein += qty * (ing.food_item.protein_per_unit || 0);
        return acc;
      },
      { totalCalories: 0, totalProtein: 0 }
    );
  }, [currentIngredients]);

  // Food Search
  const [foodSearch, setFoodSearch] = useState('');
  const searchInputRef = useRef<HTMLInputElement>(null);
  const debouncedSearch = useDebounce(foodSearch, 300);
  const { data: searchResults, isLoading: isSearchLoading } = useFoods(debouncedSearch);

  useEffect(() => {
    if (recipeToEdit && isOpen) {
      reset({
        name: recipeToEdit.name,
        ingredients: recipeToEdit.ingredients.map(ing => ({
          food_item_id: ing.food_item_id,
          quantity: ing.quantity,
          food_item: ing.food_item
        }))
      });
      setFoodSearch('');
    } else if (isOpen && !recipeToEdit) {
      reset({
        name: '',
        ingredients: [],
      });
      setFoodSearch('');
    }
  }, [recipeToEdit, isOpen, reset]);

  const handleAddIngredient = (food: FoodItemRead) => {
    append({
      food_item_id: food.id,
      quantity: 100, // Default 100g or 1 unit
      food_item: food
    });
    setFoodSearch('');
    searchInputRef.current?.focus();
  };

  const onSubmit = (data: RecipeFormValues) => {
    // Strip `food_item` out of payload to match API DTO
    const payloadIngredients = data.ingredients.map(ing => ({
      food_item_id: ing.food_item_id,
      quantity: ing.quantity
    }));

    if (recipeToEdit) {
      updateMutation.mutate({ 
        recipeId: recipeToEdit.id, 
        update: { name: data.name, ingredients: payloadIngredients } 
      }, {
        onSuccess: () => onOpenChange(false)
      });
    } else {
      createMutation.mutate({ 
        name: data.name, 
        ingredients: payloadIngredients 
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
        <Dialog.Content className="fixed bottom-0 left-0 right-0 md:top-[50%] md:left-[50%] md:translate-x-[-50%] md:translate-y-[-50%] md:bottom-auto w-full md:max-w-2xl bg-[#121212] border-t md:border border-[#2A2A2A] p-6 rounded-t-2xl md:rounded-xl shadow-2xl z-50 max-h-[90vh] flex flex-col">
          <Dialog.Title className="text-xl font-bold text-white mb-4">
            {recipeToEdit ? 'Edit Recipe' : 'Create Recipe'}
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
            <form id="recipe-form" onSubmit={handleSubmit(onSubmit)} className="space-y-6">
              <div>
                <label className="block text-sm font-bold text-gray-400 mb-2">Recipe Name</label>
                <input
                  {...register('name')}
                  className="w-full bg-[#1A1A1A] text-white p-3 rounded-lg border border-[#2A2A2A] focus:border-amber-500 outline-none"
                  placeholder="e.g., Morning Protein Shake"
                />
                {errors.name && <p className="text-red-500 text-xs mt-1">{errors.name.message}</p>}
              </div>

              <div>
                <label className="block text-sm font-bold text-gray-400 mb-2">Ingredients</label>
                
                {fields.length === 0 ? (
                  <div className="p-4 bg-[#0A0A0A] border border-dashed border-[#2A2A2A] rounded-xl text-center text-sm text-gray-500 mb-4">
                    No ingredients added yet. Search below to add foods.
                  </div>
                ) : (
                  <div className="space-y-3 mb-4">
                    {fields.map((field, index) => (
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
                            {...register(`ingredients.${index}.quantity`, { valueAsNumber: true })}
                            className="w-full bg-[#0A0A0A] text-white p-2 rounded-lg border border-[#2A2A2A] focus:border-amber-500 outline-none text-right"
                          />
                        </div>
                        <div className="text-sm text-gray-500 w-8 text-center">
                          {(field.food_item as FoodItemRead).unit}
                        </div>
                        <button
                          type="button"
                          onClick={() => remove(index)}
                          className="p-2 text-red-500 hover:text-red-400 transition-colors"
                          title="Remove ingredient"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                          </svg>
                        </button>
                      </div>
                    ))}
                  </div>
                )}
                {errors.ingredients?.message && <p className="text-red-500 text-xs mt-1">{errors.ingredients.message}</p>}
                
                {/* Search Panel */}
                <div className="mt-6 border-t border-[#2A2A2A] pt-4">
                  <label className="block text-sm font-bold text-gray-400 mb-2">Add Ingredient</label>
                  <input
                    ref={searchInputRef}
                    type="text"
                    value={foodSearch}
                    onChange={(e) => setFoodSearch(e.target.value)}
                    placeholder="Search foods..."
                    className="w-full bg-[#0A0A0A] text-white p-3 rounded-lg border border-[#2A2A2A] focus:border-amber-500 outline-none mb-3"
                  />
                  
                  {debouncedSearch && (
                    <div className="bg-[#0A0A0A] rounded-lg border border-[#2A2A2A] max-h-48 overflow-y-auto custom-scrollbar">
                      {isSearchLoading ? (
                        <div className="p-3 text-center text-sm text-gray-500">Searching...</div>
                      ) : searchResults?.length === 0 ? (
                        <div className="p-3 text-center text-sm text-gray-500">No foods found.</div>
                      ) : (
                        searchResults?.map((food) => (
                          <button
                            key={food.id}
                            type="button"
                            onClick={() => handleAddIngredient(food)}
                            className="w-full text-left p-3 border-b border-[#1A1A1A] last:border-0 hover:bg-[#1A1A1A] transition-colors flex justify-between items-center"
                          >
                            <span className="font-bold text-white text-sm">{food.name}</span>
                            <span className="text-xs text-amber-500">{food.calories_per_unit} kcal/{food.unit}</span>
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
              form="recipe-form"
              disabled={isPending}
              className="px-6 py-3 bg-amber-500 hover:bg-amber-400 text-black font-bold rounded-lg transition-colors"
            >
              {isPending ? 'Saving...' : 'Save Recipe'}
            </button>
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
};
