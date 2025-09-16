#!/usr/bin/env python3
"""
Script para iniciar el servidor Flask y probar el endpoint
"""

import sys
import os
import requests
import time
import threading
import signal
from flask import Flask

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_endpoint_with_server():
    """Iniciar servidor y probar endpoint"""
    from app import create_app
    
    print("=== INICIANDO SERVIDOR FLASK ===")
    app = create_app()
    
    # Función para probar el endpoint
    def test_endpoint():
        time.sleep(2)  # Esperar que el servidor inicie
        try:
            print("\n=== PROBANDO ENDPOINT ===")
            response = requests.get('http://localhost:5000/api/iamc/dashboard/metrics', timeout=10)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✓ SUCCESS!")
                
                if 'metrics' in data:
                    metrics = data['metrics']
                    print(f"✓ Total Funcionários: {metrics.get('totalFuncionarios', 'N/A')}")
                    print(f"✓ Funcionários Ativos: {metrics.get('funcionariosAtivos', 'N/A')}")
                    print(f"✓ Funcionários Inativos: {metrics.get('funcionariosInativos', 'N/A')}")
                    
                    print(f"\n✓ Funcionários por Departamento:")
                    for dept in metrics.get('funcionariosPorDepartamento', []):
                        print(f"  - {dept['nome']}: {dept['total']}")
                else:
                    print(f"Response Data: {data}")
            else:
                print(f"❌ ERROR: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"Erro ao testar endpoint: {e}")
        finally:
            # Parar o servidor
            os._exit(0)
    
    # Iniciar thread para teste
    test_thread = threading.Thread(target=test_endpoint)
    test_thread.daemon = True
    test_thread.start()
    
    # Iniciar servidor
    try:
        print("Servidor iniciando em http://localhost:5000")
        app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)
    except KeyboardInterrupt:
        print("\nServidor parado.")

if __name__ == '__main__':
    test_endpoint_with_server()
