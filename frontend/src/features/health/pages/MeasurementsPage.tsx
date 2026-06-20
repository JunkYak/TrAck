import { useState, useMemo } from 'react';
import { 
  useMeasurements, 
  useLatestMeasurement, 
  useLogMeasurement, 
  useUpdateMeasurement, 
  useDeleteMeasurement 
} from '../api/measurements';
import { MeasurementSessionRead } from '../types';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  Legend
} from 'recharts';

const getTodayDateString = () => {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
};

const MetricDisplay = ({ label, value }: { label: string, value: number | null }) => (
  <div className="flex flex-col">
    <span className="text-xs font-bold text-gray-500 uppercase tracking-wider">{label}</span>
    <div className="flex items-baseline gap-1">
      <span className="text-2xl font-black text-white">{value ?? '--'}</span>
      <span className="text-sm font-bold text-gray-500">in</span>
    </div>
  </div>
);

const CurrentMeasurementsCard = ({ latest }: { latest: MeasurementSessionRead | null }) => {
  if (!latest) {
    return (
      <div className="bg-[#161616] border border-[#2A2A2A] rounded-2xl p-6 flex flex-col items-center justify-center text-center h-full min-h-[160px]">
        <div className="w-12 h-12 bg-[#2A2A2A] rounded-full flex items-center justify-center mb-3">
          <span className="text-xl">📏</span>
        </div>
        <h3 className="text-lg font-bold text-white mb-1">No Measurements</h3>
        <p className="text-sm text-gray-500">Log your first session below.</p>
      </div>
    );
  }

  return (
    <div className="bg-gradient-to-br from-indigo-500/10 to-[#161616] border border-indigo-500/20 rounded-2xl p-6 relative overflow-hidden h-full">
      <div className="flex justify-between items-start mb-4 relative z-10">
        <h3 className="text-sm font-bold text-indigo-500 uppercase tracking-wider">Latest Session</h3>
        <span className="text-xs font-medium text-gray-500 bg-[#0A0A0A] px-2 py-1 rounded-md border border-[#2A2A2A]">
          {latest.date}
        </span>
      </div>
      <div className="flex justify-between items-end relative z-10">
        <MetricDisplay label="Waist" value={latest.waist_in} />
        <MetricDisplay label="Bicep" value={latest.bicep_in} />
        <MetricDisplay label="Quad" value={latest.quad_in} />
      </div>
      <div className="absolute right-[-10px] bottom-[-20px] text-[100px] opacity-[0.03] pointer-events-none">
        📏
      </div>
    </div>
  );
};

const ComparisonSection = ({ latest, previous }: { latest: MeasurementSessionRead, previous: MeasurementSessionRead }) => {
  const renderComparison = (label: string, cur: number | null, prev: number | null) => {
    if (cur === null || prev === null) return null;
    const diff = cur - prev;
    const isIncrease = diff > 0;
    const isZero = diff === 0;
    const color = isZero ? 'text-gray-500' : isIncrease ? 'text-red-400' : 'text-emerald-400';
    const sign = isIncrease ? '+' : '';

    return (
      <div className="bg-[#1A1A1A] border border-[#2A2A2A] rounded-xl p-4 flex flex-col">
        <span className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">{label}</span>
        <div className="flex items-center gap-2 mb-1">
          <span className="text-lg font-bold text-gray-400">{prev}</span>
          <span className="text-gray-600">→</span>
          <span className="text-lg font-bold text-white">{cur}</span>
        </div>
        <div className={`text-sm font-black ${color}`}>
          {sign}{diff.toFixed(1)} in
        </div>
      </div>
    );
  };

  return (
    <div className="mb-8">
      <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-4">Latest vs Previous Comparison</h3>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {renderComparison('Waist', latest.waist_in, previous.waist_in)}
        {renderComparison('Bicep', latest.bicep_in, previous.bicep_in)}
        {renderComparison('Quad', latest.quad_in, previous.quad_in)}
      </div>
    </div>
  );
};

const UpdateMeasurementsInline = () => {
  const logMutation = useLogMeasurement();
  const [waist, setWaist] = useState('');
  const [bicep, setBicep] = useState('');
  const [quad, setQuad] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const w = parseFloat(waist);
    const b = parseFloat(bicep);
    const q = parseFloat(quad);
    
    logMutation.mutate({
      date: getTodayDateString(),
      waist_in: isNaN(w) ? null : w,
      bicep_in: isNaN(b) ? null : b,
      quad_in: isNaN(q) ? null : q,
    }, {
      onSuccess: () => {
        setWaist('');
        setBicep('');
        setQuad('');
      }
    });
  };

  return (
    <div className="bg-[#1A1A1A] border border-[#2A2A2A] rounded-2xl p-6 h-full">
      <h4 className="text-sm font-bold text-white mb-1">Update Today's Measurements</h4>
      <p className="text-xs text-gray-500 mb-4">Replaces any existing entry for today.</p>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-3 gap-3">
          <div>
            <label className="block text-xs font-bold text-gray-500 mb-1">Waist</label>
            <input
              type="number" step="0.1" value={waist} onChange={e => setWaist(e.target.value)}
              placeholder="0.0" className="w-full bg-[#0A0A0A] text-white p-2 rounded-lg border border-[#2A2A2A] focus:border-indigo-500 outline-none text-center font-bold"
            />
          </div>
          <div>
            <label className="block text-xs font-bold text-gray-500 mb-1">Bicep</label>
            <input
              type="number" step="0.1" value={bicep} onChange={e => setBicep(e.target.value)}
              placeholder="0.0" className="w-full bg-[#0A0A0A] text-white p-2 rounded-lg border border-[#2A2A2A] focus:border-indigo-500 outline-none text-center font-bold"
            />
          </div>
          <div>
            <label className="block text-xs font-bold text-gray-500 mb-1">Quad</label>
            <input
              type="number" step="0.1" value={quad} onChange={e => setQuad(e.target.value)}
              placeholder="0.0" className="w-full bg-[#0A0A0A] text-white p-2 rounded-lg border border-[#2A2A2A] focus:border-indigo-500 outline-none text-center font-bold"
            />
          </div>
        </div>
        <button
          type="submit"
          disabled={logMutation.isPending || (!waist && !bicep && !quad)}
          className="w-full bg-indigo-500 hover:bg-indigo-400 disabled:opacity-50 text-white font-bold px-4 py-3 rounded-lg transition-colors"
        >
          {logMutation.isPending ? 'Saving...' : 'Save Measurements'}
        </button>
      </form>
    </div>
  );
};

export const MeasurementsPage = () => {
  const { data: latestMeasurement, isLoading: isLatestLoading } = useLatestMeasurement();
  const { data: allMeasurements, isLoading: isAllLoading } = useMeasurements(500, 0);
  const updateMutation = useUpdateMeasurement();
  const deleteMutation = useDeleteMeasurement();

  const [isExpanded, setIsExpanded] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editWaist, setEditWaist] = useState('');
  const [editBicep, setEditBicep] = useState('');
  const [editQuad, setEditQuad] = useState('');

  const handleEditClick = (entry: MeasurementSessionRead) => {
    setEditingId(entry.id);
    setEditWaist(entry.waist_in?.toString() || '');
    setEditBicep(entry.bicep_in?.toString() || '');
    setEditQuad(entry.quad_in?.toString() || '');
  };

  const handleSaveEdit = (id: string) => {
    const w = parseFloat(editWaist);
    const b = parseFloat(editBicep);
    const q = parseFloat(editQuad);
    
    updateMutation.mutate({ 
      id, 
      payload: { 
        waist_in: isNaN(w) ? null : w,
        bicep_in: isNaN(b) ? null : b,
        quad_in: isNaN(q) ? null : q,
      } 
    }, {
      onSuccess: () => setEditingId(null)
    });
  };

  const handleDelete = (id: string) => {
    if (window.confirm("Delete this measurement session?")) {
      deleteMutation.mutate(id);
    }
  };

  const chartData = useMemo(() => {
    if (!allMeasurements) return [];
    return [...allMeasurements].sort((a, b) => a.date.localeCompare(b.date)).map(m => ({
      date: m.date.substring(5),
      waist: m.waist_in,
      bicep: m.bicep_in,
      quad: m.quad_in
    }));
  }, [allMeasurements]);

  if (isLatestLoading || isAllLoading) {
    return (
      <div className="flex h-full items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-500"></div>
      </div>
    );
  }

  const historyToShow = isExpanded ? allMeasurements : allMeasurements?.slice(0, 4);

  return (
    <div className="max-w-3xl mx-auto pb-20">
      <h1 className="text-3xl font-black text-white mb-8 tracking-tight">Body Measurements</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <CurrentMeasurementsCard latest={latestMeasurement || null} />
        <UpdateMeasurementsInline />
      </div>

      {allMeasurements && allMeasurements.length >= 2 && (
        <ComparisonSection latest={allMeasurements[0]} previous={allMeasurements[1]} />
      )}

      <div className="mb-10">
        <div className="flex justify-between items-end mb-4">
          <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider">Recent History</h3>
          {allMeasurements && allMeasurements.length > 4 && (
            <button 
              onClick={() => setIsExpanded(!isExpanded)}
              className="text-indigo-500 text-sm font-bold hover:text-indigo-400 transition-colors"
            >
              {isExpanded ? 'Show Less' : 'View Full History'}
            </button>
          )}
        </div>

        <div className="bg-[#161616] border border-[#2A2A2A] rounded-2xl overflow-hidden">
          {!allMeasurements || allMeasurements.length === 0 ? (
            <div className="p-6 text-center text-gray-500 text-sm">No history available.</div>
          ) : (
            <div className="divide-y divide-[#2A2A2A]">
              {historyToShow?.map((entry: MeasurementSessionRead) => (
                <div key={entry.id} className="p-4 flex flex-col md:flex-row md:items-center justify-between hover:bg-[#1A1A1A] transition-colors group gap-4">
                  <div className="font-medium text-gray-300 w-32 shrink-0">
                    {new Date(entry.date + 'T00:00:00').toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric' })}
                  </div>
                  
                  {editingId === entry.id ? (
                    <div className="flex-1 flex items-center justify-end gap-2 flex-wrap">
                      <input type="number" step="0.1" placeholder="Waist" value={editWaist} onChange={e => setEditWaist(e.target.value)} className="w-16 bg-[#0A0A0A] text-white p-1 rounded border border-indigo-500 outline-none text-center text-sm" />
                      <input type="number" step="0.1" placeholder="Bicep" value={editBicep} onChange={e => setEditBicep(e.target.value)} className="w-16 bg-[#0A0A0A] text-white p-1 rounded border border-indigo-500 outline-none text-center text-sm" />
                      <input type="number" step="0.1" placeholder="Quad" value={editQuad} onChange={e => setEditQuad(e.target.value)} className="w-16 bg-[#0A0A0A] text-white p-1 rounded border border-indigo-500 outline-none text-center text-sm" />
                      <button onClick={() => handleSaveEdit(entry.id)} className="text-emerald-500 font-bold text-sm px-2">Save</button>
                      <button onClick={() => setEditingId(null)} className="text-gray-500 font-bold text-sm px-2">Cancel</button>
                    </div>
                  ) : (
                    <div className="flex-1 flex items-center justify-between">
                      <div className="flex gap-6 text-sm">
                        <div className="flex flex-col"><span className="text-gray-500 text-[10px] uppercase">Waist</span><span className="font-bold text-white">{entry.waist_in ?? '-'}</span></div>
                        <div className="flex flex-col"><span className="text-gray-500 text-[10px] uppercase">Bicep</span><span className="font-bold text-white">{entry.bicep_in ?? '-'}</span></div>
                        <div className="flex flex-col"><span className="text-gray-500 text-[10px] uppercase">Quad</span><span className="font-bold text-white">{entry.quad_in ?? '-'}</span></div>
                      </div>
                      
                      <div className="opacity-0 group-hover:opacity-100 transition-opacity flex gap-2">
                        <button onClick={() => handleEditClick(entry)} className="p-1.5 text-gray-500 hover:text-indigo-500 hover:bg-[#2A2A2A] rounded-md transition-colors" title="Edit">
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor"><path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" /></svg>
                        </button>
                        <button onClick={() => handleDelete(entry.id)} className="p-1.5 text-gray-500 hover:text-red-500 hover:bg-[#2A2A2A] rounded-md transition-colors" title="Delete">
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor"><path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" /></svg>
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

      {chartData.length > 1 && (
        <div className="bg-[#161616] border border-[#2A2A2A] rounded-2xl p-6">
          <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-6">Trend Overview</h3>
          <div style={{ width: '100%', height: 300 }}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData} margin={{ top: 5, right: 10, left: -20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#2A2A2A" vertical={false} />
                <XAxis dataKey="date" stroke="#555" tick={{ fill: '#888', fontSize: 12 }} tickLine={false} axisLine={false} dy={10} />
                <YAxis stroke="#555" tick={{ fill: '#888', fontSize: 12 }} tickLine={false} axisLine={false} domain={['dataMin - 1', 'dataMax + 1']} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#1A1A1A', borderColor: '#2A2A2A', borderRadius: '8px', color: '#fff' }}
                  itemStyle={{ fontWeight: 'bold' }}
                  labelStyle={{ color: '#888', marginBottom: '4px' }}
                />
                <Legend iconType="circle" wrapperStyle={{ paddingTop: '20px' }} />
                <Line type="monotone" dataKey="waist" name="Waist" stroke="#6366F1" strokeWidth={3} dot={{ r: 3 }} activeDot={{ r: 6 }} />
                <Line type="monotone" dataKey="bicep" name="Bicep" stroke="#10B981" strokeWidth={3} dot={{ r: 3 }} activeDot={{ r: 6 }} />
                <Line type="monotone" dataKey="quad" name="Quad" stroke="#F59E0B" strokeWidth={3} dot={{ r: 3 }} activeDot={{ r: 6 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

    </div>
  );
};
