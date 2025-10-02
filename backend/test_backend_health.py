#!/usr/bin/env python3
"""
Script para verificar el estado del backend y los endpoints de passes
"""

import requests
import json
import sys
import os

def test_backend():
    """Testa la conectividad del backend"""
    base_url = "http://localhost:5000"
    
    print("=== VERIFICACIÓN DEL BACKEND ===")
    
    # Test de health check general
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"✅ Health check: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check falló: {e}")
        return False
    
    # Test de endpoints específicos de passes
    endpoints = [
        "/api/iamc/passes/configuracao",
        "/api/iamc/passes/temas", 
        "/api/iamc/passes/formatos"
    ]
    
    print("\n=== TESTE DE ENDPOINTS DE PASSES ===")
    
    for endpoint in endpoints:
        try:
            url = f"{base_url}{endpoint}"
            print(f"\n🔄 Testando: {url}")
            
            response = requests.get(url, timeout=10)
            print(f"📊 Status: {response.status_code}")
            print(f"📋 Content-Type: {response.headers.get('content-type', 'N/A')}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"✅ JSON válido recebido")
                    if 'data' in data:
                        print(f"📦 Dados disponíveis: {type(data['data'])}")
                    else:
                        print(f"📦 Resposta: {list(data.keys()) if isinstance(data, dict) else type(data)}")
                except json.JSONDecodeError:
                    print(f"❌ Resposta não é JSON válido")
                    print(f"📄 Primeiros 200 chars: {response.text[:200]}")
            else:
                print(f"❌ Status não OK: {response.status_code}")
                print(f"📄 Resposta: {response.text[:200]}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro na requisição: {e}")
    
    return True

if __name__ == "__main__":
    print("Verificando backend...")
    test_backend()
