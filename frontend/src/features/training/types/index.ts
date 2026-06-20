export interface ExerciseRead {
  id: string;
  user_id: string;
  name: string;
  is_archived: boolean;
  created_at: string;
  updated_at: string | null;
}

export interface ExerciseCreate {
  name: string;
}

export interface ExerciseUpdate {
  name: string;
}

export interface ExerciseLogRead {
  id: string;
  user_id: string;
  exercise_id: string;
  log_date: string; // YYYY-MM-DD
  weight_kg: number;
  reps: number;
  notes: string | null;
  created_at: string;
  updated_at: string | null;
}

export interface ExerciseLogCreate {
  log_date: string;
  weight_kg: number;
  reps: number;
  notes?: string | null;
}

export interface ExerciseLogUpdate {
  log_date?: string;
  weight_kg?: number;
  reps?: number;
  notes?: string | null;
}

// --- Cardio ---
export type RunType = 'EASY' | 'TEMPO_INTERVAL' | 'LONG';

export interface CardioSessionRead {
  id: string;
  user_id: string;
  run_type: RunType;
  distance_km: number;
  duration_minutes: number;
  average_pace: number;
  body_weight_used: number;
  estimated_calories: number;
  notes: string | null;
  performed_at: string; // ISO datetime
  created_at: string;
  updated_at: string | null;
}

export interface CardioSessionCreate {
  run_type: RunType;
  distance_km: number;
  duration_minutes: number;
  notes?: string | null;
  performed_at?: string; // ISO datetime
}

export interface CardioSessionUpdate {
  run_type?: RunType;
  distance_km?: number;
  duration_minutes?: number;
  notes?: string | null;
  performed_at?: string; // ISO datetime
}
