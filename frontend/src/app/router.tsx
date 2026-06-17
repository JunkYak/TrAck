import { createBrowserRouter, Navigate } from 'react-router-dom';
import { NutritionWorkspaceLayout } from '../features/nutrition/layouts/NutritionWorkspaceLayout';
import { KitchenPage } from '../features/nutrition/pages/KitchenPage';
import { FoodsPage } from '../features/nutrition/pages/FoodsPage';
import { RecipesPage } from '../features/nutrition/pages/RecipesPage';
import { TemplatesPage } from '../features/nutrition/pages/TemplatesPage';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Navigate to="/nutrition/kitchen" replace />,
  },
  {
    path: '/nutrition',
    element: <NutritionWorkspaceLayout />,
    children: [
      {
        index: true,
        element: <Navigate to="/nutrition/kitchen" replace />,
      },
      {
        path: 'kitchen',
        element: <KitchenPage />,
      },
      {
        path: 'foods',
        element: <FoodsPage />,
      },
      {
        path: 'recipes',
        element: <RecipesPage />,
      },
      {
        path: 'templates',
        element: <TemplatesPage />,
      },
    ],
  },
]);
