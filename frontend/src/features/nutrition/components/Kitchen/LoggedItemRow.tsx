import { useState } from 'react';
import { DailyNutritionLogItemRead } from '../../types';
import { useUpdateLogItem, useDeleteLogItem } from '../../api/nutrition';

interface LoggedItemRowProps {
  item: DailyNutritionLogItemRead;
  date: string;
  isIndented?: boolean;
}

export const LoggedItemRow = ({ item, date, isIndented = false }: LoggedItemRowProps) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editQuantity, setEditQuantity] = useState(item.quantity.toString());

  const updateMutation = useUpdateLogItem(date);
  const deleteMutation = useDeleteLogItem(date);

  const handleSave = (e: React.MouseEvent | React.FormEvent) => {
    e.preventDefault();
    e.stopPropagation();
    
    const newQuantity = parseFloat(editQuantity);
    if (isNaN(newQuantity) || newQuantity <= 0) return;

    // The backend does not automatically recalculate macros.
    // We must scale the calories and protein based on the base units.
    const caloriesPerUnit = item.calories / item.quantity;
    const proteinPerUnit = item.protein / item.quantity;

    updateMutation.mutate({
      itemId: item.id,
      update: {
        quantity: newQuantity,
        calories: caloriesPerUnit * newQuantity,
        protein: proteinPerUnit * newQuantity,
      }
    });
    setIsEditing(false);
  };

  const handleDelete = (e: React.MouseEvent) => {
    e.stopPropagation();
    deleteMutation.mutate(item.id);
    setIsEditing(false);
  };

  const handleCancel = (e: React.MouseEvent) => {
    e.stopPropagation();
    setIsEditing(false);
    setEditQuantity(item.quantity.toString());
  };

  if (isEditing) {
    return (
      <div 
        className={`flex flex-col sm:flex-row sm:items-center justify-between py-3 border-b border-[#1A1A1A] bg-[#1A1A1A] transition-colors ${
          isIndented ? 'pl-6 pr-2' : 'px-2'
        }`}
      >
        <div className="flex flex-col mb-3 sm:mb-0">
          <span className="text-white font-medium">{item.food_name}</span>
          <span className="text-xs text-gray-500">Edit quantity ({item.unit})</span>
        </div>
        <form onSubmit={handleSave} className="flex items-center space-x-2">
          <input
            type="number"
            step="any"
            value={editQuantity}
            onChange={(e) => setEditQuantity(e.target.value)}
            className="w-20 bg-[#0A0A0A] text-white px-2 py-1.5 rounded text-sm outline-none border border-[#3A3A3A] focus:border-amber-500"
            autoFocus
            onClick={(e) => e.stopPropagation()}
          />
          <button 
            type="button" 
            onClick={handleDelete}
            disabled={deleteMutation.isPending}
            className="text-xs text-red-500 hover:text-red-400 font-bold px-2 py-1"
          >
            Delete
          </button>
          <button 
            type="button"
            onClick={handleCancel}
            className="text-xs text-gray-400 hover:text-white px-2 py-1"
          >
            Cancel
          </button>
          <button 
            type="submit" 
            disabled={updateMutation.isPending}
            className="text-xs bg-amber-500 hover:bg-amber-400 text-[#0A0A0A] font-bold px-3 py-1.5 rounded transition-colors"
          >
            Save
          </button>
        </form>
      </div>
    );
  }

  return (
    <div 
      onClick={() => setIsEditing(true)}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          setIsEditing(true);
        }
      }}
      className={`flex items-center justify-between py-3 border-b border-[#1A1A1A] hover:bg-[#1A1A1A]/50 transition-colors cursor-pointer group ${
        isIndented ? 'pl-6 pr-2' : 'px-2'
      }`}
    >
      <div className="flex flex-col">
        <span className="text-white font-medium group-hover:text-amber-500 transition-colors">{item.food_name}</span>
        <span className="text-sm text-gray-500">
          {item.quantity} {item.unit}
        </span>
      </div>
      <div className="flex flex-col items-end">
        <span className="text-amber-500 font-bold">{Number(item.calories.toFixed(1))} kcal</span>
        <span className="text-sm text-gray-500">{Number(item.protein.toFixed(1))}g protein</span>
      </div>
    </div>
  );
};
