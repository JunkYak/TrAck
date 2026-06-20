import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../../../lib/axios';
import { WeightLogRead, WeightLogCreate, WeightLogUpdate } from '../types';

const WEIGHT_QUERY_KEYS = {
  all: ['weights'] as const,
  list: (limit: number, offset: number) => [...WEIGHT_QUERY_KEYS.all, 'list', limit, offset] as const,
  latest: () => [...WEIGHT_QUERY_KEYS.all, 'latest'] as const,
};

export const useWeights = (limit: number = 100, offset: number = 0) => {
  return useQuery({
    queryKey: WEIGHT_QUERY_KEYS.list(limit, offset),
    queryFn: async () => {
      const { data } = await apiClient.get<WeightLogRead[]>('/api/v1/weights', {
        params: { limit, offset }
      });
      return data;
    },
  });
};

export const useLatestWeight = () => {
  return useQuery({
    queryKey: WEIGHT_QUERY_KEYS.latest(),
    queryFn: async () => {
      try {
        const { data } = await apiClient.get<WeightLogRead>('/api/v1/weights/latest');
        return data;
      } catch (error: any) {
        // If 404, it means no weight logged yet. Return null instead of throwing.
        if (error.response?.status === 404) {
          return null;
        }
        throw error;
      }
    },
    // Prevent retries on 404
    retry: (failureCount, error: any) => {
      if (error.response?.status === 404) return false;
      return failureCount < 3;
    }
  });
};

export const useLogWeight = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (payload: WeightLogCreate) => {
      const { data } = await apiClient.post<WeightLogRead>('/api/v1/weights', payload);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: WEIGHT_QUERY_KEYS.all });
    },
  });
};

export const useUpdateWeight = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ id, payload }: { id: string; payload: WeightLogUpdate }) => {
      const { data } = await apiClient.put<WeightLogRead>(`/api/v1/weights/${id}`, payload);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: WEIGHT_QUERY_KEYS.all });
    },
  });
};

export const useDeleteWeight = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: string) => {
      await apiClient.delete(`/api/v1/weights/${id}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: WEIGHT_QUERY_KEYS.all });
    },
  });
};
