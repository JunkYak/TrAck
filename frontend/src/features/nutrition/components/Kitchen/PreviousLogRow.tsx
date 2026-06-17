interface PreviousLogRowProps {
  dayName: string;
  calories: number;
  protein: number;
}

export const PreviousLogRow = ({ dayName, calories, protein }: PreviousLogRowProps) => {
  return (
    <div className="flex items-center justify-between p-4 bg-[#121212] border border-[#1A1A1A] rounded-lg hover:bg-[#1A1A1A] transition-colors cursor-pointer mb-2 shadow-sm">
      <span className="text-gray-300 font-bold">{dayName}</span>
      <div className="flex space-x-4">
        <span className="text-amber-500 font-bold">{calories} kcal</span>
        <span className="text-gray-500">{protein}g protein</span>
      </div>
    </div>
  );
};
