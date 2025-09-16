import axios from 'axios';
import type { 
  Funcionario, 
  FuncionarioFormData,
  Departamento,
  Cargo,
  ApiResponse,
  PaginatedResponse,
  FuncionarioFilter
} from '../../types/rrhh';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';
const API_BASE = `${BASE_URL}/api/iamc`;

// Configure axios defaults
axios.defaults.timeout = 10000;

// Funcionários
export const getFuncionarios = async (filters?: FuncionarioFilter): Promise<PaginatedResponse<Funcionario>> => {
  const params = new URLSearchParams();
  if (filters) {
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== '') {
        params.append(key, value.toString());
      }
    });
  }
  
  const url = `${API_BASE}/funcionarios?${params}`;
  console.log('🌐 Fazendo requisição para:', url);
  
  try {
    const response = await axios.get(url);
    console.log('📡 Status da resposta:', response.status);
    console.log('📄 Dados da resposta:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Erro na requisição:', error);
    if (axios.isAxiosError(error)) {
      console.error('📋 Detalhes do erro:', {
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data
      });
    }
    throw error;
  }
};

export const getFuncionario = async (id: number): Promise<ApiResponse<Funcionario>> => {
  const response = await axios.get(`${API_BASE}/funcionarios/${id}`);
  return response.data;
};

export const createFuncionario = async (data: FuncionarioFormData): Promise<ApiResponse<Funcionario>> => {
  const response = await axios.post(`${API_BASE}/funcionarios`, data);
  return response.data;
};

export const updateFuncionario = async (id: number, data: Partial<FuncionarioFormData>): Promise<ApiResponse<Funcionario>> => {
  const response = await axios.put(`${API_BASE}/funcionarios/${id}`, data);
  return response.data;
};

export const deleteFuncionario = async (id: number): Promise<ApiResponse<void>> => {
  const response = await axios.delete(`${API_BASE}/funcionarios/${id}`);
  return response.data;
};

// Upload de foto
export const uploadFoto = async (id: number, foto: File): Promise<ApiResponse<Funcionario>> => {
  const formData = new FormData();
  formData.append('foto', foto);
  const response = await axios.post(`${API_BASE}/funcionarios/${id}/foto`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getFotoInfo = async (id: number): Promise<ApiResponse<{foto_url: string; funcionario_id: number; nome: string}>> => {
  const response = await axios.get(`${API_BASE}/funcionarios/${id}/foto`);
  return response.data;
};

export const deleteFoto = async (id: number): Promise<ApiResponse<void>> => {
  const response = await axios.delete(`${API_BASE}/funcionarios/${id}/foto`);
  return response.data;
};

// Departamentos
export const getDepartamentos = async (): Promise<ApiResponse<Departamento[]>> => {
  const response = await axios.get(`${API_BASE}/departamentos`);
  return response.data;
};

// Cargos
export const getCargos = async (): Promise<ApiResponse<Cargo[]>> => {
  const response = await axios.get(`${API_BASE}/cargos`);
  return response.data;
};

// Status IAMC
export const getStatusIAMC = async () => {
  const response = await axios.get(`${API_BASE}/status`);
  return response.data;
};

export default {
  getFuncionarios,
  getFuncionario,
  createFuncionario,
  updateFuncionario,
  deleteFuncionario,
  uploadFoto,
  getFotoInfo,
  deleteFoto,
  getDepartamentos,
  getCargos,
  getStatusIAMC
};
