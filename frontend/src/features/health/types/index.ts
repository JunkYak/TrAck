export interface WeightLogRead {
  id: string;
  user_id: string;
  created_at: string;
  date: string; // YYYY-MM-DD
  weight_kg: number;
}

export interface WeightLogCreate {
  date: string;
  weight_kg: number;
}

export interface WeightLogUpdate {
  date?: string;
  weight_kg?: number;
}

export interface MeasurementSessionRead {
  id: string;
  user_id: string;
  created_at: string;
  date: string; // YYYY-MM-DD
  waist_in: number | null;
  bicep_in: number | null;
  quad_in: number | null;
}

export interface MeasurementSessionCreate {
  date: string;
  waist_in?: number | null;
  bicep_in?: number | null;
  quad_in?: number | null;
}

export interface MeasurementSessionUpdate {
  date?: string;
  waist_in?: number | null;
  bicep_in?: number | null;
  quad_in?: number | null;
}
