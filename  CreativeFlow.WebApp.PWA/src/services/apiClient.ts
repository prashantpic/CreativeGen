import axios, { AxiosInstance, InternalAxiosRequestConfig, AxiosError } from 'axios';
import { useAuthStore } from '@/app/store';
import { useNotificationStore } from '@/app/store/slices/notificationStore';

/**
 * A centralized Axios instance for making HTTP requests to the backend API.
 * It is configured with a base URL and interceptors for handling
 * authentication tokens and global API error responses.
 */
const apiClient: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  timeout: 15000, // 15 seconds timeout
});

/**
 * Request Interceptor:
 * Attaches the JWT authentication token to the `Authorization` header
 * of every outgoing request if a token is available in the `authStore`.
 */
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = useAuthStore.getState().token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    // This part is rarely hit, but good practice to have.
    // It's for errors that happen before the request is even sent.
    console.error('Axios Request Error:', error);
    return Promise.reject(error);
  }
);

/**
 * Response Interceptor:
 * Handles global error responses from the API.
 * - On a `401 Unauthorized` error, it logs the user out.
 * - For other errors, it can be configured to show a generic notification.
 */
apiClient.interceptors.response.use(
  (response) => {
    // Any status code that lie within the range of 2xx cause this function to trigger
    return response;
  },
  (error: AxiosError) => {
    // Any status codes that falls outside the range of 2xx cause this function to trigger
    if (error.response) {
      const { status } = error.response;
      
      // Handle 401 Unauthorized: Token is invalid or expired
      if (status === 401) {
        // Prevent multiple logouts if multiple requests fail
        if (useAuthStore.getState().isAuthenticated) {
            console.warn('Unauthorized access (401). Logging out.');
            useAuthStore.getState().logout();
            useNotificationStore.getState().addNotification({
                id: 'auth-error',
                type: 'error',
                message: 'Your session has expired. Please log in again.',
                duration: 5000
            });
            // The router guard will handle the redirect to /login
        }
      } else if (status >= 500) {
        // Handle server-side errors
        console.error('Server Error:', error.response.data);
         useNotificationStore.getState().addNotification({
                id: `server-error-${Date.now()}`,
                type: 'error',
                message: 'A server error occurred. Please try again later.',
                duration: 5000
            });
      }
    } else if (error.request) {
      // The request was made but no response was received (e.g., network error)
      console.error('Network Error:', error.request);
      useNotificationStore.getState().addNotification({
                id: `network-error-${Date.now()}`,
                type: 'error',
                message: 'Network error. Please check your connection.',
                duration: 5000
            });
    }

    return Promise.reject(error);
  }
);

export default apiClient;