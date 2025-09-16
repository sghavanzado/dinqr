#!/usr/bin/env python3
"""
Script para probar el endpoint dashboard metrics sin servidor
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controllers.iamc_funcionarios_controller_new import FuncionarioController

def test_endpoint():
    """Probar el método dashboard_metrics del controlador"""
    try:
        print("=== TESTE DO ENDPOINT DASHBOARD METRICS ===")
        response, status_code = FuncionarioController.dashboard_metrics()
        
        print(f"Status Code: {status_code}")
        print(f"Response Type: {type(response)}")
        
        if hasattr(response, 'get_json'):
            data = response.get_json()
        else:
            # Pode ser que seja um dict direto ou um response object
            data = response if isinstance(response, dict) else None
            
        if data:
            print(f"Response Data: {data}")
            
            if 'metrics' in data:
                metrics = data['metrics']
                print(f"\n✓ Total Funcionários: {metrics.get('totalFuncionarios', 'N/A')}")
                print(f"✓ Funcionários Ativos: {metrics.get('funcionariosAtivos', 'N/A')}")
                print(f"✓ Funcionários Inativos: {metrics.get('funcionariosInativos', 'N/A')}")
                
                print(f"\n✓ Funcionários por Departamento:")
                for dept in metrics.get('funcionariosPorDepartamento', []):
                    print(f"  - {dept['nome']}: {dept['total']}")
                    
                print(f"\n✓ Funcionários por Estado:")
                for estado in metrics.get('funcionariosPorEstado', []):
                    print(f"  - {estado['estado']}: {estado['total']}")
        else:
            print("Erro: Resposta inválida")
            
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_endpoint()
