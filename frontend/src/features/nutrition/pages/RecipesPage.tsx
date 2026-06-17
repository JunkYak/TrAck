import { useState } from 'react';
import { useRecipes, useDeleteRecipe } from '../api/nutrition';
import { RecipeFormDialog } from '../components/Recipes/RecipeFormDialog';
import { RecipeRead } from '../types';
import { LoadingState } from '../components/Shared/LoadingState';

export const RecipesPage = () => {
  const { data: recipes, isLoading, isError } = useRecipes();
  const deleteMutation = useDeleteRecipe();

  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [recipeToEdit, setRecipeToEdit] = useState<RecipeRead | null>(null);

  const handleEdit = (recipe: RecipeRead) => {
    setRecipeToEdit(recipe);
    setIsDialogOpen(true);
  };

  const handleCreate = () => {
    setRecipeToEdit(null);
    setIsDialogOpen(true);
  };

  const handleDelete = (e: React.MouseEvent, recipe: RecipeRead) => {
    e.stopPropagation();
    if (confirm(`Are you sure you want to delete the recipe "${recipe.name}"?`)) {
      deleteMutation.mutate(recipe.id);
    }
  };

  return (
    <div className="p-4 lg:p-8 max-w-4xl mx-auto min-h-screen">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between mb-8 gap-4">
        <h1 className="text-3xl font-black text-white tracking-tighter uppercase">Recipes</h1>
        <button 
          onClick={handleCreate}
          className="bg-amber-500 hover:bg-amber-400 text-black font-bold py-2 px-4 rounded-xl transition-colors whitespace-nowrap"
        >
          + Create Recipe
        </button>
      </div>

      {isLoading ? (
        <LoadingState />
      ) : isError ? (
        <div className="text-center py-20 text-red-500 font-bold">Failed to load recipes.</div>
      ) : recipes?.length === 0 ? (
        <div className="text-center py-20 text-gray-500">
          <p className="text-lg font-bold mb-4">No recipes found.</p>
          <button onClick={handleCreate} className="text-amber-500 font-bold hover:underline">
            Create your first recipe
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {recipes?.map((recipe) => {
            // Compute total macros on the fly
            const totalCalories = recipe.ingredients.reduce((acc, ing) => acc + (ing.quantity * ing.food_item.calories_per_unit), 0);
            const totalProtein = recipe.ingredients.reduce((acc, ing) => acc + (ing.quantity * ing.food_item.protein_per_unit), 0);
            
            return (
              <div 
                key={recipe.id}
                onClick={() => handleEdit(recipe)}
                className="bg-[#0A0A0A] rounded-xl border border-[#1A1A1A] p-5 cursor-pointer hover:bg-[#1A1A1A]/50 transition-colors group relative overflow-hidden"
              >
                <div className="flex justify-between items-start mb-4">
                  <h3 className="text-xl font-bold text-white group-hover:text-amber-500 transition-colors pr-8">
                    {recipe.name}
                  </h3>
                  <button 
                    onClick={(e) => handleDelete(e, recipe)} 
                    disabled={deleteMutation.isPending}
                    className="absolute top-4 right-4 text-red-500/0 group-hover:text-red-500 hover:text-red-400 text-sm font-bold transition-colors p-1"
                    title="Delete Recipe"
                  >
                    Delete
                  </button>
                </div>
                
                <div className="text-sm text-gray-400 mb-6 font-medium">
                  {recipe.ingredients.length} {recipe.ingredients.length === 1 ? 'ingredient' : 'ingredients'}
                </div>
                
                <div className="flex justify-between items-end mt-auto pt-4 border-t border-[#1A1A1A]">
                  <div>
                    <span className="text-sm font-bold text-gray-500 block">Total Calories</span>
                    <span className="text-xl font-black text-amber-500">{Math.round(totalCalories)} <span className="text-xs font-bold">kcal</span></span>
                  </div>
                  <div className="text-right">
                    <span className="text-sm font-bold text-gray-500 block">Total Protein</span>
                    <span className="text-lg font-bold text-gray-200">{Math.round(totalProtein)}g</span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      <RecipeFormDialog 
        isOpen={isDialogOpen} 
        onOpenChange={setIsDialogOpen} 
        recipeToEdit={recipeToEdit} 
      />
    </div>
  );
};
