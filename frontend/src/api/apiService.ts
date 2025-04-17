// apiService.ts

import axiosInstance from './axiosInstance';

// ------------------- Servicio de Usuarios ---------------------------
export const userService = {
  getUsers: async () => {
    try {
      const response = await axiosInstance.get('/users');
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener usuarios');
    }
  },

  createUser: async (userData: any) => {
    try {
      const response = await axiosInstance.post('/users', userData);
      return response.data;
    } catch (error) {
      throw new Error('Error al crear usuario');
    }
  },

  updateUser: async (userId: number, userData: any) => {
    try {
      const response = await axiosInstance.put(`/users/${userId}`, userData);
      return response.data;
    } catch (error) {
      throw new Error('Error al actualizar usuario');
    }
  },

  deleteUser: async (userId: number) => {
    try {
      const response = await axiosInstance.delete(`/users/${userId}`);
      return response.data;
    } catch (error) {
      throw new Error('Error al eliminar usuario');
    }
  }
};

// ------------------- Servicio de QR ---------------------------
export const fetchFuncionarios = async (page: number, perPage: number, filtro: string) => {
  const response = await axiosInstance.get('/qr/funcionarios', {
    params: { page, per_page: perPage, filtro },
  });
  return response.data;
};

export const generateQR = async (ids: number[]) => {
  const response = await axiosInstance.post('/qr/generar', { ids });
  return response.data;
};

export const deleteQR = async (contactId: number) => {
  const response = await axiosInstance.delete(`/qr/eliminar/${contactId}`);
  return response.data;
};

export const downloadQR = async (contactId: number) => {
  const response = await axiosInstance.get(`/qr/descargar/${contactId}`, { responseType: 'blob' });
  return response.data;
};

export const downloadMultipleQR = async (ids: number[]) => {
  const response = await axiosInstance.post('/qr/descargar-multiples', { ids }, { responseType: 'blob' });
  return response.data;
};
