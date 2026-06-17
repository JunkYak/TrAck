import { useMemo } from 'react';
import { DailyNutritionLogRead } from '../../types';

interface NutritionSummaryCardProps {
  log: DailyNutritionLogRead;
}

export const NutritionSummaryCard = ({ log }: NutritionSummaryCardProps) => {
  // Calculate totals natively on the frontend to avoid extra backend calls
  const { totalCalories, totalProtein } = useMemo(() => {
    return log.entries.reduce(
      (acc, entry) => {
        entry.items.forEach((item) => {
          acc.totalCalories += item.calories;
          acc.totalProtein += item.protein;
        });
        return acc;
      },
      { totalCalories: 0, totalProtein: 0 }
    );
  }, [log.entries]);

  return (
    <div className="w-full bg-[#1A1A1A] rounded-xl p-6 shadow-lg mb-8 border border-[#2A2A2A]">
      <h2 className="text-lg font-bold text-gray-400 mb-4 tracking-tight">Today's Nutrition</h2>
      <div className="flex items-baseline space-x-3">
        <span className="text-4xl lg:text-5xl font-black text-amber-500 tracking-tighter">
          {Math.round(totalCalories)}
        </span>
        <span className="text-xl text-amber-500/80 font-bold">kcal</span>
      </div>
      <div className="mt-2 text-gray-300 font-medium text-lg">
        {Math.round(totalProtein)}g protein
      </div>
    </div>
  );
};
