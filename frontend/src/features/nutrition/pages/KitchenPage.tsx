import { useState } from 'react';
import { useDailyLog } from '../api/nutrition';

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

      {/* SECTION 4: Previous Logs (Placeholder UI) */}
      <div className="mt-8">
        <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-4 px-2">Previous Logs</h3>
        <PreviousLogRow dayName="Yesterday" calories={2600} protein={120} />
        <PreviousLogRow dayName="Monday" calories={2800} protein={130} />
        <PreviousLogRow dayName="Sunday" calories={2500} protein={115} />
      </div>
    </div>
  );
};
