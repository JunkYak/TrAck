import { useState } from 'react';
import { useFoods, useDeleteFood } from '../api/nutrition';
import { useDebounce } from '../../../hooks/useDebounce';
import { FoodFormDialog } from '../components/Foods/FoodFormDialog';
import { FoodItemRead } from '../types';
import { LoadingState } from '../components/Shared/LoadingState';

export const FoodsPage = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const debouncedSearch = useDebounce(searchTerm, 300);
  
  const { data: foods, isLoading, isError } = useFoods(debouncedSearch);

  const deleteMutation = useDeleteFood();

  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [foodToEdit, setFoodToEdit] = useState<FoodItemRead | null>(null);
  const [deleteErrorMsg, setDeleteErrorMsg] = useState('');

  const handleEdit = (food: FoodItemRead) => {
    // Only allow editing if user_id is present (not a global food)
    if (food.user_id) {
      setFoodToEdit(food);
      setIsDialogOpen(true);
    }
  };

  const handleCreate = () => {
    setFoodToEdit(null);
    setIsDialogOpen(true);
  };

  const handleDelete = (e: React.MouseEvent, food: FoodItemRead) => {
    e.stopPropagation();
    if (!food.user_id) return;
    
    setDeleteErrorMsg('');
    deleteMutation.mutate(food.id, {
      onError: () => {
        setDeleteErrorMsg(`Could not delete ${food.name}. It may be currently used in a recipe.`);
      }
    });
  };

  return (
    <div className="p-4 lg:p-8 max-w-4xl mx-auto min-h-screen">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between mb-8 gap-4">
        <h1 className="text-3xl font-black text-white tracking-tighter uppercase">Foods Catalog</h1>
        <button 
          onClick={handleCreate}
          className="bg-amber-500 hover:bg-amber-400 text-black font-bold py-2 px-4 rounded-xl transition-colors whitespace-nowrap"
        >
          + Custom Food
        </button>
      </div>

      <div className="mb-8">
        <input 
          type="text" 
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Search global database and your personal foods..."
          className="w-full bg-[#1A1A1A] border border-[#2A2A2A] text-white p-4 rounded-xl outline-none focus:border-amber-500 transition-colors"
        />
      </div>

      {deleteErrorMsg && (
        <div className="mb-4 p-4 bg-red-500/10 border border-red-500/20 text-red-500 rounded-lg text-sm font-bold flex justify-between items-center">
          <span>{deleteErrorMsg}</span>
          <button className="text-xs underline hover:text-red-400" onClick={() => setDeleteErrorMsg('')}>Dismiss</button>
        </div>
      )}

      {!debouncedSearch ? (
        <div className="text-center py-20 text-gray-500">
          <p className="text-lg font-bold">Search for a food above to get started.</p>
        </div>
      ) : isLoading ? (
        <LoadingState />
      ) : isError ? (
        <div className="text-center py-20 text-red-500 font-bold">Failed to load foods.</div>
      ) : foods?.length === 0 ? (
        <div className="text-center py-20 text-gray-500">
          <p className="text-lg font-bold mb-4">No foods found matching "{debouncedSearch}".</p>
          <button onClick={handleCreate} className="text-amber-500 font-bold hover:underline">
            Create a custom food instead
          </button>
        </div>
      ) : (
        <div className="bg-[#0A0A0A] rounded-xl border border-[#1A1A1A] overflow-hidden">
          {foods?.map((food) => (
            <div 
              key={food.id}
              onClick={() => handleEdit(food)}
              className={`flex items-center justify-between p-4 border-b border-[#1A1A1A] hover:bg-[#1A1A1A]/50 transition-colors group ${food.user_id ? 'cursor-pointer' : 'cursor-default'}`}
            >
              <div className="flex flex-col">
                <div className="flex items-center space-x-3 mb-1">
                  <span className={`text-lg font-bold ${food.user_id ? 'text-white group-hover:text-amber-500 transition-colors' : 'text-gray-300'}`}>
                    {food.name}
                  </span>
                  {!food.user_id ? (
                    <span className="text-[10px] uppercase font-bold px-2 py-0.5 rounded border text-blue-400 bg-blue-400/10 border-blue-400/20">Global</span>
                  ) : (
                    <span className="text-[10px] uppercase font-bold px-2 py-0.5 rounded border text-purple-400 bg-purple-400/10 border-purple-400/20">Custom</span>
                  )}
                </div>
                <div className="flex space-x-4">
                  <span className="text-sm text-gray-500">{Number(food.calories_per_unit.toFixed(1))} kcal / {food.unit}</span>
                  <span className="text-sm text-gray-500">{Number(food.protein_per_unit.toFixed(1))}g protein / {food.unit}</span>
                </div>
              </div>
              
              {food.user_id && (
                <div className="flex items-center space-x-4 opacity-100 md:opacity-0 md:group-hover:opacity-100 transition-opacity">
                  <button 
                    onClick={(e) => handleDelete(e, food)} 
                    disabled={deleteMutation.isPending}
                    className="text-red-500 hover:text-red-400 text-sm font-bold px-2 py-1"
                  >
                    Delete
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      <FoodFormDialog 
        isOpen={isDialogOpen} 
        onOpenChange={setIsDialogOpen} 
        foodToEdit={foodToEdit} 
      />
    </div>
  );
};
