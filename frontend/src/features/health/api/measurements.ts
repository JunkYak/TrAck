import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../../../lib/axios';
import { MeasurementSessionRead, MeasurementSessionCreate, MeasurementSessionUpdate } from '../types';

const MEASUREMENT_QUERY_KEYS = {
  all: ['measurements'] as const,
  list: (limit: number, offset: number) => [...MEASUREMENT_QUERY_KEYS.all, 'list', limit, offset] as const,
  latest: () => [...MEASUREMENT_QUERY_KEYS.all, 'latest'] as const,
};

export const useMeasurements = (limit: number = 100, offset: number = 0) => {
  return useQuery({
    queryKey: MEASUREMENT_QUERY_KEYS.list(limit, offset),
    queryFn: async () => {
      const { data } = await apiClient.get<MeasurementSessionRead[]>('/api/v1/measurements', {
        params: { limit, offset }
      });
      return data;
    },
  });
};

export const useLatestMeasurement = () => {
  return useQuery({
    queryKey: MEASUREMENT_QUERY_KEYS.latest(),
    queryFn: async () => {
      try {
        const { data } = await apiClient.get<MeasurementSessionRead>('/api/v1/measurements/latest');
        return data;
      } catch (error: any) {
        if (error.response?.status === 404) {
          return null;
        }
        throw error;
      }
    },
    retry: (failureCount, error: any) => {
      if (error.response?.status === 404) return false;
      return failureCount < 3;
    }
  });
};

export const useLogMeasurement = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (payload: MeasurementSessionCreate) => {
      const { data } = await apiClient.post<MeasurementSessionRead>('/api/v1/measurements', payload);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: MEASUREMENT_QUERY_KEYS.all });
    },
  });
};

export const useUpdateMeasurement = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ id, payload }: { id: string; payload: MeasurementSessionUpdate }) => {
      const { data } = await apiClient.put<MeasurementSessionRead>(`/api/v1/measurements/${id}`, payload);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: MEASUREMENT_QUERY_KEYS.all });
    },
  });
};

export const useDeleteMeasurement = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: string) => {
      await apiClient.delete(`/api/v1/measurements/${id}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: MEASUREMENT_QUERY_KEYS.all });
    },
  });
};
