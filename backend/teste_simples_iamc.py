#!/usr/bin/env python3
"""
Teste simples dos endpoints IAMC principais.
"""

from flask import Flask
from app import app

def test_main_endpoints():
    """Testa os principais endpoints."""
    
    with app.test_client() as client:
        print("🧪 Teste Simples IAMC")
        print("=" * 40)
        
        endpoints = [
            '/api/iamc/status',
            '/api/iamc/funcionarios',
            '/api/iamc/departamentos'
        ]
        
        for endpoint in endpoints:
            try:
                print(f"\n📡 {endpoint}")
                response = client.get(endpoint)
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.get_json()
                    if isinstance(data, list):
                        print(f"   ✅ {len(data)} registros")
                    else:
                        print(f"   ✅ Dados OK")
                else:
                    print(f"   ❌ Erro: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Exceção: {e}")
        
        print("\n" + "=" * 40)

if __name__ == "__main__":
    with app.app_context():
        test_main_endpoints()
