import { useState } from 'react';
import { 
  useExercises, useCreateExercise, useUpdateExercise, 
  useArchiveExercise, useRestoreExercise, useExerciseLogs, 
  useLogBestSet, useUpdateBestSet 
} from '../api/exercises';
import { getStartOfWeekDate, getWeekNumber } from '../utils/date';
import { ExerciseRead } from '../types';

const ExerciseLogTracker = ({ exercise }: { exercise: ExerciseRead }) => {
  const { data: logs, isLoading } = useExerciseLogs(exercise.id);
  const logMutation = useLogBestSet(exercise.id);
  const updateMutation = useUpdateBestSet();
  
  const [weight, setWeight] = useState('');
  const [reps, setReps] = useState('');
  const [isEditingExercise, setIsEditingExercise] = useState(false);
  const [editName, setEditName] = useState(exercise.name);
  
  const updateExerciseMutation = useUpdateExercise();
  const archiveMutation = useArchiveExercise();
  const restoreMutation = useRestoreExercise();

  const handleSaveExerciseName = () => {
    if (editName.trim() && editName !== exercise.name) {
      updateExerciseMutation.mutate({ id: exercise.id, payload: { name: editName } });
    }
    setIsEditingExercise(false);
  };

  const currentWeekDate = getStartOfWeekDate();
  
  const currentWeekLog = logs?.find(log => log.log_date === currentWeekDate);
  const historicalLogs = logs?.filter(log => log.log_date !== currentWeekDate).sort((a, b) => b.log_date.localeCompare(a.log_date)) || [];

  const handleSaveSet = (e: React.FormEvent) => {
    e.preventDefault();
    const w = parseFloat(weight);
    const r = parseInt(reps, 10);
    if (isNaN(w) || isNaN(r)) return;

    if (currentWeekLog) {
      updateMutation.mutate({ 
        id: currentWeekLog.id, 
        payload: { weight_kg: w, reps: r } 
      }, {
        onSuccess: () => { setWeight(''); setReps(''); }
      });
    } else {
      logMutation.mutate({ 
        log_date: currentWeekDate, 
        weight_kg: w, 
        reps: r 
      }, {
        onSuccess: () => { setWeight(''); setReps(''); }
      });
    }
  };

  if (isLoading) return <div className="p-4 border border-[#2A2A2A] rounded-xl animate-pulse bg-[#161616] h-32"></div>;

  return (
    <div className={`bg-[#161616] border border-[#2A2A2A] rounded-xl p-5 mb-4 transition-opacity ${exercise.is_archived ? 'opacity-50' : ''}`}>
      <div className="flex justify-between items-center mb-4 border-b border-[#2A2A2A] pb-3">
        {isEditingExercise ? (
          <div className="flex gap-2 items-center flex-1 mr-4">
            <input 
              type="text" value={editName} onChange={e => setEditName(e.target.value)}
              className="bg-[#0A0A0A] text-white px-3 py-1 rounded border border-indigo-500 outline-none flex-1 font-bold"
              autoFocus
            />
            <button onClick={handleSaveExerciseName} className="text-emerald-500 font-bold text-sm px-2">Save</button>
            <button onClick={() => { setIsEditingExercise(false); setEditName(exercise.name); }} className="text-gray-500 font-bold text-sm px-2">Cancel</button>
          </div>
        ) : (
          <h3 className="text-xl font-bold text-white flex-1">{exercise.name}</h3>
        )}

        <div className="flex items-center gap-2">
          {!isEditingExercise && !exercise.is_archived && (
            <button onClick={() => setIsEditingExercise(true)} className="text-gray-500 hover:text-indigo-500 text-sm font-bold transition-colors">Edit</button>
          )}
          {exercise.is_archived ? (
            <button onClick={() => restoreMutation.mutate(exercise.id)} className="text-gray-500 hover:text-emerald-500 text-sm font-bold transition-colors">Restore</button>
          ) : (
            <button onClick={() => archiveMutation.mutate(exercise.id)} className="text-gray-500 hover:text-red-500 text-sm font-bold transition-colors">Archive</button>
          )}
        </div>
      </div>

      {!exercise.is_archived && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <h4 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3">
              Current Week ({getWeekNumber(currentWeekDate)})
            </h4>
            
            {currentWeekLog && !weight && !reps ? (
              <div className="bg-indigo-500/10 border border-indigo-500/20 rounded-lg p-4 flex justify-between items-center group">
                <div className="flex items-baseline gap-2">
                  <span className="text-2xl font-black text-white">{currentWeekLog.weight_kg}kg</span>
                  <span className="text-gray-400 font-bold">x</span>
                  <span className="text-2xl font-black text-white">{currentWeekLog.reps}</span>
                </div>
                <button 
                  onClick={() => { setWeight(currentWeekLog.weight_kg.toString()); setReps(currentWeekLog.reps.toString()); }}
                  className="text-indigo-500 text-sm font-bold opacity-0 group-hover:opacity-100 transition-opacity"
                >
                  Update
                </button>
              </div>
            ) : (
              <form onSubmit={handleSaveSet} className="bg-[#0A0A0A] border border-[#2A2A2A] rounded-lg p-4">
                <div className="flex gap-3 mb-3">
                  <div className="flex-1">
                    <label className="block text-[10px] uppercase font-bold text-gray-500 mb-1">Weight (kg)</label>
                    <input 
                      type="number" step="0.5" required value={weight} onChange={e => setWeight(e.target.value)}
                      className="w-full bg-[#161616] text-white p-2 rounded border border-[#2A2A2A] focus:border-indigo-500 outline-none text-center font-bold"
                    />
                  </div>
                  <div className="flex items-end pb-2 font-black text-gray-600">x</div>
                  <div className="flex-1">
                    <label className="block text-[10px] uppercase font-bold text-gray-500 mb-1">Reps</label>
                    <input 
                      type="number" step="1" required value={reps} onChange={e => setReps(e.target.value)}
                      className="w-full bg-[#161616] text-white p-2 rounded border border-[#2A2A2A] focus:border-indigo-500 outline-none text-center font-bold"
                    />
                  </div>
                </div>
                <div className="flex gap-2">
                  <button type="submit" disabled={logMutation.isPending || updateMutation.isPending} className="flex-1 bg-indigo-600 hover:bg-indigo-500 text-white font-bold py-2 rounded transition-colors text-sm">
                    {currentWeekLog ? 'Update Best Set' : 'Save Best Set'}
                  </button>
                  {weight || reps ? (
                    <button type="button" onClick={() => { setWeight(''); setReps(''); }} className="px-3 bg-[#2A2A2A] hover:bg-[#333] text-white font-bold rounded transition-colors text-sm">
                      Cancel
                    </button>
                  ) : null}
                </div>
              </form>
            )}
          </div>

          <div>
            <h4 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3">Progress History</h4>
            {historicalLogs.length === 0 ? (
              <div className="text-sm text-gray-500 h-full flex items-center">No history recorded yet.</div>
            ) : (
              <div className="space-y-2 max-h-[120px] overflow-y-auto pr-2 custom-scrollbar">
                {historicalLogs.map(log => (
                  <div key={log.id} className="flex justify-between items-center text-sm border-b border-[#2A2A2A] pb-2 last:border-0 last:pb-0">
                    <span className="text-gray-400 font-medium">{getWeekNumber(log.log_date)}</span>
                    <span className="text-white font-bold">{log.weight_kg}kg <span className="text-gray-500 mx-1">x</span> {log.reps}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export const ExerciseLibraryPage = () => {
  const { data: activeExercises, isLoading: activeLoading } = useExercises(false);
  const { data: archivedExercises, isLoading: archivedLoading } = useExercises(true);
  const createMutation = useCreateExercise();

  const [newExerciseName, setNewExerciseName] = useState('');
  const [showArchived, setShowArchived] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleCreate = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newExerciseName.trim()) return;
    setErrorMessage(null);
    createMutation.mutate({ name: newExerciseName }, {
      onSuccess: () => setNewExerciseName(''),
      onError: (err: any) => {
        if (err.response?.status === 409) {
          setErrorMessage(err.response.data?.detail || 'An exercise with this name already exists.');
        } else {
          setErrorMessage('Failed to create exercise.');
        }
      }
    });
  };

  return (
    <div className="max-w-4xl mx-auto pb-20">
      <h1 className="text-3xl font-black text-white mb-8 tracking-tight">Exercise Library</h1>

      {errorMessage && (
        <div className="bg-red-500/10 border border-red-500/20 text-red-400 p-4 rounded-xl mb-6 font-bold text-sm">
          {errorMessage}
        </div>
      )}

      <form onSubmit={handleCreate} className="flex gap-3 mb-10">
        <input 
          type="text" 
          value={newExerciseName}
          onChange={e => { setNewExerciseName(e.target.value); setErrorMessage(null); }}
          placeholder="New exercise name (e.g. Incline Dumbbell Press)"
          className="flex-1 bg-[#161616] border border-[#2A2A2A] focus:border-indigo-500 rounded-xl px-4 py-3 text-white font-bold outline-none"
        />
        <button 
          type="submit"
          disabled={!newExerciseName.trim() || createMutation.isPending}
          className="bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-bold px-6 py-3 rounded-xl transition-colors"
        >
          Create
        </button>
      </form>

      <div className="mb-10">
        <h2 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-4">Active Exercises</h2>
        {activeLoading ? (
          <div className="text-gray-500">Loading...</div>
        ) : activeExercises?.length === 0 ? (
          <div className="text-gray-500 text-center p-8 bg-[#161616] border border-[#2A2A2A] rounded-xl">
            No active exercises. Add one above to start tracking.
          </div>
        ) : (
          <div className="space-y-4">
            {activeExercises?.map(ex => (
              <ExerciseLogTracker key={ex.id} exercise={ex} />
            ))}
          </div>
        )}
      </div>

      {archivedExercises && archivedExercises.length > 0 && (
        <div>
          <button 
            onClick={() => setShowArchived(!showArchived)}
            className="text-sm font-bold text-gray-500 hover:text-white uppercase tracking-wider mb-4 flex items-center gap-2 transition-colors"
          >
            {showArchived ? '▼' : '▶'} Archived Exercises ({archivedExercises.length})
          </button>
          
          {showArchived && (
            <div className="space-y-4 opacity-75">
              {archivedExercises.map(ex => (
                <ExerciseLogTracker key={ex.id} exercise={ex} />
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
