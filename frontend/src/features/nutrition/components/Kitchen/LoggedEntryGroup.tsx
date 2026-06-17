import { useState } from 'react';
import { DailyNutritionLogEntryRead } from '../../types';
import { LoggedItemRow } from './LoggedItemRow';

interface LoggedEntryGroupProps {
  entry: DailyNutritionLogEntryRead;
  date: string;
}

export const LoggedEntryGroup = ({ entry, date }: LoggedEntryGroupProps) => {
  const [isExpanded, setIsExpanded] = useState(true);

  // Distinguish visual styling based on entry type
  const getTypeBadgeColor = (type: string) => {
    switch (type) {
      case 'TEMPLATE': return 'text-purple-400 bg-purple-400/10 border-purple-400/20';
      case 'RECIPE': return 'text-blue-400 bg-blue-400/10 border-blue-400/20';
      case 'FOOD': return 'text-emerald-400 bg-emerald-400/10 border-emerald-400/20';
      default: return 'text-gray-400 bg-gray-400/10 border-gray-400/20';
    }
  };

  if (entry.entry_type === 'TEMPLATE') {
    return (
      <div className="mb-4">
        <div 
          className="flex items-center space-x-2 py-3 px-2 bg-[#1A1A1A] rounded-t-lg cursor-pointer border-b border-[#2A2A2A]"
          role="button"
          tabIndex={0}
          onClick={() => setIsExpanded(!isExpanded)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              e.preventDefault();
              setIsExpanded(!isExpanded);
            }
          }}
        >
          <svg 
            className={`w-4 h-4 text-gray-400 transition-transform ${isExpanded ? 'rotate-180' : ''}`} 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
          <span className="font-bold text-white tracking-tight">{entry.entry_name} Template</span>
          <span className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded border ${getTypeBadgeColor(entry.entry_type)}`}>
            {entry.entry_type}
          </span>
        </div>
        
        {isExpanded && (
          <div className="bg-[#0A0A0A] border-l border-r border-b border-[#1A1A1A] rounded-b-lg">
            {entry.items.map((item) => (
              <LoggedItemRow key={item.id} item={item} date={date} isIndented={true} />
            ))}
          </div>
        )}
      </div>
    );
  }

  // Non-template entries (Foods, Recipes, Custom)
  return (
    <div className="mb-4">
      <div className="flex items-center space-x-2 py-2 px-2">
        <span className="font-bold text-gray-300">{entry.entry_name}</span>
        <span className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded border ${getTypeBadgeColor(entry.entry_type)}`}>
          {entry.entry_type}
        </span>
      </div>
      <div className="bg-[#0A0A0A] rounded-lg border border-[#1A1A1A]">
        {entry.items.map((item) => (
          <LoggedItemRow key={item.id} item={item} date={date} isIndented={false} />
        ))}
      </div>
    </div>
  );
};
