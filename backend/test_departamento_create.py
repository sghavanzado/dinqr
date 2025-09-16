#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script to verify departamento creation with camelCase data
"""

import requests
import json

def test_create_departamento():
    """Test creating a departamento with camelCase data"""
    
    url = "http://localhost:5000/api/iamc/departamentos"
    
    # Test data in camelCase (as sent by frontend)
    data = {
        "nome": "Departamento de Teste API",
        "descricao": "Departamento criado via teste de API"
    }
    
    print("🧪 Testando criação de departamento...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data)
        print(f"\n📊 Status Code: {response.status_code}")
        print(f"📄 Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            print("✅ Departamento criado com sucesso!")
            return True
        else:
            print("❌ Erro ao criar departamento")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar ao servidor backend")
        print("   Certifique-se de que o backend está rodando em localhost:5000")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")
        return False

if __name__ == "__main__":
    test_create_departamento()
