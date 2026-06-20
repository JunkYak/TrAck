import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../../../lib/axios';
import { 
  ExerciseRead, ExerciseCreate, ExerciseUpdate,
  ExerciseLogRead, ExerciseLogCreate, ExerciseLogUpdate
} from '../types';

export const EXERCISE_QUERY_KEYS = {
  all: ['exercises'] as const,
  list: (archived: boolean) => [...EXERCISE_QUERY_KEYS.all, 'list', archived] as const,
  logs: (exerciseId: string) => [...EXERCISE_QUERY_KEYS.all, 'logs', exerciseId] as const,
  latestLogs: () => [...EXERCISE_QUERY_KEYS.all, 'logs', 'latest'] as const,
};

// --- Exercises ---
export const useExercises = (archived: boolean = false) => {
  return useQuery({
    queryKey: EXERCISE_QUERY_KEYS.list(archived),
    queryFn: async () => {
      const { data } = await apiClient.get<ExerciseRead[]>('/api/v1/exercises', {
        params: { archived }
      });
      return data;
    },
  });
};

export const useCreateExercise = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (payload: ExerciseCreate) => {
      const { data } = await apiClient.post<ExerciseRead>('/api/v1/exercises', payload);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: EXERCISE_QUERY_KEYS.all });
    },
  });
};

export const useUpdateExercise = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, payload }: { id: string; payload: ExerciseUpdate }) => {
      const { data } = await apiClient.put<ExerciseRead>(`/api/v1/exercises/${id}`, payload);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: EXERCISE_QUERY_KEYS.all });
    },
  });
};

export const useArchiveExercise = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (id: string) => {
      const { data } = await apiClient.post<ExerciseRead>(`/api/v1/exercises/${id}/archive`);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: EXERCISE_QUERY_KEYS.all });
    },
  });
};

export const useRestoreExercise = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (id: string) => {
      const { data } = await apiClient.post<ExerciseRead>(`/api/v1/exercises/${id}/restore`);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: EXERCISE_QUERY_KEYS.all });
    },
  });
};

// --- Exercise Logs ---
export const useExerciseLogs = (exerciseId: string) => {
  return useQuery({
    queryKey: EXERCISE_QUERY_KEYS.logs(exerciseId),
    queryFn: async () => {
      const { data } = await apiClient.get<ExerciseLogRead[]>(`/api/v1/exercises/${exerciseId}/logs`);
      return data;
    },
    enabled: !!exerciseId,
  });
};

export const useLatestExerciseLogs = () => {
  return useQuery({
    queryKey: EXERCISE_QUERY_KEYS.latestLogs(),
    queryFn: async () => {
      const { data } = await apiClient.get<ExerciseLogRead[]>('/api/v1/exercises/logs/latest');
      return data;
    },
  });
};

export const useLogBestSet = (exerciseId: string) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (payload: ExerciseLogCreate) => {
      const { data } = await apiClient.post<ExerciseLogRead>(`/api/v1/exercises/${exerciseId}/logs`, payload);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: EXERCISE_QUERY_KEYS.all });
    },
  });
};

export const useUpdateBestSet = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, payload }: { id: string; payload: ExerciseLogUpdate }) => {
      const { data } = await apiClient.put<ExerciseLogRead>(`/api/v1/exercises/logs/${id}`, payload);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: EXERCISE_QUERY_KEYS.all });
    },
  });
};

export const useDeleteBestSet = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (id: string) => {
      await apiClient.delete(`/api/v1/exercises/logs/${id}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: EXERCISE_QUERY_KEYS.all });
    },
  });
};
