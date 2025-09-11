import axios from 'axios';
import type { 
  Funcionario, 
  FuncionarioFormData,
  Departamento,
  DepartamentoFormData,
  Cargo,
  CargoFormData,
  Presenca,
  PresencaFormData,
  Licenca,
  LicencaFormData,
  Avaliacao,
  AvaliacaoFormData,
  FolhaSalarial,
  FolhaSalarialFormData,
  Beneficio,
  BeneficioFormData,
  FuncionarioBeneficio,
  FuncionarioBeneficioFormData,
  ApiResponse,
  PaginatedResponse,
  DashboardMetrics,
  FuncionarioFilter,
  PresencaFilter,
  LicencaFilter
} from '../../types/rrhh';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';
const API_BASE = `${BASE_URL}/api/iamc`;

// Configure axios defaults
axios.defaults.timeout = 10000;

// Dashboard
export const getDashboardMetrics = async (): Promise<DashboardMetrics> => {
  const response = await axios.get(`${API_BASE}/dashboard/metrics`);
  return response.data;
};

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
  const response = await axios.get(`${API_BASE}/funcionarios?${params}`);
  return response.data;
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

export const getDepartamento = async (id: number): Promise<ApiResponse<Departamento>> => {
  const response = await axios.get(`${API_BASE}/departamentos/${id}`);
  return response.data;
};

export const createDepartamento = async (data: DepartamentoFormData): Promise<ApiResponse<Departamento>> => {
  const response = await axios.post(`${API_BASE}/departamentos`, data);
  return response.data;
};

export const updateDepartamento = async (id: number, data: Partial<DepartamentoFormData>): Promise<ApiResponse<Departamento>> => {
  const response = await axios.put(`${API_BASE}/departamentos/${id}`, data);
  return response.data;
};

export const deleteDepartamento = async (id: number): Promise<ApiResponse<void>> => {
  const response = await axios.delete(`${API_BASE}/departamentos/${id}`);
  return response.data;
};

// Cargos
export const getCargos = async (): Promise<ApiResponse<Cargo[]>> => {
  const response = await axios.get(`${API_BASE}/cargos`);
  return response.data;
};

export const getCargo = async (id: number): Promise<ApiResponse<Cargo>> => {
  const response = await axios.get(`${API_BASE}/cargos/${id}`);
  return response.data;
};

export const createCargo = async (data: CargoFormData): Promise<ApiResponse<Cargo>> => {
  const response = await axios.post(`${API_BASE}/cargos`, data);
  return response.data;
};

export const updateCargo = async (id: number, data: Partial<CargoFormData>): Promise<ApiResponse<Cargo>> => {
  const response = await axios.put(`${API_BASE}/cargos/${id}`, data);
  return response.data;
};

export const deleteCargo = async (id: number): Promise<ApiResponse<void>> => {
  const response = await axios.delete(`${API_BASE}/cargos/${id}`);
  return response.data;
};

// Presenças
export const getPresencas = async (filters?: PresencaFilter): Promise<PaginatedResponse<Presenca>> => {
  const params = new URLSearchParams();
  if (filters) {
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== '') {
        params.append(key, value.toString());
      }
    });
  }
  const response = await axios.get(`${API_BASE}/presencas?${params}`);
  return response.data;
};

export const getPresenca = async (id: number): Promise<ApiResponse<Presenca>> => {
  const response = await axios.get(`${API_BASE}/presencas/${id}`);
  return response.data;
};

export const createPresenca = async (data: PresencaFormData): Promise<ApiResponse<Presenca>> => {
  const response = await axios.post(`${API_BASE}/presencas`, data);
  return response.data;
};

export const updatePresenca = async (id: number, data: Partial<PresencaFormData>): Promise<ApiResponse<Presenca>> => {
  const response = await axios.put(`${API_BASE}/presencas/${id}`, data);
  return response.data;
};

export const deletePresenca = async (id: number): Promise<ApiResponse<void>> => {
  const response = await axios.delete(`${API_BASE}/presencas/${id}`);
  return response.data;
};

// Licenças
export const getLicencas = async (filters?: LicencaFilter): Promise<PaginatedResponse<Licenca>> => {
  const params = new URLSearchParams();
  if (filters) {
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== '') {
        params.append(key, value.toString());
      }
    });
  }
  const response = await axios.get(`${API_BASE}/licencas?${params}`);
  return response.data;
};

export const getLicenca = async (id: number): Promise<ApiResponse<Licenca>> => {
  const response = await axios.get(`${API_BASE}/licencas/${id}`);
  return response.data;
};

export const createLicenca = async (data: LicencaFormData): Promise<ApiResponse<Licenca>> => {
  const response = await axios.post(`${API_BASE}/licencas`, data);
  return response.data;
};

export const updateLicenca = async (id: number, data: Partial<LicencaFormData>): Promise<ApiResponse<Licenca>> => {
  const response = await axios.put(`${API_BASE}/licencas/${id}`, data);
  return response.data;
};

export const deleteLicenca = async (id: number): Promise<ApiResponse<void>> => {
  const response = await axios.delete(`${API_BASE}/licencas/${id}`);
  return response.data;
};

// Avaliações
export const getAvaliacoes = async (): Promise<ApiResponse<Avaliacao[]>> => {
  const response = await axios.get(`${API_BASE}/avaliacoes`);
  return response.data;
};

export const getAvaliacao = async (id: number): Promise<ApiResponse<Avaliacao>> => {
  const response = await axios.get(`${API_BASE}/avaliacoes/${id}`);
  return response.data;
};

export const createAvaliacao = async (data: AvaliacaoFormData): Promise<ApiResponse<Avaliacao>> => {
  const response = await axios.post(`${API_BASE}/avaliacoes`, data);
  return response.data;
};

export const updateAvaliacao = async (id: number, data: Partial<AvaliacaoFormData>): Promise<ApiResponse<Avaliacao>> => {
  const response = await axios.put(`${API_BASE}/avaliacoes/${id}`, data);
  return response.data;
};

export const deleteAvaliacao = async (id: number): Promise<ApiResponse<void>> => {
  const response = await axios.delete(`${API_BASE}/avaliacoes/${id}`);
  return response.data;
};

// Folha Salarial
export const getFolhasSalariais = async (): Promise<ApiResponse<FolhaSalarial[]>> => {
  const response = await axios.get(`${API_BASE}/folha-salarial`);
  return response.data;
};

export const getFolhaSalarial = async (id: number): Promise<ApiResponse<FolhaSalarial>> => {
  const response = await axios.get(`${API_BASE}/folha-salarial/${id}`);
  return response.data;
};

export const createFolhaSalarial = async (data: FolhaSalarialFormData): Promise<ApiResponse<FolhaSalarial>> => {
  const response = await axios.post(`${API_BASE}/folha-salarial`, data);
  return response.data;
};

export const updateFolhaSalarial = async (id: number, data: Partial<FolhaSalarialFormData>): Promise<ApiResponse<FolhaSalarial>> => {
  const response = await axios.put(`${API_BASE}/folha-salarial/${id}`, data);
  return response.data;
};

export const deleteFolhaSalarial = async (id: number): Promise<ApiResponse<void>> => {
  const response = await axios.delete(`${API_BASE}/folha-salarial/${id}`);
  return response.data;
};

// Benefícios
export const getBeneficios = async (): Promise<ApiResponse<Beneficio[]>> => {
  const response = await axios.get(`${API_BASE}/beneficios`);
  return response.data;
};

export const getBeneficio = async (id: number): Promise<ApiResponse<Beneficio>> => {
  const response = await axios.get(`${API_BASE}/beneficios/${id}`);
  return response.data;
};

export const createBeneficio = async (data: BeneficioFormData): Promise<ApiResponse<Beneficio>> => {
  const response = await axios.post(`${API_BASE}/beneficios`, data);
  return response.data;
};

export const updateBeneficio = async (id: number, data: Partial<BeneficioFormData>): Promise<ApiResponse<Beneficio>> => {
  const response = await axios.put(`${API_BASE}/beneficios/${id}`, data);
  return response.data;
};

export const deleteBeneficio = async (id: number): Promise<ApiResponse<void>> => {
  const response = await axios.delete(`${API_BASE}/beneficios/${id}`);
  return response.data;
};

// Funcionário-Benefícios
export const getFuncionarioBeneficios = async (): Promise<ApiResponse<FuncionarioBeneficio[]>> => {
  const response = await axios.get(`${API_BASE}/funcionario-beneficios`);
  return response.data;
};

export const getFuncionarioBeneficio = async (id: number): Promise<ApiResponse<FuncionarioBeneficio>> => {
  const response = await axios.get(`${API_BASE}/funcionario-beneficios/${id}`);
  return response.data;
};

export const createFuncionarioBeneficio = async (data: FuncionarioBeneficioFormData): Promise<ApiResponse<FuncionarioBeneficio>> => {
  const response = await axios.post(`${API_BASE}/funcionario-beneficios`, data);
  return response.data;
};

export const updateFuncionarioBeneficio = async (id: number, data: Partial<FuncionarioBeneficioFormData>): Promise<ApiResponse<FuncionarioBeneficio>> => {
  const response = await axios.put(`${API_BASE}/funcionario-beneficios/${id}`, data);
  return response.data;
};

export const deleteFuncionarioBeneficio = async (id: number): Promise<ApiResponse<void>> => {
  const response = await axios.delete(`${API_BASE}/funcionario-beneficios/${id}`);
  return response.data;
};

// Utilitários
export const exportToCSV = async (endpoint: string, filename: string): Promise<void> => {
  const response = await axios.get(`${API_BASE}/${endpoint}/export/csv`, {
    responseType: 'blob',
  });
  
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', `${filename}.csv`);
  document.body.appendChild(link);
  link.click();
  link.remove();
};

export const exportToExcel = async (endpoint: string, filename: string): Promise<void> => {
  const response = await axios.get(`${API_BASE}/${endpoint}/export/excel`, {
    responseType: 'blob',
  });
  
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', `${filename}.xlsx`);
  document.body.appendChild(link);
  link.click();
  link.remove();
};
