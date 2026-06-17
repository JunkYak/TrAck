import { useState, useEffect } from 'react';
import * as Dialog from '@radix-ui/react-dialog';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { FoodItemRead } from '../../types';
import { useCreateFood, useUpdateFood } from '../../api/nutrition';

const foodSchema = z.object({
  name: z.string().min(1, 'Name is required').max(255),
  unit: z.enum(['g', 'ml', 'count']),
  calories_per_unit: z.number().min(0),
  protein_per_unit: z.number().min(0),
});

type FoodFormValues = z.infer<typeof foodSchema>;

interface FoodFormDialogProps {
  isOpen: boolean;
  onOpenChange: (open: boolean) => void;
  foodToEdit?: FoodItemRead | null;
}

export const FoodFormDialog = ({ isOpen, onOpenChange, foodToEdit }: FoodFormDialogProps) => {
  const createMutation = useCreateFood();
  const updateMutation = useUpdateFood();
  
  const { register, handleSubmit, reset, formState: { errors } } = useForm<FoodFormValues>({
    resolver: zodResolver(foodSchema),
    defaultValues: {
      name: '',
      unit: 'g',
      calories_per_unit: 0,
      protein_per_unit: 0,
    }
  });

  useEffect(() => {
    if (foodToEdit && isOpen) {
      reset({
        name: foodToEdit.name,
        unit: foodToEdit.unit as any,
        calories_per_unit: foodToEdit.calories_per_unit,
        protein_per_unit: foodToEdit.protein_per_unit,
      });
    } else if (isOpen && !foodToEdit) {
      reset({
        name: '',
        unit: 'g',
        calories_per_unit: 0,
        protein_per_unit: 0,
      });
    }
  }, [foodToEdit, isOpen, reset]);

  const onSubmit = (data: FoodFormValues) => {
    if (foodToEdit) {
      updateMutation.mutate({ foodId: foodToEdit.id, update: data }, {
        onSuccess: () => onOpenChange(false)
      });
    } else {
      createMutation.mutate(data, {
        onSuccess: () => onOpenChange(false)
      });
    }
  };

  const isPending = createMutation.isPending || updateMutation.isPending;

  return (
    <Dialog.Root open={isOpen} onOpenChange={onOpenChange}>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-black/80 backdrop-blur-sm z-40" />
        <Dialog.Content className="fixed bottom-0 left-0 right-0 md:top-[50%] md:left-[50%] md:translate-x-[-50%] md:translate-y-[-50%] md:bottom-auto w-full md:max-w-md bg-[#121212] border-t md:border border-[#2A2A2A] p-6 rounded-t-2xl md:rounded-xl shadow-2xl z-50">
          <Dialog.Title className="text-xl font-bold text-white mb-4">
            {foodToEdit ? 'Edit Custom Food' : 'Create Custom Food'}
          </Dialog.Title>
          
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div>
              <label className="block text-sm font-bold text-gray-400 mb-1">Name</label>
              <input
                {...register('name')}
                className="w-full bg-[#1A1A1A] text-white p-3 rounded-lg border border-[#2A2A2A] focus:border-amber-500 outline-none"
                placeholder="e.g., Chicken Breast"
              />
              {errors.name && <p className="text-red-500 text-xs mt-1">{errors.name.message}</p>}
            </div>

            <div>
              <label className="block text-sm font-bold text-gray-400 mb-1">Unit</label>
              <select
                {...register('unit')}
                className="w-full bg-[#1A1A1A] text-white p-3 rounded-lg border border-[#2A2A2A] focus:border-amber-500 outline-none"
              >
                <option value="g">Grams (g)</option>
                <option value="ml">Milliliters (ml)</option>
                <option value="count">Count (ea)</option>
              </select>
              {errors.unit && <p className="text-red-500 text-xs mt-1">{errors.unit.message}</p>}
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-bold text-gray-400 mb-1">Calories / unit</label>
                <input
                  type="number"
                  step="any"
                  {...register('calories_per_unit', { valueAsNumber: true })}
                  className="w-full bg-[#1A1A1A] text-white p-3 rounded-lg border border-[#2A2A2A] focus:border-amber-500 outline-none"
                />
                {errors.calories_per_unit && <p className="text-red-500 text-xs mt-1">{errors.calories_per_unit.message}</p>}
              </div>
              <div>
                <label className="block text-sm font-bold text-gray-400 mb-1">Protein / unit</label>
                <input
                  type="number"
                  step="any"
                  {...register('protein_per_unit', { valueAsNumber: true })}
                  className="w-full bg-[#1A1A1A] text-white p-3 rounded-lg border border-[#2A2A2A] focus:border-amber-500 outline-none"
                />
                {errors.protein_per_unit && <p className="text-red-500 text-xs mt-1">{errors.protein_per_unit.message}</p>}
              </div>
            </div>

            {(createMutation.isError || updateMutation.isError) && (
              <p className="text-red-500 text-sm mt-2">An error occurred while saving.</p>
            )}

            <div className="flex justify-end space-x-3 mt-8">
              <Dialog.Close asChild>
                <button type="button" className="px-6 py-3 text-gray-400 hover:text-white font-bold transition-colors">
                  Cancel
                </button>
              </Dialog.Close>
              <button
                type="submit"
                disabled={isPending}
                className="px-6 py-3 bg-amber-500 hover:bg-amber-400 text-black font-bold rounded-lg transition-colors"
              >
                {isPending ? 'Saving...' : 'Save Food'}
              </button>
            </div>
          </form>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
};
