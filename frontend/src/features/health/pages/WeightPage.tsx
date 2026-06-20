import { useState, useMemo } from 'react';
import { 
  useWeights, 
  useLatestWeight, 
  useLogWeight, 
  useUpdateWeight, 
  useDeleteWeight 
} from '../api/weight';
import { WeightLogRead } from '../types';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer 
} from 'recharts';

const getTodayDateString = () => {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
};

// --- Subcomponents ---

const CurrentWeightCard = ({ latestWeight }: { latestWeight: WeightLogRead | null }) => {
  if (!latestWeight) {
    return (
      <div className="bg-[#161616] border border-[#2A2A2A] rounded-2xl p-6 flex flex-col items-center justify-center text-center h-48">
        <div className="w-12 h-12 bg-[#2A2A2A] rounded-full flex items-center justify-center mb-3">
          <span className="text-xl">⚖️</span>
        </div>
        <h3 className="text-lg font-bold text-white mb-1">No Weight Logged</h3>
        <p className="text-sm text-gray-500">Log your first weight entry below.</p>
      </div>
    );
  }

  return (
    <div className="bg-gradient-to-br from-amber-500/10 to-[#161616] border border-amber-500/20 rounded-2xl p-6 relative overflow-hidden">
      <div className="flex justify-between items-start mb-2 relative z-10">
        <h3 className="text-sm font-bold text-amber-500 uppercase tracking-wider">Current Weight</h3>
        <span className="text-xs font-medium text-gray-500 bg-[#0A0A0A] px-2 py-1 rounded-md border border-[#2A2A2A]">
          {latestWeight.date}
        </span>
      </div>
      <div className="flex items-baseline gap-1 relative z-10">
        <span className="text-5xl font-black text-white">{latestWeight.weight_kg}</span>
        <span className="text-xl font-bold text-gray-400">kg</span>
      </div>
      <div className="absolute right-[-20px] bottom-[-20px] text-[120px] opacity-5 pointer-events-none">
        ⚖️
      </div>
    </div>
  );
};

const UpdateWeightInline = () => {
  const logMutation = useLogWeight();
  const [weight, setWeight] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const val = parseFloat(weight);
    if (!isNaN(val) && val > 0) {
      logMutation.mutate({
        date: getTodayDateString(),
        weight_kg: val
      }, {
        onSuccess: () => setWeight('')
      });
    }
  };

  return (
    <div className="bg-[#1A1A1A] border border-[#2A2A2A] rounded-xl p-4 flex items-center justify-between">
      <div>
        <h4 className="text-sm font-bold text-white mb-1">Update Today's Weight</h4>
        <p className="text-xs text-gray-500">Replaces existing entry for today.</p>
      </div>
      <form onSubmit={handleSubmit} className="flex gap-2">
        <div className="relative">
          <input
            type="number"
            step="0.1"
            value={weight}
            onChange={(e) => setWeight(e.target.value)}
            placeholder="0.0"
            className="w-24 bg-[#0A0A0A] text-white p-2 pl-3 pr-8 rounded-lg border border-[#2A2A2A] focus:border-amber-500 outline-none text-right font-bold"
            required
            min="0.1"
          />
          <span className="absolute right-3 top-2.5 text-xs font-bold text-gray-500 pointer-events-none">kg</span>
        </div>
        <button
          type="submit"
          disabled={logMutation.isPending || !weight}
          className="bg-amber-500 hover:bg-amber-400 disabled:opacity-50 text-black font-bold px-4 py-2 rounded-lg transition-colors"
        >
          {logMutation.isPending ? '...' : 'Save'}
        </button>
      </form>
    </div>
  );
};

// --- Main Page ---

export const WeightPage = () => {
  const { data: latestWeight, isLoading: isLatestLoading } = useLatestWeight();
  const { data: allWeights, isLoading: isAllLoading } = useWeights(500, 0); // Fetch all for graph
  const updateMutation = useUpdateWeight();
  const deleteMutation = useDeleteWeight();

  const [isExpanded, setIsExpanded] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editVal, setEditVal] = useState('');

  const handleEditClick = (entry: WeightLogRead) => {
    setEditingId(entry.id);
    setEditVal(entry.weight_kg.toString());
  };

  const handleSaveEdit = (id: string) => {
    const val = parseFloat(editVal);
    if (!isNaN(val) && val > 0) {
      updateMutation.mutate({ id, payload: { weight_kg: val } }, {
        onSuccess: () => setEditingId(null)
      });
    }
  };

  const handleDelete = (id: string) => {
    if (window.confirm("Delete this weight entry?")) {
      deleteMutation.mutate(id);
    }
  };

  const chartData = useMemo(() => {
    if (!allWeights) return [];
    // Sort oldest first for left-to-right graph
    return [...allWeights].sort((a, b) => a.date.localeCompare(b.date)).map(w => ({
      date: w.date.substring(5), // MM-DD
      weight: w.weight_kg
    }));
  }, [allWeights]);

  if (isLatestLoading || isAllLoading) {
    return (
      <div className="flex h-full items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-amber-500"></div>
      </div>
    );
  }

  const historyToShow = isExpanded ? allWeights : allWeights?.slice(0, 4);

  return (
    <div className="max-w-2xl mx-auto pb-20">
      <h1 className="text-3xl font-black text-white mb-8 tracking-tight">Weight Tracking</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <CurrentWeightCard latestWeight={latestWeight || null} />
        <div className="flex flex-col justify-center">
          <UpdateWeightInline />
        </div>
      </div>

      <div className="mb-10">
        <div className="flex justify-between items-end mb-4">
          <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider">Recent History</h3>
          {allWeights && allWeights.length > 4 && (
            <button 
              onClick={() => setIsExpanded(!isExpanded)}
              className="text-amber-500 text-sm font-bold hover:text-amber-400 transition-colors"
            >
              {isExpanded ? 'Show Less' : 'View Full History'}
            </button>
          )}
        </div>

        <div className="bg-[#161616] border border-[#2A2A2A] rounded-2xl overflow-hidden">
          {!allWeights || allWeights.length === 0 ? (
            <div className="p-6 text-center text-gray-500 text-sm">No history available.</div>
          ) : (
            <div className="divide-y divide-[#2A2A2A]">
              {historyToShow?.map((entry: WeightLogRead) => (
                <div key={entry.id} className="p-4 flex items-center justify-between hover:bg-[#1A1A1A] transition-colors group">
                  <div className="font-medium text-gray-300">
                    {new Date(entry.date + 'T00:00:00').toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric' })}
                  </div>
                  
                  {editingId === entry.id ? (
                    <div className="flex items-center gap-2">
                      <input 
                        type="number"
                        step="0.1"
                        value={editVal}
                        onChange={e => setEditVal(e.target.value)}
                        className="w-20 bg-[#0A0A0A] text-white p-1 rounded border border-amber-500 outline-none text-right"
                        autoFocus
                      />
                      <button onClick={() => handleSaveEdit(entry.id)} className="text-emerald-500 font-bold text-sm px-2">Save</button>
                      <button onClick={() => setEditingId(null)} className="text-gray-500 font-bold text-sm px-2">Cancel</button>
                    </div>
                  ) : (
                    <div className="flex items-center gap-4">
                      <div className="font-bold text-white text-lg">{entry.weight_kg} <span className="text-sm text-gray-500 font-normal">kg</span></div>
                      
                      <div className="opacity-0 group-hover:opacity-100 transition-opacity flex gap-2">
                        <button onClick={() => handleEditClick(entry)} className="p-1.5 text-gray-500 hover:text-amber-500 hover:bg-[#2A2A2A] rounded-md transition-colors" title="Edit">
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                            <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                          </svg>
                        </button>
                        <button onClick={() => handleDelete(entry.id)} className="p-1.5 text-gray-500 hover:text-red-500 hover:bg-[#2A2A2A] rounded-md transition-colors" title="Delete">
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                          </svg>
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Trend Graph */}
      {chartData.length > 1 && (
        <div className="bg-[#161616] border border-[#2A2A2A] rounded-2xl p-6">
          <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-6">Weight Trend</h3>
          <div style={{ width: '100%', height: 300 }}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData} margin={{ top: 5, right: 10, left: -20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#2A2A2A" vertical={false} />
                <XAxis 
                  dataKey="date" 
                  stroke="#555" 
                  tick={{ fill: '#888', fontSize: 12 }} 
                  tickLine={false}
                  axisLine={false}
                  dy={10}
                />
                <YAxis 
                  stroke="#555" 
                  tick={{ fill: '#888', fontSize: 12 }} 
                  tickLine={false}
                  axisLine={false}
                  domain={['dataMin - 1', 'dataMax + 1']}
                  tickFormatter={(val) => val.toFixed(1)}
                />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#1A1A1A', borderColor: '#2A2A2A', borderRadius: '8px', color: '#fff' }}
                  itemStyle={{ color: '#F59E0B', fontWeight: 'bold' }}
                  formatter={(value: any) => [`${value} kg`, 'Weight']}
                  labelStyle={{ color: '#888', marginBottom: '4px' }}
                />
                <Line 
                  type="monotone" 
                  dataKey="weight" 
                  stroke="#F59E0B" 
                  strokeWidth={3}
                  dot={{ fill: '#F59E0B', strokeWidth: 2, r: 4, stroke: '#0A0A0A' }}
                  activeDot={{ r: 6, fill: '#F59E0B', stroke: '#fff', strokeWidth: 2 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

    </div>
  );
};
