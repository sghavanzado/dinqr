#!/usr/bin/env python3
"""
Script de teste para verificar se o backend está funcionando corretamente
com a integração IAMC para funcionários.
"""

import sys
import os
import requests
import json
from datetime import datetime

# Adicionar o diretório do backend ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_backend_endpoints():
    """Testa os endpoints do backend"""
    base_url = "http://localhost:5000"
    
    print("🔍 Testando Backend IAMC - Funcionários")
    print("=" * 50)
    
    endpoints = [
        ("/api/iamc/status", "GET", "Status do módulo IAMC"),
        ("/api/iamc/funcionarios", "GET", "Listar funcionários"),
        ("/api/iamc/departamentos", "GET", "Listar departamentos"),
        ("/api/iamc/cargos", "GET", "Listar cargos"),
    ]
    
    for endpoint, method, description in endpoints:
        print(f"\n📍 Testando: {description}")
        print(f"   {method} {endpoint}")
        
        try:
            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}", timeout=10)
            else:
                response = requests.request(method, f"{base_url}{endpoint}", timeout=10)
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and data.get('success'):
                    print(f"   ✅ Sucesso: {data.get('message', 'OK')}")
                    if 'data' in data:
                        print(f"   📊 Total de registros: {len(data['data']) if isinstance(data['data'], list) else 'N/A'}")
                else:
                    print(f"   ⚠️  Resposta: {response.text[:100]}...")
            else:
                print(f"   ❌ Erro: {response.text[:100]}...")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Erro de conexão: Servidor não está rodando em {base_url}")
        except requests.exceptions.Timeout:
            print(f"   ❌ Timeout: Servidor demorou muito para responder")
        except Exception as e:
            print(f"   ❌ Erro: {str(e)}")

def test_frontend_integration():
    """Testa se o frontend está rodando"""
    print(f"\n🌐 Testando Frontend")
    print("=" * 30)
    
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Frontend está rodando")
        else:
            print("   ⚠️  Frontend retornou status diferente de 200")
    except requests.exceptions.ConnectionError:
        print("   ❌ Frontend não está rodando em http://localhost:3000")
    except Exception as e:
        print(f"   ❌ Erro: {str(e)}")

def test_database_connection():
    """Testa a conexão com o banco de dados"""
    print(f"\n💾 Testando Conexão com Banco de Dados")
    print("=" * 40)
    
    try:
        # Importar e testar as conexões do database
        from extensions import get_iamc_connection
        
        conn = get_iamc_connection()
        if conn:
            cursor = conn.cursor()
            
            # Teste básico de conexão
            cursor.execute("SELECT 1 AS test")
            result = cursor.fetchone()
            if result and result[0] == 1:
                print("   ✅ Conexão com banco IAMC: OK")
            
            # Teste de contagem de funcionários
            cursor.execute("SELECT COUNT(*) FROM funcionarios")
            count = cursor.fetchone()[0]
            print(f"   📊 Total de funcionários no banco: {count}")
            
            cursor.close()
            conn.close()
        else:
            print("   ❌ Falha ao conectar com banco IAMC")
            
    except Exception as e:
        print(f"   ❌ Erro na conexão com banco: {str(e)}")

if __name__ == "__main__":
    print(f"🚀 Teste de Integração DINQR - RRHH")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Testar banco de dados primeiro
    test_database_connection()
    
    # Testar endpoints do backend
    test_backend_endpoints()
    
    # Testar frontend
    test_frontend_integration()
    
    print("\n" + "=" * 60)
    print("🏁 Teste concluído!")
    print("\n💡 Se todos os testes passaram, a integração está funcionando!")
    print("   Acesse: http://localhost:3000/rrhh/funcionarios")
