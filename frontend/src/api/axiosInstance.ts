// axiosInstance.ts

import axios, { AxiosError, AxiosInstance, AxiosResponse, InternalAxiosRequestConfig, AxiosRequestConfig } from 'axios';

// Interfaces for token types
interface TokenResponse {
  access_token: string;
  refresh_token?: string;
}

interface ApiError {
  error: string;
  message: string;
  statusCode: number;
}

// Global state for token handling
let isRefreshing = false;
type QueueItem = { resolve: (token: string) => void; reject: (error: unknown) => void };
let failedQueue: QueueItem[] = [];

const processQueue = (error: unknown, token: string | null = null) => {
  failedQueue.forEach(prom => {
    error ? prom.reject(error) : prom.resolve(token!);
  });
  failedQueue = [];
};

// Backend base URL
const axiosInstance: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000',
  headers: {
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
  },
  timeout: 10000,
});

// Request interceptor
axiosInstance.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('access_token');
    const language = localStorage.getItem('i18nextLng') || 'en';

    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    config.headers['Accept-Language'] = language;
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
axiosInstance.interceptors.response.use(
  (response: AxiosResponse) => response,
  async (error: AxiosError<ApiError>) => {
    const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean };

    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise<string>((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        }).then((token) => {
          originalRequest.headers!.Authorization = `Bearer ${token}`;
          return axiosInstance(originalRequest);
        });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) throw new Error('No refresh token available');

        const { data } = await axios.post<TokenResponse>(
          '/auth/refresh',
          { refresh_token: refreshToken },
          { baseURL: import.meta.env.VITE_API_URL }
        );

        localStorage.setItem('access_token', data.access_token);
        axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${data.access_token}`;

        processQueue(null, data.access_token);
        return axiosInstance(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        processQueue(refreshError, null);
        window.location.href = '/login';
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    const errorData: ApiError = {
      error: error.response?.data?.error || 'unknown_error',
      message: error.response?.data?.message || 'Unknown error',
      statusCode: error.response?.status || 500,
    };

    return Promise.reject({
      ...errorData,
      isApiError: true,
      localizedMessage: getLocalizedErrorMessage(errorData.error),
    });
  }
);

// Localized error messages
type LocalizedMessages = {
  [key: string]: {
    [lang: string]: string;
  };
};

const localizedMessages: LocalizedMessages = {
  invalid_token: {
    en: 'Session expired, please login again',
    es: 'Sesión expirada, por favor inicie sesión nuevamente',
  },
  network_error: {
    en: 'Network error - please check your connection',
    es: 'Error de red - verifique su conexión',
  },
};

const getLocalizedErrorMessage = (messageKey: string): string => {
  const language = localStorage.getItem('i18nextLng') || 'en';
  return localizedMessages[messageKey]?.[language] || messageKey;
};

export default axiosInstance;