import { calculateTemplateMacros } from '../../utils/templateCalculations';
import { MealTemplateRead } from '../../types';

interface TemplateCardProps {
  template: MealTemplateRead;
  onClick: () => void;
  onDeleteClick: (e: React.MouseEvent) => void;
}

export const TemplateCard = ({ template, onClick, onDeleteClick }: TemplateCardProps) => {
  const { calories, protein } = calculateTemplateMacros(template);

  return (
    <div 
      onClick={onClick}
      className="bg-[#161616] border border-[#2A2A2A] rounded-2xl p-6 hover:border-amber-500 hover:-translate-y-1 hover:shadow-[0_8px_30px_rgb(0,0,0,0.5)] transition-all duration-300 cursor-pointer group relative overflow-hidden flex flex-col h-full"
    >
      <div className="flex justify-between items-start mb-6">
        <div className="pr-8">
          <h3 className="text-xl font-black text-white group-hover:text-amber-500 transition-colors leading-tight">
            {template.name}
          </h3>
          <p className="text-sm font-medium text-gray-500 mt-2">
            {template.foods.length} Foods • {template.recipes.length} Recipes
          </p>
        </div>
        
        {/* Delete Button - only visible on hover */}
        <button
          onClick={onDeleteClick}
          className="opacity-0 group-hover:opacity-100 p-2.5 text-gray-500 hover:text-red-500 hover:bg-[#2A2A2A] transition-all bg-[#1A1A1A] rounded-xl absolute top-5 right-5 z-10"
          title="Delete template"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
        </button>
      </div>

      <div className="mt-auto pt-6 border-t border-[#2A2A2A] group-hover:border-amber-500/30 transition-colors">
        <div className="flex flex-col gap-1">
          <div className="flex items-baseline gap-1.5">
            <span className="text-2xl font-black text-white">{Math.round(calories)}</span>
            <span className="text-sm font-bold text-gray-500 uppercase tracking-wider">kcal</span>
          </div>
          <div className="flex items-baseline gap-1.5">
            <span className="text-xl font-bold text-emerald-400">{Math.round(protein)}g</span>
            <span className="text-sm font-bold text-gray-500 uppercase tracking-wider">protein</span>
          </div>
        </div>
      </div>
      
      {/* Decorative gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-br from-amber-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none" />
    </div>
  );
};
