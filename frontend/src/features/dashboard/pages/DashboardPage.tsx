import { NavLink } from 'react-router-dom';
import { useLatestWeight } from '../../health/api/weight';
import { useLatestMeasurement } from '../../health/api/measurements';
import { useLatestExerciseLogs } from '../../training/api/exercises';
import { getStartOfWeekDate } from '../../training/utils/date';
import { useCardioSessions } from '../../training/api/cardio';
import { useDailyLog } from '../../nutrition/api/nutrition';
import { formatPace, formatRunType } from '../../training/utils/format';
import { useMemo } from 'react';

// Helper to get local date string (e.g. 2026-06-18)
const getTodayDateString = () => {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
};

const NutritionStatusCard = () => {
  const today = getTodayDateString();
  const { data: dailyLog, isLoading } = useDailyLog(today);

  const { totalCalories, totalProtein } = useMemo(() => {
    if (!dailyLog) return { totalCalories: 0, totalProtein: 0 };
    return dailyLog.entries.reduce(
      (acc, entry) => {
        entry.items.forEach((item) => {
          acc.totalCalories += item.calories;
          acc.totalProtein += item.protein;
        });
        return acc;
      },
      { totalCalories: 0, totalProtein: 0 }
    );
  }, [dailyLog]);

  if (isLoading) {
    return (
      <div className="bg-[#161616] border border-[#2A2A2A] rounded-2xl p-6 h-40 animate-pulse">
        <div className="h-4 w-24 bg-[#2A2A2A] rounded mb-4"></div>
        <div className="h-10 w-20 bg-[#2A2A2A] rounded"></div>
      </div>
    );
  }

  const hasData = totalCalories > 0;

  if (!hasData) {
    return (
      <NavLink 
        to="/nutrition/kitchen"
        className="block bg-[#161616] border border-[#2A2A2A] hover:border-orange-500 hover:shadow-[0_4px_20px_rgba(249,115,22,0.15)] rounded-2xl p-6 h-40 flex flex-col justify-between transition-all group"
      >
        <div className="flex justify-between items-center">
          <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider group-hover:text-orange-500 transition-colors">Nutrition</h3>
          <span className="text-xl opacity-50 group-hover:opacity-100 transition-opacity">🍎</span>
        </div>
        <div>
          <p className="text-2xl font-bold text-gray-500">No Nutrition Logged</p>
          <p className="text-xs text-orange-500 font-bold mt-1 opacity-0 group-hover:opacity-100 transition-opacity">Log meals →</p>
        </div>
      </NavLink>
    );
  }

  return (
    <NavLink 
      to="/nutrition/kitchen"
      className="block bg-gradient-to-br from-orange-500/10 to-[#161616] border border-orange-500/20 hover:border-orange-500 hover:shadow-[0_4px_20px_rgba(249,115,22,0.2)] rounded-2xl p-6 h-40 flex flex-col justify-between transition-all group relative overflow-hidden"
    >
      <div className="flex justify-between items-center relative z-10">
        <h3 className="text-sm font-bold text-orange-500 uppercase tracking-wider">Nutrition</h3>
        <span className="text-xs font-bold text-orange-500 bg-[#0A0A0A] px-2 py-1 rounded-md border border-[#2A2A2A]">
          Today's Log
        </span>
      </div>
      <div className="relative z-10">
        <div className="flex items-baseline gap-1">
          <span className="text-4xl font-black text-white">{Math.round(totalCalories)}</span>
          <span className="text-lg font-bold text-gray-400">kcal</span>
        </div>
        <div className="text-gray-400 font-bold flex gap-3 text-xs mt-1">
          <span>{Math.round(totalProtein)}g Protein</span>
        </div>
      </div>
      <div className="absolute right-[-10px] bottom-[-10px] text-[80px] opacity-10 pointer-events-none group-hover:scale-110 transition-transform">
        🍎
      </div>
    </NavLink>
  );
};

const WeightStatusCard = () => {
  const { data: latestWeight, isLoading } = useLatestWeight();

  if (isLoading) {
    return (
      <div className="bg-[#161616] border border-[#2A2A2A] rounded-2xl p-6 h-40 animate-pulse">
        <div className="h-4 w-24 bg-[#2A2A2A] rounded mb-4"></div>
        <div className="h-10 w-20 bg-[#2A2A2A] rounded"></div>
      </div>
    );
  }

  if (!latestWeight) {
    return (
      <NavLink 
        to="/health/weight"
        className="block bg-[#161616] border border-[#2A2A2A] hover:border-amber-500 hover:shadow-[0_4px_20px_rgba(245,158,11,0.15)] rounded-2xl p-6 h-40 flex flex-col justify-between transition-all group"
      >
        <div className="flex justify-between items-center">
          <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider group-hover:text-amber-500 transition-colors">Weight</h3>
          <span className="text-xl opacity-50 group-hover:opacity-100 transition-opacity">⚖️</span>
        </div>
        <div>
          <p className="text-2xl font-bold text-gray-500">No data</p>
          <p className="text-xs text-amber-500 font-bold mt-1 opacity-0 group-hover:opacity-100 transition-opacity">Log your weight →</p>
        </div>
      </NavLink>
    );
  }

  return (
    <NavLink 
      to="/health/weight"
      className="block bg-gradient-to-br from-amber-500/10 to-[#161616] border border-amber-500/20 hover:border-amber-500 hover:shadow-[0_4px_20px_rgba(245,158,11,0.2)] rounded-2xl p-6 h-40 flex flex-col justify-between transition-all group relative overflow-hidden"
    >
      <div className="flex justify-between items-center relative z-10">
        <h3 className="text-sm font-bold text-amber-500 uppercase tracking-wider">Weight</h3>
        <span className="text-xs font-bold text-amber-500 bg-[#0A0A0A] px-2 py-1 rounded-md border border-[#2A2A2A]">
          Updated {new Date(latestWeight.date).toDateString() === new Date().toDateString() ? 'Today' : latestWeight.date}
        </span>
      </div>
      <div className="relative z-10">
        <div className="flex items-baseline gap-1">
          <span className="text-4xl font-black text-white">{latestWeight.weight_kg}</span>
          <span className="text-lg font-bold text-gray-400">kg</span>
        </div>
      </div>
      <div className="absolute right-[-10px] bottom-[-10px] text-[80px] opacity-10 pointer-events-none group-hover:scale-110 transition-transform">
        ⚖️
      </div>
    </NavLink>
  );
};

const MeasurementStatusCard = () => {
  const { data: latestMeasurement, isLoading } = useLatestMeasurement();

  if (isLoading) {
    return (
      <div className="bg-[#161616] border border-[#2A2A2A] rounded-2xl p-6 h-40 animate-pulse">
        <div className="h-4 w-24 bg-[#2A2A2A] rounded mb-4"></div>
        <div className="h-10 w-20 bg-[#2A2A2A] rounded"></div>
      </div>
    );
  }

  if (!latestMeasurement) {
    return (
      <NavLink 
        to="/health/measurements"
        className="block bg-[#161616] border border-[#2A2A2A] hover:border-indigo-500 hover:shadow-[0_4px_20px_rgba(99,102,241,0.15)] rounded-2xl p-6 h-40 flex flex-col justify-between transition-all group"
      >
        <div className="flex justify-between items-center">
          <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider group-hover:text-indigo-500 transition-colors">Measurements</h3>
          <span className="text-xl opacity-50 group-hover:opacity-100 transition-opacity">📏</span>
        </div>
        <div>
          <p className="text-2xl font-bold text-gray-500">No data</p>
          <p className="text-xs text-indigo-500 font-bold mt-1 opacity-0 group-hover:opacity-100 transition-opacity">Log measurements →</p>
        </div>
      </NavLink>
    );
  }

  return (
    <NavLink 
      to="/health/measurements"
      className="block bg-gradient-to-br from-indigo-500/10 to-[#161616] border border-indigo-500/20 hover:border-indigo-500 hover:shadow-[0_4px_20px_rgba(99,102,241,0.2)] rounded-2xl p-6 h-40 flex flex-col justify-between transition-all group relative overflow-hidden"
    >
      <div className="flex justify-between items-center relative z-10">
        <h3 className="text-sm font-bold text-indigo-500 uppercase tracking-wider">Measurements</h3>
        <span className="text-xs font-bold text-indigo-500 bg-[#0A0A0A] px-2 py-1 rounded-md border border-[#2A2A2A]">
          Updated This Week
        </span>
      </div>
      <div className="relative z-10 mt-2">
        <div className="flex gap-4">
          <div className="flex flex-col">
            <span className="text-[10px] text-gray-500 uppercase font-bold">Waist</span>
            <span className="font-black text-white text-xl">{latestMeasurement.waist_in ?? '-'}</span>
          </div>
          <div className="flex flex-col">
            <span className="text-[10px] text-gray-500 uppercase font-bold">Bicep</span>
            <span className="font-black text-white text-xl">{latestMeasurement.bicep_in ?? '-'}</span>
          </div>
          <div className="flex flex-col">
            <span className="text-[10px] text-gray-500 uppercase font-bold">Quad</span>
            <span className="font-black text-white text-xl">{latestMeasurement.quad_in ?? '-'}</span>
          </div>
        </div>
      </div>
      <div className="absolute right-[-10px] bottom-[-10px] text-[80px] opacity-10 pointer-events-none group-hover:scale-110 transition-transform">
        📏
      </div>
    </NavLink>
  );
};

const TrainingStatusCard = () => {
  const { data: latestLogs, isLoading } = useLatestExerciseLogs();
  
  if (isLoading) {
    return (
      <div className="bg-[#161616] border border-[#2A2A2A] rounded-2xl p-6 h-40 animate-pulse">
        <div className="h-4 w-24 bg-[#2A2A2A] rounded mb-4"></div>
        <div className="h-10 w-20 bg-[#2A2A2A] rounded"></div>
      </div>
    );
  }

  const currentWeekDate = getStartOfWeekDate();
  const logsThisWeek = latestLogs?.filter(log => log.log_date === currentWeekDate) || [];
  const count = logsThisWeek.length;

  if (count === 0) {
    return (
      <NavLink 
        to="/training/exercises"
        className="block bg-[#161616] border border-[#2A2A2A] hover:border-emerald-500 hover:shadow-[0_4px_20px_rgba(16,185,129,0.15)] rounded-2xl p-6 h-40 flex flex-col justify-between transition-all group"
      >
        <div className="flex justify-between items-center">
          <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider group-hover:text-emerald-500 transition-colors">Strength</h3>
          <span className="text-xl opacity-50 group-hover:opacity-100 transition-opacity">💪</span>
        </div>
        <div>
          <p className="text-2xl font-bold text-gray-500">0 tracked</p>
          <p className="text-xs text-emerald-500 font-bold mt-1 opacity-0 group-hover:opacity-100 transition-opacity">Log weekly best sets →</p>
        </div>
      </NavLink>
    );
  }

  return (
    <NavLink 
      to="/training/exercises"
      className="block bg-gradient-to-br from-emerald-500/10 to-[#161616] border border-emerald-500/20 hover:border-emerald-500 hover:shadow-[0_4px_20px_rgba(16,185,129,0.2)] rounded-2xl p-6 h-40 flex flex-col justify-between transition-all group relative overflow-hidden"
    >
      <div className="flex justify-between items-center relative z-10">
        <h3 className="text-sm font-bold text-emerald-500 uppercase tracking-wider">Strength</h3>
        <span className="text-xs font-bold text-emerald-500 bg-[#0A0A0A] px-2 py-1 rounded-md border border-[#2A2A2A]">
          This Week
        </span>
      </div>
      <div className="relative z-10">
        <div className="flex items-baseline gap-1">
          <span className="text-4xl font-black text-white">{count}</span>
          <span className="text-lg font-bold text-gray-400">exercises</span>
        </div>
      </div>
      <div className="absolute right-[-10px] bottom-[-10px] text-[80px] opacity-10 pointer-events-none group-hover:scale-110 transition-transform">
        💪
      </div>
    </NavLink>
  );
};

const CardioStatusCard = () => {
  const { data: sessions, isLoading } = useCardioSessions(1);

  if (isLoading) {
    return (
      <div className="bg-[#161616] border border-[#2A2A2A] rounded-2xl p-6 h-40 animate-pulse">
        <div className="h-4 w-24 bg-[#2A2A2A] rounded mb-4"></div>
        <div className="h-10 w-20 bg-[#2A2A2A] rounded"></div>
      </div>
    );
  }

  const latestSession = sessions && sessions.length > 0 ? sessions[0] : null;

  if (!latestSession) {
    return (
      <NavLink 
        to="/training/cardio"
        className="block bg-[#161616] border border-[#2A2A2A] hover:border-cyan-500 hover:shadow-[0_4px_20px_rgba(6,182,212,0.15)] rounded-2xl p-6 h-40 flex flex-col justify-between transition-all group"
      >
        <div className="flex justify-between items-center">
          <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider group-hover:text-cyan-500 transition-colors">Cardio</h3>
          <span className="text-xl opacity-50 group-hover:opacity-100 transition-opacity">🏃</span>
        </div>
        <div>
          <p className="text-2xl font-bold text-gray-500">No Cardio Logged</p>
          <p className="text-xs text-cyan-500 font-bold mt-1 opacity-0 group-hover:opacity-100 transition-opacity">Log a session →</p>
        </div>
      </NavLink>
    );
  }

  return (
    <NavLink 
      to="/training/cardio"
      className="block bg-gradient-to-br from-cyan-500/10 to-[#161616] border border-cyan-500/20 hover:border-cyan-500 hover:shadow-[0_4px_20px_rgba(6,182,212,0.2)] rounded-2xl p-6 h-40 flex flex-col justify-between transition-all group relative overflow-hidden"
    >
      <div className="flex justify-between items-center relative z-10">
        <h3 className="text-sm font-bold text-cyan-500 uppercase tracking-wider">Cardio</h3>
        <span className="text-xs font-bold text-cyan-500 bg-[#0A0A0A] px-2 py-1 rounded-md border border-[#2A2A2A]">
          {formatRunType(latestSession.run_type)}
        </span>
      </div>
      <div className="relative z-10">
        <div className="flex items-baseline gap-1">
          <span className="text-4xl font-black text-white">{latestSession.distance_km}</span>
          <span className="text-lg font-bold text-gray-400">km</span>
        </div>
        <div className="text-gray-400 font-bold flex gap-3 text-xs mt-1">
          <span>{formatPace(latestSession.average_pace)}</span>
        </div>
      </div>
      <div className="absolute right-[-10px] bottom-[-10px] text-[80px] opacity-10 pointer-events-none group-hover:scale-110 transition-transform">
        🏃
      </div>
    </NavLink>
  );
};

export const DashboardPage = () => {
  return (
    <div className="w-full pb-20">
      <h1 className="text-3xl font-black text-white mb-8 tracking-tight">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <NutritionStatusCard />
        <WeightStatusCard />
        <MeasurementStatusCard />
        <TrainingStatusCard />
        <CardioStatusCard />
      </div>
    </div>
  );
};
