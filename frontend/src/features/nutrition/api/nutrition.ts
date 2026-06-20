import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../../../lib/axios';
import { 
  FoodItemRead, 
  RecipeRead, 
  MealTemplateRead, 
  DailyNutritionLogRead,
  DailyNutritionLogEntryCreate,
  DailyNutritionLogItemUpdate,
  FoodItemCreate,
  FoodItemUpdate,
  RecipeCreate,
  RecipeUpdate,
  MealTemplateCreate,
  MealTemplateUpdate
} from '../types';

// Query Keys Strategy for Cache Management
export const nutritionKeys = {
  all: ['nutrition'] as const,
  foods: () => [...nutritionKeys.all, 'foods'] as const,
  recipes: () => [...nutritionKeys.all, 'recipes'] as const,
  templates: () => [...nutritionKeys.all, 'templates'] as const,
  logs: () => [...nutritionKeys.all, 'logs'] as const,
  logByDate: (date: string) => [...nutritionKeys.logs(), date] as const,
};

// --- API FETCHERS ---

export const getFoods = async (q: string): Promise<FoodItemRead[]> => {
  if (q) {
    const { data } = await apiClient.get(`/api/v1/foods/search?q=${q}`);
    return data;
  }
  const { data } = await apiClient.get('/api/v1/foods?limit=500');
  return data;
};

export const createFood = async (data: FoodItemCreate): Promise<FoodItemRead> => {
  const response = await apiClient.post('/api/v1/foods', data);
  return response.data;
};

export const updateFood = async ({ foodId, update }: { foodId: string, update: FoodItemUpdate }): Promise<FoodItemRead> => {
  const response = await apiClient.put(`/api/v1/foods/${foodId}`, update);
  return response.data;
};

export const cloneOverrideFood = async ({ foodId, data }: { foodId: string, data: FoodItemCreate }): Promise<FoodItemRead> => {
  const response = await apiClient.post(`/api/v1/foods/${foodId}/override`, data);
  return response.data;
};

export const deleteFood = async (foodId: string) => {
  await apiClient.delete(`/api/v1/foods/${foodId}`);
};

export const getRecipes = async (): Promise<RecipeRead[]> => {
  const { data } = await apiClient.get('/api/v1/recipes');
  return data;
};

export const createRecipe = async (data: RecipeCreate): Promise<RecipeRead> => {
  const response = await apiClient.post('/api/v1/recipes', data);
  return response.data;
};

export const updateRecipe = async ({ recipeId, update }: { recipeId: string, update: RecipeUpdate }): Promise<RecipeRead> => {
  const response = await apiClient.put(`/api/v1/recipes/${recipeId}`, update);
  return response.data;
};

export const deleteRecipe = async (recipeId: string) => {
  await apiClient.delete(`/api/v1/recipes/${recipeId}`);
};

export const getTemplates = async (): Promise<MealTemplateRead[]> => {
  const { data } = await apiClient.get('/api/v1/meal-templates');
  return data;
};

export const createTemplate = async (data: MealTemplateCreate): Promise<MealTemplateRead> => {
  const response = await apiClient.post('/api/v1/meal-templates', data);
  return response.data;
};

export const updateTemplate = async ({ templateId, update }: { templateId: string, update: MealTemplateUpdate }): Promise<MealTemplateRead> => {
  const response = await apiClient.put(`/api/v1/meal-templates/${templateId}`, update);
  return response.data;
};

export const deleteTemplate = async (templateId: string) => {
  await apiClient.delete(`/api/v1/meal-templates/${templateId}`);
};

export const getDailyLog = async (date: string): Promise<DailyNutritionLogRead> => {
  const { data } = await apiClient.get(`/api/v1/nutrition-logs/${date}`);
  return data;
};

export const createLogEntry = async ({ date, entry }: { date: string, entry: DailyNutritionLogEntryCreate }) => {
  const { data } = await apiClient.post(`/api/v1/nutrition-logs/entries?log_date=${date}`, entry);
  return data;
};

export const updateLogItem = async ({ itemId, update }: { itemId: string, update: DailyNutritionLogItemUpdate }) => {
  const { data } = await apiClient.put(`/api/v1/nutrition-logs/items/${itemId}`, update);
  return data;
};

export const deleteLogItem = async (itemId: string) => {
  await apiClient.delete(`/api/v1/nutrition-logs/items/${itemId}`);
};

// --- REACT QUERY HOOKS ---

export const useFoods = (q: string = '') => {
  return useQuery({
    queryKey: [...nutritionKeys.foods(), q],
    queryFn: () => getFoods(q),
  });
};

export const useCreateFood = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: createFood,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: nutritionKeys.foods() });
    },
  });
};

export const useUpdateFood = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: updateFood,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: nutritionKeys.foods() });
    },
  });
};

export const useCloneFood = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: cloneOverrideFood,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: nutritionKeys.foods() });
    },
  });
};

export const useDeleteFood = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: deleteFood,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: nutritionKeys.foods() });
    },
  });
};

export const useRecipes = () => {
  return useQuery({
    queryKey: nutritionKeys.recipes(),
    queryFn: getRecipes,
  });
};

export const useCreateRecipe = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: createRecipe,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: nutritionKeys.recipes() });
    },
  });
};

export const useUpdateRecipe = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: updateRecipe,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: nutritionKeys.recipes() });
    },
  });
};

export const useDeleteRecipe = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: deleteRecipe,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: nutritionKeys.recipes() });
    },
  });
};

export const useTemplates = () => {
  return useQuery({
    queryKey: nutritionKeys.templates(),
    queryFn: getTemplates,
  });
};

export const useCreateTemplate = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: createTemplate,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: nutritionKeys.templates() });
    },
  });
};

export const useUpdateTemplate = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: updateTemplate,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: nutritionKeys.templates() });
    },
  });
};

export const useDeleteTemplate = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: deleteTemplate,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: nutritionKeys.templates() });
    },
  });
};

export const useDailyLog = (date: string) => {
  return useQuery({
    queryKey: nutritionKeys.logByDate(date),
    queryFn: () => getDailyLog(date),
  });
};

export const useCreateLogEntry = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: createLogEntry,
    onSuccess: (_, variables) => {
      // Invalidate the log for this specific date so the UI refreshes
      queryClient.invalidateQueries({ queryKey: nutritionKeys.logByDate(variables.date) });
    },
  });
};

export const useUpdateLogItem = (date: string) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: updateLogItem,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: nutritionKeys.logByDate(date) });
    },
  });
};

export const useDeleteLogItem = (date: string) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: deleteLogItem,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: nutritionKeys.logByDate(date) });
    },
  });
};
