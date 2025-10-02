// Test script to verify passesConfig imports
import { 
  configuracaoAvancadaService,
  temasAvancadosService,
  formatosAvancadosService,
  passesConfigUtils,
  type ConfiguracaoAvancada,
  type TemaAvancado,
  type FormatoAvancado,
  MEDIDAS_PADRAO
} from './src/services/api/passesConfig';

// Test that all exports are available
console.log('Testing imports from passesConfig.ts:');
console.log('configuracaoAvancadaService:', typeof configuracaoAvancadaService);
console.log('temasAvancadosService:', typeof temasAvancadosService);
console.log('formatosAvancadosService:', typeof formatosAvancadosService);
console.log('passesConfigUtils:', typeof passesConfigUtils);
console.log('MEDIDAS_PADRAO:', typeof MEDIDAS_PADRAO);

// Test type usage
const testConfig: ConfiguracaoAvancada = {} as ConfiguracaoAvancada;
const testTema: TemaAvancado = {} as TemaAvancado;
const testFormato: FormatoAvancado = {} as FormatoAvancado;

console.log('Types are properly imported:', typeof testConfig, typeof testTema, typeof testFormato);

export {};
