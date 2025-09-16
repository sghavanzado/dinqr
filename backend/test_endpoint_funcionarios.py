#!/usr/bin/env python3
"""
Test específico del endpoint de funcionários
"""

import requests
import json
import time

def test_funcionarios_endpoint():
    """Test específico do endpoint de funcionários"""
    base_url = "http://localhost:5000"
    
    print("=" * 60)
    print("TESTE DO ENDPOINT DE FUNCIONÁRIOS")
    print("=" * 60)
    
    # Test 1: Status IAMC
    print("\n1. Testando /api/iamc/status...")
    try:
        response = requests.get(f"{base_url}/api/iamc/status", timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Test 2: Lista funcionários
    print("\n2. Testando /api/iamc/funcionarios...")
    try:
        response = requests.get(f"{base_url}/api/iamc/funcionarios", timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        print(f"   Response: {response.text[:500]}...")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   ✅ JSON válido")
                print(f"   Chaves: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                if isinstance(data, dict) and 'funcionarios' in data:
                    print(f"   Total funcionários: {len(data['funcionarios'])}")
                elif isinstance(data, dict) and 'data' in data:
                    print(f"   Total funcionários: {len(data['data'])}")
            except json.JSONDecodeError as e:
                print(f"   ❌ JSON inválido: {e}")
        else:
            print(f"   ❌ Status code não é 200")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Test 3: Lista funcionários com paginação
    print("\n3. Testando /api/iamc/funcionarios com paginação...")
    try:
        response = requests.get(f"{base_url}/api/iamc/funcionarios?page=1&per_page=5", timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:300]}...")
    except Exception as e:
        print(f"   ❌ Erro: {e}")

if __name__ == "__main__":
    test_funcionarios_endpoint()
