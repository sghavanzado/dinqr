// Tipos base
export interface BaseEntity {
  id: number;
  createdAt?: string;
  updatedAt?: string;
}

// Funcionário
export interface Funcionario extends BaseEntity {
  funcionarioID: number;
  FuncionarioID?: number; // Campo PascalCase del backend
  nome: string;
  apelido: string;
  bi: string;
  dataNascimento?: string;
  sexo?: 'M' | 'F' | 'O';
  estadoCivil?: string;
  email?: string;
  telefone?: string;
  endereco?: string;
  dataAdmissao: string;
  estadoFuncionario: 'Activo' | 'Inactivo' | 'Suspenso';
  foto?: string;
  cargoID?: number;
  departamentoID?: number;
  // Campos PascalCase del backend
  Nome?: string;
  Apelido?: string;
  BI?: string;
  DataNascimento?: string;
  Sexo?: 'M' | 'F' | 'O';
  EstadoCivil?: string;
  Email?: string;
  Telefone?: string;
  Endereco?: string;
  DataAdmissao?: string;
  EstadoFuncionario?: 'Activo' | 'Inactivo' | 'Suspenso';
  Foto?: string;
  CargoID?: number;
  DepartamentoID?: number;
  // Campos procesados por el frontend
  CargoNome?: string;
  DepartamentoNome?: string;
  cargo?: { nome: string };
  departamento?: { nome: string };
}

export interface FuncionarioFormData {
  nome: string;
  apelido: string;
  bi: string;
  dataNascimento?: string;
  sexo?: 'M' | 'F' | 'O';
  estadoCivil?: string;
  email?: string;
  telefone?: string;
  endereco?: string;
  dataAdmissao: string;
  estadoFuncionario: 'Activo' | 'Inactivo' | 'Suspenso';
  cargoID?: number;
  departamentoID?: number;
}

// Departamento
export interface Departamento extends BaseEntity {
  departamentoID: number;
  nome: string;
  descricao?: string;
}

export interface DepartamentoFormData {
  nome: string;
  descricao?: string;
}

// Cargo
export interface Cargo extends BaseEntity {
  cargoID: number;
  nome: string;
  descricao?: string;
  nivel?: string;
  departamentoID?: number;
}

export interface CargoFormData {
  nome: string;
  descricao?: string;
  nivel?: string;
  departamentoID?: number;
}

// Presença
export interface Presenca extends BaseEntity {
  presencaID: number;
  funcionarioID: number;
  data: string;
  horaEntrada?: string;
  horaSaida?: string;
  observacao?: string;
  funcionario?: Funcionario;
}

export interface PresencaFormData {
  funcionarioID: number;
  data: string;
  horaEntrada?: string;
  horaSaida?: string;
  observacao?: string;
}

// Licença
export interface Licenca extends BaseEntity {
  licencaID: number;
  funcionarioID: number;
  tipo: 'Ferias' | 'Medica' | 'Maternidade' | 'Paternidade' | 'Outras';
  dataInicio: string;
  dataFim: string;
  motivo?: string;
  estado: 'Pendente' | 'Aprovada' | 'Rejeitada';
  funcionario?: Funcionario;
}

export interface LicencaFormData {
  funcionarioID: number;
  tipo: 'Ferias' | 'Medica' | 'Maternidade' | 'Paternidade' | 'Outras';
  dataInicio: string;
  dataFim: string;
  motivo?: string;
  estado: 'Pendente' | 'Aprovada' | 'Rejeitada';
}

// Avaliação
export interface Avaliacao extends BaseEntity {
  avaliacaoID: number;
  funcionarioID: number;
  dataAvaliacao: string;
  assiduidade: number; // 1-5
  competenciasTecnicas: number; // 1-5
  softSkills: number; // 1-5
  comentarios?: string;
  funcionario?: Funcionario;
}

export interface AvaliacaoFormData {
  funcionarioID: number;
  dataAvaliacao: string;
  assiduidade: number;
  competenciasTecnicas: number;
  softSkills: number;
  comentarios?: string;
}

// Folha Salarial
export interface FolhaSalarial extends BaseEntity {
  folhaID: number;
  funcionarioID: number;
  periodoInicio: string;
  periodoFim: string;
  salarioBase: number;
  bonificacoes: number;
  descontos: number;
  valorLiquido?: number;
  dataPagamento?: string;
  funcionario?: Funcionario;
}

export interface FolhaSalarialFormData {
  funcionarioID: number;
  periodoInicio: string;
  periodoFim: string;
  salarioBase: number;
  bonificacoes: number;
  descontos: number;
  dataPagamento?: string;
}

// Benefício
export interface Beneficio extends BaseEntity {
  beneficioID: number;
  nome: string;
  descricao?: string;
  tipo: 'Saude' | 'Transporte' | 'Alimentacao' | 'Seguro' | 'Outros';
}

export interface BeneficioFormData {
  nome: string;
  descricao?: string;
  tipo: 'Saude' | 'Transporte' | 'Alimentacao' | 'Seguro' | 'Outros';
}

// Funcionário-Benefício
export interface FuncionarioBeneficio extends BaseEntity {
  funcionarioBeneficioID: number;
  funcionarioID: number;
  beneficioID: number;
  dataInicio: string;
  dataFim?: string;
  estado: 'Activo' | 'Inactivo';
  funcionario?: Funcionario;
  beneficio?: Beneficio;
}

export interface FuncionarioBeneficioFormData {
  funcionarioID: number;
  beneficioID: number;
  dataInicio: string;
  dataFim?: string;
  estado: 'Activo' | 'Inactivo';
}

// API Response types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}

export interface PaginatedResponse<T> {
  success: boolean;
  data: T[];
  total: number;
  page: number;
  per_page: number;
  pages: number;
}

// Dashboard Metrics
export interface DashboardMetrics {
  funcionariosAtivos: number;
  funcionariosInativos: number;
  ultimasContratacoes: number;
  licencasAtivas: number;
  proximasAvaliacoes: number;
  totalFuncionarios: number;
}

// Chart data
export interface ChartData {
  name: string;
  value: number;
  color?: string;
}

// Filtros
export interface FuncionarioFilter {
  nome?: string;
  cargo?: string;
  departamento?: string;
  estado?: string;
  page?: number;
  per_page?: number;
}

export interface PresencaFilter {
  funcionarioID?: number;
  departamentoID?: number;
  dataInicio?: string;
  dataFim?: string;
  search?: string;
  page?: number;
  per_page?: number;
}

export interface LicencaFilter {
  funcionarioID?: number;
  tipo?: string;
  estado?: string;
  dataInicio?: string;
  dataFim?: string;
  page?: number;
  per_page?: number;
}
