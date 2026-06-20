import { DailyNutritionLogSummaryRead } from '../../types';

interface PreviousLogRowProps {
  log: DailyNutritionLogSummaryRead;
}

const getDayName = (dateStr: string) => {
  const date = new Date(dateStr + 'T00:00:00');
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const diffTime = today.getTime() - date.getTime();
  const diffDays = Math.round(diffTime / (1000 * 60 * 60 * 24));

  if (diffDays === 0) return 'Today';
  if (diffDays === 1) return 'Yesterday';
  
  if (diffDays < 7) {
    return date.toLocaleDateString(undefined, { weekday: 'long' });
  }

  return date.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
};

export const PreviousLogRow = ({ log }: PreviousLogRowProps) => {
  const dayName = getDayName(log.date);

  return (
    <div className="bg-[#161616] border border-[#2A2A2A] rounded-xl p-4 flex justify-between items-center mb-3">
      <div>
        <h4 className="font-bold text-white">{dayName}</h4>
        <p className="text-xs text-gray-500">{log.date}</p>
      </div>
      <div className="text-right">
        <div className="flex items-baseline gap-1 justify-end">
          <span className="font-black text-white">{Math.round(log.total_calories)}</span>
          <span className="text-xs font-bold text-gray-500">kcal</span>
        </div>
        <p className="text-xs font-bold text-orange-500 mt-1">{Math.round(log.total_protein)}g Protein</p>
      </div>
    </div>
  );
};
