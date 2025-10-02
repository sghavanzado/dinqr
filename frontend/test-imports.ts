/**
 * Test file to verify imports work correctly
 */

import { 
  TemaAvancado, 
  FormatoAvancado, 
  ConfiguracaoAvancada,
  configuracaoAvancadaService,
  temasAvancadosService,
  formatosAvancadosService,
  passesConfigUtils,
  MEDIDAS_PADRAO
} from './src/services/api/passesConfig';

console.log('✅ All imports successful!');
console.log('Available services:', {
  configuracaoAvancadaService,
  temasAvancadosService,
  formatosAvancadosService,
  passesConfigUtils,
  MEDIDAS_PADRAO
});

export default {};
