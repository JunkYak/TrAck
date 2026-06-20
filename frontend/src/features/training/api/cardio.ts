import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../../../lib/axios';
import { CardioSessionRead, CardioSessionCreate, CardioSessionUpdate } from '../types';

export const CARDIO_QUERY_KEYS = {
  all: ['cardio'] as const,
  list: (limit: number) => [...CARDIO_QUERY_KEYS.all, 'list', limit] as const,
};

export const useCardioSessions = (limit: number = 100) => {
  return useQuery({
    queryKey: CARDIO_QUERY_KEYS.list(limit),
    queryFn: async () => {
      const { data } = await apiClient.get<CardioSessionRead[]>('/api/v1/cardio', {
        params: { limit, offset: 0 }
      });
      return data;
    },
  });
};

export const useCreateCardioSession = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (payload: CardioSessionCreate) => {
      const { data } = await apiClient.post<CardioSessionRead>('/api/v1/cardio', payload);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: CARDIO_QUERY_KEYS.all });
    },
  });
};

export const useUpdateCardioSession = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, payload }: { id: string; payload: CardioSessionUpdate }) => {
      const { data } = await apiClient.put<CardioSessionRead>(`/api/v1/cardio/${id}`, payload);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: CARDIO_QUERY_KEYS.all });
    },
  });
};

export const useDeleteCardioSession = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (id: string) => {
      await apiClient.delete(`/api/v1/cardio/${id}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: CARDIO_QUERY_KEYS.all });
    },
  });
};
