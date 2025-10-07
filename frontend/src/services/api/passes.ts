

export interface PassRequest {
  funcionario_id: number;
  incluir_qr?: boolean;
  data_validade?: string;
  // Campos legados (compatibilidade)
  tema?: 'default' | 'dark' | 'green' | 'orange';
  formato_saida?: 'pdf' | 'html';
  // Novos campos avançados
  tema_id?: number;
  formato_id?: number;
}

export interface PassConfig {
  temas_disponiveis: Array<{
    id: string;
    nome: string;
    cor_primaria: string;
  }>;
  formatos_saida: Array<{
    id: string;
    nome: string;
    descricao: string;
  }>;
  dimensoes: {
    formato: string;
    largura_mm: number;
    altura_mm: number;
    dpi_recomendado: number;
  };
  validade_padrao_dias: number;
}

/**
 * Gera um passe individual para um funcionário
 */
export const gerarPasse = async (request: PassRequest) => {
  try {
    const response = await fetch('/api/iamc/passes/gerar', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // Return the PDF blob directly
    return await response.blob();
  } catch (error) {
    console.error('Erro ao gerar passe:', error);
    throw error;
  }
};

/**
 * Gera uma pré-visualização do passe para um funcionário
 */
export const previewPasse = async (funcionarioId: number) => {
  try {
    // Try the new endpoint first, fallback to old one if it fails
    let response;
    try {
      response = await fetch(`/api/iamc/passes/preview-new/${funcionarioId}`, {
        method: 'GET',
      });
    } catch {
      // Fallback to original endpoint
      response = await fetch(`/api/iamc/passes/preview/${funcionarioId}`, {
        method: 'GET',
      });
    }

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // Check content type - if HTML, return text, if PDF return blob
    const contentType = response.headers.get('content-type') || '';
    if (contentType.includes('text/html')) {
      return await response.text();
    } else {
      return await response.blob();
    }
  } catch (error) {
    console.error('Erro ao gerar preview do passe:', error);
    throw error;
  }
};

/**
 * Gera passes em lote para múltiplos funcionários
 */
export const gerarPassesLote = async (funcionarioIds: number[], options?: {
  incluir_qr?: boolean;
  tema?: string;
  formato_saida?: string;
}) => {
  try {
    const response = await fetch('/api/iamc/passes/lote', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        funcionario_ids: funcionarioIds,
        ...options
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // Return the ZIP blob directly
    return await response.blob();
  } catch (error) {
    console.error('Erro ao gerar passes em lote:', error);
    throw error;
  }
};

/**
 * Obtém a configuração disponível para geração de passes
 */
export const getPassesConfig = async (): Promise<PassConfig> => {
  try {
    // Try the main endpoint first
    let response;
    try {
      response = await fetch('/api/iamc/passes/configuracao', {
        method: 'GET',
      });
    } catch (mainError) {
      // If main endpoint fails, try the safe fallback
      console.warn('Main config endpoint failed, trying safe fallback:', mainError);
      response = await fetch('/api/iamc/passes/configuracao-safe', {
        method: 'GET',
      });
    }

    // If main endpoint returns 500, try safe fallback
    if (!response.ok && response.status === 500) {
      console.warn('Main config endpoint returned 500, trying safe fallback');
      response = await fetch('/api/iamc/passes/configuracao-safe', {
        method: 'GET',
      });
    }

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data.data;
  } catch (error) {
    console.error('Erro ao carregar configuração de passes:', error);
    throw error;
  }
};
