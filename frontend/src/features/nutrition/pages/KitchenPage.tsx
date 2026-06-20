import { useState } from 'react';
import { useDailyLog, useNutritionHistory } from '../api/nutrition';

import { LoadingState } from '../components/Shared/LoadingState';
import { ErrorState } from '../components/Shared/ErrorState';

import { EmptyNutritionState } from '../components/Kitchen/EmptyNutritionState';
import { NutritionSummaryCard } from '../components/Kitchen/NutritionSummaryCard';
import { LoggedEntryGroup } from '../components/Kitchen/LoggedEntryGroup';
import { PreviousLogRow } from '../components/Kitchen/PreviousLogRow';
import { AddLogInlinePanel } from '../components/Kitchen/AddLogInlinePanel';

// Helper to get local date in YYYY-MM-DD
const getTodayDateString = () => {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
};

export const KitchenPage = () => {
  const [todayDate] = useState(getTodayDateString);
  const { data: dailyLog, isLoading, isError } = useDailyLog(todayDate);
  const { data: historyLogs, isLoading: isHistoryLoading } = useNutritionHistory(8); // Fetch 8 to ensure we have 7 previous if today is included


  if (isLoading) {
    return <LoadingState />;
  }

  if (isError) {
    return <ErrorState message="Could not fetch today's nutrition log." />;
  }

  // Filter out orphaned/empty entries
  const validEntries = dailyLog?.entries.filter(entry => entry.items.length > 0) || [];
  const hasEntries = validEntries.length > 0;

  return (
    <div className="w-full pb-20">
      <h1 className="text-2xl font-black text-white mb-6 tracking-tight">Kitchen</h1>

      {/* SECTION 1 & 2: Summary and Logs */}
      {!hasEntries ? (
        <EmptyNutritionState />
      ) : (
        <>
          <NutritionSummaryCard log={dailyLog!} />
          <div className="mb-8">
            <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-4 px-2">Today's Log</h3>
            <div className="space-y-4 mb-8">
              {validEntries.map((entry) => (
                <LoggedEntryGroup key={entry.id} entry={entry} date={todayDate} />
              ))}
            </div>
          </div>
        </>
      )}

      {/* SECTION 3: Add To Today's Log */}
      <AddLogInlinePanel date={todayDate} />

      {/* SECTION 4: Previous Logs */}
      <div className="mt-8">
        <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-4 px-2">Previous Logs</h3>
        {isHistoryLoading ? (
          <div className="p-6 text-center text-gray-500 text-sm bg-[#161616] border border-[#2A2A2A] rounded-2xl animate-pulse">
            Loading history...
          </div>
        ) : historyLogs && historyLogs.filter(log => log.date !== todayDate).length > 0 ? (
          <div className="space-y-3">
            {historyLogs
              .filter(log => log.date !== todayDate)
              .slice(0, 7) // Only show up to 7 previous
              .map(log => (
                <PreviousLogRow key={log.date} log={log} />
              ))}
          </div>
        ) : (
          <div className="p-6 text-center text-gray-500 text-sm bg-[#161616] border border-[#2A2A2A] rounded-2xl">
            No previous logs found.
          </div>
        )}
      </div>
    </div>
  );
};
