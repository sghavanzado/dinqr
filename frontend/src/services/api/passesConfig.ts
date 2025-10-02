/**
 * API Service para Configurações Avançadas de Passes
 * Gerenciamento completo de temas e formatos com controle de layout, tipografia e elementos gráficos
 */

import type { 
  TemaAvancado, 
  FormatoAvancado, 
  ConfiguracaoAvancada, 
  MedidaPadrao 
} from './passesConfigTypes';

const API_BASE = '/api/iamc/passes';

// Re-export types for convenience
export type { TemaAvancado, FormatoAvancado, ConfiguracaoAvancada, MedidaPadrao };

// ===== SERVIÇOS PARA TEMAS AVANÇADOS =====

export const temasAvancadosService = {
  // Listar todos os temas
  async listar(): Promise<{ temas: TemaAvancado[]; total: number }> {
    const response = await fetch(`${API_BASE}/temas`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Erro ao carregar temas');
    }

    const data = await response.json();
    return data.data;
  },

  // Obter tema por ID
  async obterPorId(id: number): Promise<TemaAvancado> {
    const response = await fetch(`${API_BASE}/temas/${id}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Erro ao carregar tema');
    }

    const data = await response.json();
    return data.data;
  },

  // Criar novo tema
  async criar(tema: Omit<TemaAvancado, 'id' | 'data_criacao' | 'data_atualizacao'>): Promise<{ id: number; message: string }> {
    const response = await fetch(`${API_BASE}/temas`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(tema),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Erro ao criar tema');
    }

    const data = await response.json();
    return data.data;
  },

  // Atualizar tema
  async atualizar(id: number, tema: Omit<TemaAvancado, 'id' | 'data_criacao' | 'data_atualizacao'>): Promise<{ message: string }> {
    const response = await fetch(`${API_BASE}/temas/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(tema),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Erro ao atualizar tema');
    }

    const data = await response.json();
    return data.data;
  },

  // Deletar tema
  async deletar(id: number): Promise<{ message: string }> {
    const response = await fetch(`${API_BASE}/temas/${id}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Erro ao deletar tema');
    }

    const data = await response.json();
    return data.data;
  },

  // Duplicar tema
  async duplicar(id: number, novoNome: string): Promise<{ id: number; message: string }> {
    const temaOriginal = await this.obterPorId(id);
    const temaDuplicado = {
      ...temaOriginal,
      nome: novoNome,
    };
    delete (temaDuplicado as any).id;
    delete (temaDuplicado as any).data_criacao;
    delete (temaDuplicado as any).data_atualizacao;
    
    return this.criar(temaDuplicado);
  },
};

// ===== SERVIÇOS PARA FORMATOS AVANÇADOS =====

export const formatosAvancadosService = {
  // Listar todos os formatos
  async listar(): Promise<{ formatos: FormatoAvancado[]; total: number; medidas_padrao: Record<string, MedidaPadrao> }> {
    const response = await fetch(`${API_BASE}/formatos`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Erro ao carregar formatos');
    }

    const data = await response.json();
    return data.data;
  },

  // Obter formato por ID
  async obterPorId(id: number): Promise<FormatoAvancado> {
    const response = await fetch(`${API_BASE}/formatos/${id}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Erro ao carregar formato');
    }

    const data = await response.json();
    return data.data;
  },

  // Criar novo formato
  async criar(formato: Omit<FormatoAvancado, 'id' | 'data_criacao' | 'data_atualizacao'>): Promise<{ id: number; message: string }> {
    const response = await fetch(`${API_BASE}/formatos`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formato),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Erro ao criar formato');
    }

    const data = await response.json();
    return data.data;
  },

  // Atualizar formato
  async atualizar(id: number, formato: Omit<FormatoAvancado, 'id' | 'data_criacao' | 'data_atualizacao'>): Promise<{ message: string }> {
    const response = await fetch(`${API_BASE}/formatos/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formato),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Erro ao atualizar formato');
    }

    const data = await response.json();
    return data.data;
  },

  // Deletar formato
  async deletar(id: number): Promise<{ message: string }> {
    const response = await fetch(`${API_BASE}/formatos/${id}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Erro ao deletar formato');
    }

    const data = await response.json();
    return data.data;
  },

  // Aplicar medida padrão
  async aplicarMedidaPadrao(medidaTipo: string): Promise<Partial<FormatoAvancado>> {
    const response = await this.listar();
    const medida = response.medidas_padrao[medidaTipo];
    
    if (!medida) {
      throw new Error('Medida padrão não encontrada');
    }

    return {
      largura: medida.largura,
      altura: medida.altura,
      orientacao: medida.largura > medida.altura ? 'horizontal' : 'vertical'
    };
  },
};

// ===== SERVIÇO PARA CONFIGURAÇÃO GERAL AVANÇADA =====

export const configuracaoAvancadaService = {
  // Obter configuração completa
  async obter(): Promise<ConfiguracaoAvancada> {
    const response = await fetch(`${API_BASE}/configuracao`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Erro ao carregar configuração');
    }

    const data = await response.json();
    return data.data;
  },

  // Validar tema
  async validarTema(tema: Partial<TemaAvancado>): Promise<{ valido: boolean; erros: string[] }> {
    const erros: string[] = [];

    if (!tema.nome || tema.nome.trim().length === 0) {
      erros.push('Nome do tema é obrigatório');
    }

    if (!tema.cor_primaria || !tema.cor_primaria.match(/^#[0-9A-Fa-f]{6}$/)) {
      erros.push('Cor primária deve ser um código hexadecimal válido');
    }

    if (tema.fundo_opacidade !== undefined && (tema.fundo_opacidade < 0 || tema.fundo_opacidade > 1)) {
      erros.push('Opacidade do fundo deve estar entre 0 e 1');
    }

    if (tema.tamanho_fonte_titulo !== undefined && (tema.tamanho_fonte_titulo < 6 || tema.tamanho_fonte_titulo > 24)) {
      erros.push('Tamanho da fonte do título deve estar entre 6 e 24');
    }

    return {
      valido: erros.length === 0,
      erros
    };
  },

  // Validar formato
  async validarFormato(formato: Partial<FormatoAvancado>): Promise<{ valido: boolean; erros: string[] }> {
    const erros: string[] = [];

    if (!formato.nome || formato.nome.trim().length === 0) {
      erros.push('Nome do formato é obrigatório');
    }

    if (!formato.extensao || !['pdf', 'html', 'png', 'svg'].includes(formato.extensao)) {
      erros.push('Extensão deve ser pdf, html, png ou svg');
    }

    if (formato.largura !== undefined && (formato.largura < 10 || formato.largura > 200)) {
      erros.push('Largura deve estar entre 10mm e 200mm');
    }

    if (formato.altura !== undefined && (formato.altura < 10 || formato.altura > 200)) {
      erros.push('Altura deve estar entre 10mm e 200mm');
    }

    if (formato.dpi !== undefined && (formato.dpi < 72 || formato.dpi > 600)) {
      erros.push('DPI deve estar entre 72 e 600');
    }

    if (formato.qualidade !== undefined && (formato.qualidade < 1 || formato.qualidade > 100)) {
      erros.push('Qualidade deve estar entre 1 e 100');
    }

    return {
      valido: erros.length === 0,
      erros
    };
  },
};

// ===== UTILITÁRIOS =====

export const passesConfigUtils = {
  // Converter mm para pixels
  mmToPixels: (mm: number, dpi: number = 300): number => {
    return Math.round((mm * dpi) / 25.4);
  },

  // Converter pixels para mm
  pixelsToMm: (pixels: number, dpi: number = 300): number => {
    return Math.round((pixels * 25.4) / dpi * 100) / 100;
  },

  // Obter razão de aspecto
  getAspectRatio: (largura: number, altura: number): string => {
    const gcd = (a: number, b: number): number => b === 0 ? a : gcd(b, a % b);
    const divisor = gcd(largura * 100, altura * 100);
    const ratioW = (largura * 100) / divisor;
    const ratioH = (altura * 100) / divisor;
    return `${ratioW}:${ratioH}`;
  },

  // Gerar preview de cor
  gerarPreviewCor: (tema: TemaAvancado): string => {
    if (tema.fundo_tipo === 'gradiente') {
      return `linear-gradient(45deg, ${tema.fundo_cor}, ${tema.fundo_cor_gradiente})`;
    }
    return tema.fundo_cor;
  },

  // Calcular área em mm²
  calcularArea: (largura: number, altura: number): number => {
    return Math.round(largura * altura * 100) / 100;
  },

  // Obter informações de formato
  getFormatoInfo: (formato: FormatoAvancado): string => {
    const area = passesConfigUtils.calcularArea(formato.largura, formato.altura);
    const ratio = passesConfigUtils.getAspectRatio(formato.largura, formato.altura);
    return `${formato.largura}×${formato.altura}mm (${area}mm², ${ratio})`;
  },
};

// ===== CONSTANTS EXPORT =====
export const MEDIDAS_PADRAO = {
  'CR80': { largura: 85.6, altura: 53.98, descricao: 'Cartão de crédito padrão' },
  'CR100': { largura: 98.5, altura: 67.0, descricao: 'Cartão grande' },
  'BUSINESS': { largura: 89.0, altura: 51.0, descricao: 'Cartão de visita' },
  'BADGE': { largura: 76.2, altura: 101.6, descricao: 'Crachá vertical' },
  'MINI': { largura: 70.0, altura: 45.0, descricao: 'Mini cartão' },
};

export default {
  temasAvancadosService,
  formatosAvancadosService,
  configuracaoAvancadaService,
  passesConfigUtils,
};
