import React from 'react';
import { LoadingState } from '../Shared/LoadingState';

interface SelectionListProps<T> {
  title: string;
  data?: T[];
  isLoading: boolean;
  isError: boolean;
  onSelect: (item: T) => void;
  renderItem: (item: T) => React.ReactNode;
}

export function SelectionList<T>({ title, data, isLoading, isError, onSelect, renderItem }: SelectionListProps<T>) {
  return (
    <div className="flex-1 flex flex-col bg-[#121212] border border-[#1A1A1A] rounded-xl overflow-hidden min-w-0">
      <div className="bg-[#1A1A1A] py-3 px-4 border-b border-[#2A2A2A]">
        <h3 className="text-xs font-bold text-gray-400 uppercase tracking-wider">{title}</h3>
      </div>
      <div className="flex-1 overflow-y-auto min-h-[200px] max-h-[300px]">
        {isLoading && (
          <div className="p-4">
            <LoadingState />
          </div>
        )}
        
        {isError && (
          <div className="p-4 text-sm text-red-500 font-medium text-center">
            Failed to load {title.toLowerCase()}
          </div>
        )}
        
        {!isLoading && !isError && (!data || data.length === 0) && (
          <div className="p-4 text-sm text-gray-500 text-center mt-4">
            No {title.toLowerCase()} found
          </div>
        )}
        
        {!isLoading && !isError && data && (
          <div className="flex flex-col">
            {data.map((item, idx) => (
              <div 
                key={idx} 
                className="p-4 border-b border-[#1A1A1A] hover:bg-[#1A1A1A] cursor-pointer transition-colors"
                role="button"
                tabIndex={0}
                onClick={() => onSelect(item)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    onSelect(item);
                  }
                }}
              >
                {renderItem(item)}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
