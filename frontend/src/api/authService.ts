//authService.ts

import axiosInstance from './axiosInstance';

interface LoginResponse {
  access_token: string;
  user: {
    id: number;
    email: string;
    name: string;
    role: string;
  };
}

export const authService = {
  login: async (email: string, password: string): Promise<LoginResponse> => {
    const response = await axiosInstance.post('/auth/login', { email, password });
    localStorage.setItem('access_token', response.data.access_token);
    return response.data;
  },

  logout: (): void => {
    localStorage.removeItem('access_token');
    window.location.href = '/login';
  },

  register: async (email: string, password: string, name?: string): Promise<void> => {
    await axiosInstance.post('/auth/register', { email, password, name });
  },

  getProfile: async (): Promise<LoginResponse['user']> => {
    const response = await axiosInstance.get('/users/profile');
    return response.data;
  },

  refreshToken: async (): Promise<string> => {
    const response = await axiosInstance.post('/auth/refresh');
    localStorage.setItem('access_token', response.data.access_token);
    return response.data.access_token;
  },

  getCurrentUser: (): LoginResponse['user'] | null => {
    const token = localStorage.getItem('access_token');
    return token ? JSON.parse(atob(token.split('.')[1])) : null;
  }
};