import { useState } from 'react';
import { 
  useCardioSessions, 
  useCreateCardioSession, 
  useUpdateCardioSession, 
  useDeleteCardioSession 
} from '../api/cardio';
import { RunType, CardioSessionRead } from '../types';
import { formatPace, formatRunType, formatDuration } from '../utils/format';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip as RechartsTooltip, CartesianGrid } from 'recharts';

const RunTypeBadge = ({ runType }: { runType: RunType }) => {
  const colors = {
    EASY: 'bg-emerald-500/10 text-emerald-500 border-emerald-500/20',
    TEMPO_INTERVAL: 'bg-amber-500/10 text-amber-500 border-amber-500/20',
    LONG: 'bg-indigo-500/10 text-indigo-500 border-indigo-500/20',
  };
  return (
    <span className={`px-2 py-1 rounded text-xs font-bold border ${colors[runType] || 'bg-gray-500/10 text-gray-400'}`}>
      {formatRunType(runType)}
    </span>
  );
};

export const CardioPage = () => {
  const { data: sessions, isLoading } = useCardioSessions(100);
  const createMutation = useCreateCardioSession();
  const updateMutation = useUpdateCardioSession();
  const deleteMutation = useDeleteCardioSession();

  const [date, setDate] = useState(() => new Date().toISOString().split('T')[0]);
  const [distance, setDistance] = useState('');
  const [duration, setDuration] = useState('');
  const [runType, setRunType] = useState<RunType>('EASY');
  const [notes, setNotes] = useState('');

  const [editingId, setEditingId] = useState<string | null>(null);
  const [showFullHistory, setShowFullHistory] = useState(false);

  const handleCreate = (e: React.FormEvent) => {
    e.preventDefault();
    const dist = parseFloat(distance);
    const dur = parseFloat(duration);
    if (isNaN(dist) || isNaN(dur) || dist <= 0 || dur <= 0) return;

    createMutation.mutate({
      performed_at: new Date(date).toISOString(),
      distance_km: dist,
      duration_minutes: dur,
      run_type: runType,
      notes: notes || undefined,
    }, {
      onSuccess: () => {
        setDistance('');
        setDuration('');
        setNotes('');
        setRunType('EASY');
      }
    });
  };

  const handleSaveEdit = (e: React.FormEvent, session: CardioSessionRead) => {
    e.preventDefault();
    const dist = parseFloat(distance);
    const dur = parseFloat(duration);
    if (isNaN(dist) || isNaN(dur) || dist <= 0 || dur <= 0) return;

    updateMutation.mutate({
      id: session.id,
      payload: {
        performed_at: new Date(date).toISOString(),
        distance_km: dist,
        duration_minutes: dur,
        run_type: runType,
        notes: notes || undefined,
      }
    }, {
      onSuccess: () => {
        setEditingId(null);
        setDistance('');
        setDuration('');
        setNotes('');
        setRunType('EASY');
      }
    });
  };

  const startEdit = (session: CardioSessionRead) => {
    setEditingId(session.id);
    setDate(session.performed_at.split('T')[0]);
    setDistance(session.distance_km.toString());
    setDuration(session.duration_minutes.toString());
    setRunType(session.run_type);
    setNotes(session.notes || '');
  };

  const cancelEdit = () => {
    setEditingId(null);
    setDate(new Date().toISOString().split('T')[0]);
    setDistance('');
    setDuration('');
    setNotes('');
    setRunType('EASY');
  };

  if (isLoading) {
    return <div className="text-gray-500 p-8 text-center">Loading cardio data...</div>;
  }

  const latestSession = sessions && sessions.length > 0 ? sessions[0] : null;
  const recentHistory = sessions?.slice(0, 3) || [];
  const fullHistory = showFullHistory ? (sessions || []) : recentHistory;

  // Format data for chart (oldest to newest)
  const chartData = sessions?.slice().reverse().map(s => ({
    date: new Date(s.performed_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric' }),
    distance: s.distance_km,
    pace: s.average_pace,
  })) || [];

  return (
    <div className="max-w-4xl mx-auto pb-20 space-y-8">
      <h1 className="text-3xl font-black text-white tracking-tight">Cardio Tracking</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Left Column: Form & Latest Card */}
        <div className="space-y-8">
          {/* Latest Session Card */}
          <div>
            <h2 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-4">Latest Session</h2>
            {latestSession ? (
              <div className="bg-gradient-to-br from-cyan-500/10 to-[#161616] border border-cyan-500/20 rounded-2xl p-6">
                <div className="flex justify-between items-start mb-6">
                  <RunTypeBadge runType={latestSession.run_type} />
                  <span className="text-sm text-gray-400 font-bold bg-[#0A0A0A] px-2 py-1 rounded border border-[#2A2A2A]">
                    {new Date(latestSession.performed_at).toLocaleDateString()}
                  </span>
                </div>
                <div className="flex items-end justify-between">
                  <div>
                    <div className="flex items-baseline gap-1">
                      <span className="text-5xl font-black text-white">{latestSession.distance_km}</span>
                      <span className="text-xl font-bold text-cyan-500">km</span>
                    </div>
                    <div className="text-gray-400 font-bold mt-2 flex gap-4">
                      <span>⏱ {formatDuration(latestSession.duration_minutes)}</span>
                      <span>⚡ {formatPace(latestSession.average_pace)}</span>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="bg-[#161616] border border-[#2A2A2A] rounded-2xl p-6 text-center text-gray-500 h-40 flex items-center justify-center font-bold">
                No cardio logged yet.
              </div>
            )}
          </div>

          {/* Log New Session Form */}
          <div className="bg-[#161616] border border-[#2A2A2A] rounded-2xl p-6">
            <h2 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-6">Log New Session</h2>
            
            <form onSubmit={handleCreate} className="space-y-6">
              <div>
                <label className="block text-[10px] uppercase font-bold text-gray-500 mb-2">Run Type</label>
                <div className="flex bg-[#0A0A0A] p-1 rounded-lg border border-[#2A2A2A]">
                  {(['EASY', 'TEMPO_INTERVAL', 'LONG'] as RunType[]).map(type => (
                    <button
                      key={type}
                      type="button"
                      onClick={() => setRunType(type)}
                      className={`flex-1 py-2 rounded-md text-xs font-bold transition-all ${
                        runType === type 
                          ? 'bg-cyan-600 text-white shadow-md' 
                          : 'text-gray-500 hover:text-white hover:bg-[#2A2A2A]'
                      }`}
                    >
                      {formatRunType(type)}
                    </button>
                  ))}
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-[10px] uppercase font-bold text-gray-500 mb-1">Date</label>
                  <input 
                    type="date" required value={date} onChange={e => setDate(e.target.value)}
                    className="w-full bg-[#0A0A0A] text-white p-3 rounded-lg border border-[#2A2A2A] focus:border-cyan-500 outline-none font-bold"
                  />
                </div>
                <div>
                  <label className="block text-[10px] uppercase font-bold text-gray-500 mb-1">Distance (km)</label>
                  <input 
                    type="number" step="0.01" required value={distance} onChange={e => setDistance(e.target.value)} placeholder="5.0"
                    className="w-full bg-[#0A0A0A] text-white p-3 rounded-lg border border-[#2A2A2A] focus:border-cyan-500 outline-none font-bold text-center"
                  />
                </div>
              </div>

              <div>
                <label className="block text-[10px] uppercase font-bold text-gray-500 mb-1">Duration (minutes)</label>
                <input 
                  type="number" step="0.5" required value={duration} onChange={e => setDuration(e.target.value)} placeholder="30"
                  className="w-full bg-[#0A0A0A] text-white p-3 rounded-lg border border-[#2A2A2A] focus:border-cyan-500 outline-none font-bold text-center"
                />
              </div>

              <div>
                <label className="block text-[10px] uppercase font-bold text-gray-500 mb-1">Notes (Optional)</label>
                <textarea 
                  value={notes} onChange={e => setNotes(e.target.value)} placeholder="How did it feel?" rows={2}
                  className="w-full bg-[#0A0A0A] text-white p-3 rounded-lg border border-[#2A2A2A] focus:border-cyan-500 outline-none font-medium resize-none text-sm"
                />
              </div>

              <button 
                type="submit" 
                disabled={createMutation.isPending || !distance || !duration}
                className="w-full bg-cyan-600 hover:bg-cyan-500 disabled:opacity-50 text-white font-black py-4 rounded-xl transition-colors shadow-[0_4px_20px_rgba(8,145,178,0.3)]"
              >
                Save Cardio
              </button>
            </form>
          </div>
        </div>

        {/* Right Column: History & Trends */}
        <div className="space-y-8">
          
          {/* Trend Graph */}
          {chartData.length > 0 && (
            <div>
              <h2 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-4">Distance Trend (km)</h2>
              <div className="bg-[#161616] border border-[#2A2A2A] rounded-2xl p-6" style={{ height: 300 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#2A2A2A" vertical={false} />
                    <XAxis dataKey="date" stroke="#555" tick={{ fill: '#555', fontSize: 12 }} axisLine={false} tickLine={false} />
                    <YAxis stroke="#555" tick={{ fill: '#555', fontSize: 12 }} axisLine={false} tickLine={false} />
                    <RechartsTooltip 
                      contentStyle={{ backgroundColor: '#0A0A0A', borderColor: '#2A2A2A', borderRadius: '8px' }}
                      itemStyle={{ color: '#06b6d4', fontWeight: 'bold' }}
                    />
                    <Line type="monotone" dataKey="distance" stroke="#06b6d4" strokeWidth={3} dot={{ fill: '#06b6d4', r: 4 }} activeDot={{ r: 6, fill: '#fff' }} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}

          {/* History List */}
          <div>
            <h2 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-4">History</h2>
            <div className="bg-[#161616] border border-[#2A2A2A] rounded-2xl overflow-hidden">
              {fullHistory.length === 0 ? (
                <div className="p-6 text-center text-gray-500 text-sm">No history yet.</div>
              ) : (
                <div className="divide-y divide-[#2A2A2A]">
                  {fullHistory.map(session => (
                    <div key={session.id} className="p-5">
                      {editingId === session.id ? (
                        <form onSubmit={(e) => handleSaveEdit(e, session)} className="bg-[#0A0A0A] p-4 rounded-xl border border-cyan-500/30">
                          <div className="flex gap-2 mb-3">
                            <input type="date" required value={date} onChange={e => setDate(e.target.value)} className="w-1/3 bg-[#161616] text-xs text-white p-2 rounded outline-none border border-[#2A2A2A] focus:border-cyan-500"/>
                            <div className="flex flex-1 bg-[#161616] rounded border border-[#2A2A2A]">
                              {(['EASY', 'TEMPO_INTERVAL', 'LONG'] as RunType[]).map(type => (
                                <button key={type} type="button" onClick={() => setRunType(type)} className={`flex-1 text-[10px] font-bold ${runType === type ? 'bg-cyan-600 text-white' : 'text-gray-500'}`}>{formatRunType(type)}</button>
                              ))}
                            </div>
                          </div>
                          <div className="flex gap-2 mb-3">
                            <input type="number" step="0.01" required value={distance} onChange={e => setDistance(e.target.value)} placeholder="Dist" className="w-1/2 bg-[#161616] text-sm text-white p-2 rounded outline-none border border-[#2A2A2A] focus:border-cyan-500 text-center font-bold"/>
                            <input type="number" step="0.5" required value={duration} onChange={e => setDuration(e.target.value)} placeholder="Mins" className="w-1/2 bg-[#161616] text-sm text-white p-2 rounded outline-none border border-[#2A2A2A] focus:border-cyan-500 text-center font-bold"/>
                          </div>
                          <div className="flex gap-2">
                            <button type="submit" disabled={updateMutation.isPending} className="flex-1 bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-bold py-2 rounded">Save</button>
                            <button type="button" onClick={cancelEdit} className="px-4 bg-[#2A2A2A] hover:bg-[#333] text-white text-xs font-bold rounded">Cancel</button>
                          </div>
                        </form>
                      ) : (
                        <div>
                          <div className="flex justify-between items-start mb-2">
                            <div className="flex items-center gap-3">
                              <RunTypeBadge runType={session.run_type} />
                              <span className="text-white font-bold text-lg">{session.distance_km} km</span>
                            </div>
                            <span className="text-gray-500 text-xs font-bold">{new Date(session.performed_at).toLocaleDateString()}</span>
                          </div>
                          <div className="flex justify-between items-end">
                            <div className="text-gray-400 text-sm font-medium flex gap-3">
                              <span>⏱ {formatDuration(session.duration_minutes)}</span>
                              <span>⚡ {formatPace(session.average_pace)}</span>
                            </div>
                            <div className="flex gap-3 text-xs font-bold">
                              <button onClick={() => startEdit(session)} className="text-gray-500 hover:text-white transition-colors">Edit</button>
                              <button onClick={() => deleteMutation.mutate(session.id)} disabled={deleteMutation.isPending} className="text-gray-500 hover:text-red-500 transition-colors">Delete</button>
                            </div>
                          </div>
                          {session.notes && <p className="mt-3 text-gray-500 text-xs italic">"{session.notes}"</p>}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
              
              {sessions && sessions.length > 3 && (
                <button 
                  onClick={() => setShowFullHistory(!showFullHistory)}
                  className="w-full p-3 text-center text-xs font-bold text-gray-500 hover:bg-[#2A2A2A] transition-colors border-t border-[#2A2A2A] uppercase tracking-wider"
                >
                  {showFullHistory ? 'Collapse History' : 'View Full History'}
                </button>
              )}
            </div>
          </div>

        </div>
      </div>
    </div>
  );
};
