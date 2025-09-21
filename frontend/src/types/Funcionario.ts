export interface Funcionario {
  id: number; // Ensure `id` is consistently a number
  nome: string;
  funcao?: string;
  area?: string;
  nif?: string;
  telefone?: string;
  unineg?: string; // Adicionar unidad organizacional
}

// Dashboard funcionario with IAMC data structure
export interface DashboardFuncionario {
  id: number;
  funcionarioId: number;
  nome: string;
  apelido: string;
  email: string;
  telefone: string;
  cargo: string;
  cargoId?: number;
  departamento: string;
  departamentoId?: number;
  qrGenerated: boolean;
}
