/**
 * Tipos para Configurações Avançadas de Passes
 */

export interface TemaAvancado {
  id?: number;
  nome: string;
  // Cores
  cor_primaria: string;
  cor_secundaria: string;
  cor_texto: string;
  cor_borda: string;
  // Layout
  layout_tipo: 'horizontal' | 'vertical' | 'compact';
  margem_superior: number;
  margem_inferior: number;
  margem_esquerda: number;
  margem_direita: number;
  // Tipografia
  fonte_titulo: string;
  tamanho_fonte_titulo: number;
  fonte_nome: string;
  tamanho_fonte_nome: number;
  fonte_cargo: string;
  tamanho_fonte_cargo: number;
  fonte_info: string;
  tamanho_fonte_info: number;
  // Elementos gráficos
  mostrar_logo: boolean;
  posicao_logo: 'superior_esquerda' | 'superior_direita' | 'superior_centro' | 'inferior_esquerda' | 'inferior_direita';
  tamanho_logo: number;
  mostrar_qr_borda: boolean;
  qr_tamanho: number;
  qr_posicao: 'direita' | 'esquerda' | 'centro';
  // Fundo
  fundo_tipo: 'solido' | 'gradiente' | 'imagem';
  fundo_cor: string;
  fundo_cor_gradiente: string;
  fundo_imagem_url: string;
  fundo_opacidade: number;
  // Estado
  ativo: boolean;
  data_criacao?: string;
  data_atualizacao?: string;
}

export interface FormatoAvancado {
  id?: number;
  nome: string;
  extensao: 'pdf' | 'html' | 'png' | 'svg';
  descricao: string;
  // Medidas (mm)
  largura: number;
  altura: number;
  dpi: number;
  orientacao: 'horizontal' | 'vertical';
  // Configurações
  qualidade: number;
  compressao: boolean;
  ativo: boolean;
  data_criacao?: string;
  data_atualizacao?: string;
}

export interface MedidaPadrao {
  largura: number;
  altura: number;
  descricao: string;
}

export interface ConfiguracaoAvancada {
  temas_disponiveis: Array<{
    id: number;
    nome: string;
    cor_primaria: string;
    cor_secundaria: string;
    cor_texto: string;
    layout_tipo: string;
  }>;
  formatos_saida: Array<{
    id: number;
    nome: string;
    extensao: string;
    descricao: string;
    largura: number;
    altura: number;
    dpi: number;
  }>;
  medidas_padrao: Record<string, MedidaPadrao>;
  opcoes_layout: Array<{ id: string; nome: string; descricao: string }>;
  opcoes_fonte: Array<{ id: string; nome: string }>;
  opcoes_fundo: Array<{ id: string; nome: string }>;
  validade_padrao_dias: number;
  versao_api: string;
}
