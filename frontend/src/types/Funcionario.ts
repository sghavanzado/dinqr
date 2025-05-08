export interface Funcionario {
  id: number; // Ensure `id` is consistently a number
  nome: string;
  funcao?: string;
  area?: string;
  nif?: string;
  telefone?: string;
  uo?: string; // Adicionar unidad organizacional
}
