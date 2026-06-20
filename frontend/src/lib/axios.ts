import axios from 'axios';

// Create a configured Axios instance
export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request Interceptor: Attach JWT Token
apiClient.interceptors.request.use(
  (config) => {
    // In a real implementation, we would pull this from Zustand or localStorage
    const token = localStorage.getItem('track_auth_token');
    
    // For development/stubbing based on backend config, we might not need to attach 
    // it if using the _DEV_TEST_USER_ID, but this is the production architecture.
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response Interceptor: Handle global errors (e.g., 401 Unauthorized)
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Flush token and redirect to login
      localStorage.removeItem('track_auth_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
