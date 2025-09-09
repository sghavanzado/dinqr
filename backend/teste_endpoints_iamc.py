#!/usr/bin/env python3
"""
Script rápido para testar os endpoints IAMC com dados existentes.
"""

import requests
import json

BASE_URL = "http://localhost:5000/api/iamc"

def test_endpoint(endpoint, description):
    """Testa um endpoint específico."""
    try:
        url = f"{BASE_URL}/{endpoint}"
        print(f"\n📡 Testando {description}...")
        print(f"   URL: {url}")
        
        response = requests.get(url, timeout=10)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, list):
                    print(f"   ✅ Retornou {len(data)} registros")
                    if len(data) > 0:
                        print(f"   📄 Primeiro registro: {json.dumps(data[0], indent=2, default=str)}")
                else:
                    print(f"   ✅ Dados: {json.dumps(data, indent=2, default=str)}")
            except Exception as e:
                print(f"   ⚠️ Erro ao parsear JSON: {e}")
                print(f"   📄 Resposta bruta: {response.text[:200]}...")
        else:
            print(f"   ❌ Erro: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"   🚫 Servidor não está rodando ou endpoint inacessível")
    except Exception as e:
        print(f"   ❌ Erro inesperado: {e}")

def main():
    print("🧪 Teste Rápido dos Endpoints IAMC")
    print("=" * 50)
    
    # Lista de endpoints para testar
    endpoints = [
        ("status", "Status do sistema IAMC"),
        ("funcionarios", "Lista de funcionários"),
        ("departamentos", "Lista de departamentos"),
        ("cargos", "Lista de cargos"),
        ("presencas", "Lista de presenças"),
        ("beneficios", "Lista de benefícios"),
        ("funcionario-beneficios", "Associações funcionário-benefício"),
        ("folha-salarial", "Folhas salariais"),
        ("historico-cargo", "Histórico de cargos"),
    ]
    
    for endpoint, description in endpoints:
        test_endpoint(endpoint, description)
    
    print("\n" + "=" * 50)
    print("🏁 Teste concluído!")
    
    print("\n💡 Para testar manualmente:")
    print("   1. Certifique-se que o servidor Flask está rodando")
    print("   2. Acesse os endpoints no browser ou Postman")
    print("   3. Use a coleção Postman: IAMC_Postman_Collection_Melhorada.json")

if __name__ == "__main__":
    main()
