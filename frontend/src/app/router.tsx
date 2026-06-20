import { createBrowserRouter, Navigate } from 'react-router-dom';
import { GlobalWorkspaceLayout } from './layouts/GlobalWorkspaceLayout';
import { KitchenPage } from '../features/nutrition/pages/KitchenPage';
import { FoodsPage } from '../features/nutrition/pages/FoodsPage';
import { RecipesPage } from '../features/nutrition/pages/RecipesPage';
import { TemplatesPage } from '../features/nutrition/pages/TemplatesPage';
import { WeightPage } from '../features/health/pages/WeightPage';
import { MeasurementsPage } from '../features/health/pages/MeasurementsPage';
import { DashboardPage } from '../features/dashboard/pages/DashboardPage';
import { ExerciseLibraryPage } from '../features/training/pages/ExerciseLibraryPage';
import { CardioPage } from '../features/training/pages/CardioPage';
import { LoginPage } from '../features/auth/pages/LoginPage';
import { AuthCallbackPage } from '../features/auth/pages/AuthCallbackPage';
import { AuthGuard } from '../features/auth/components/AuthGuard';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Navigate to="/dashboard" replace />,
  },
  {
    path: '/login',
    element: <LoginPage />,
  },
  {
    path: '/auth/callback',
    element: <AuthCallbackPage />,
  },
  {
    path: '/',
    element: <AuthGuard />,
    children: [
      {
        path: '/',
        element: <GlobalWorkspaceLayout />,
        children: [
          {
            path: 'dashboard',
            element: <DashboardPage />,
          },
          {
            path: 'nutrition/kitchen',
            element: <KitchenPage />,
          },
          {
            path: 'nutrition/foods',
            element: <FoodsPage />,
          },
          {
            path: 'nutrition/recipes',
            element: <RecipesPage />,
          },
          {
            path: 'nutrition/templates',
            element: <TemplatesPage />,
          },
          {
            path: 'health/weight',
            element: <WeightPage />,
          },
          {
            path: 'health/measurements',
            element: <MeasurementsPage />,
          },
          {
            path: 'training/exercises',
            element: <ExerciseLibraryPage />,
          },
          {
            path: 'training/cardio',
            element: <CardioPage />,
          },
        ],
      },
    ],
  },
]);
