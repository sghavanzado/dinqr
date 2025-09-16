#!/usr/bin/env python3
"""
Script de diagnóstico para verificar por que la lista de funcionários está vacía
"""

import requests
import json
import sys
import os

def verificar_backend_funcionando():
    """Verifica se o backend está rodando"""
    print("🔍 Verificando se o backend está rodando...")
    
    try:
        response = requests.get("http://localhost:5000/api/iamc/status", timeout=5)
        if response.status_code == 200:
            print("   ✅ Backend está rodando")
            return True
        else:
            print(f"   ❌ Backend retornou status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ Backend não está rodando em http://localhost:5000")
        return False
    except Exception as e:
        print(f"   ❌ Erro: {str(e)}")
        return False

def verificar_endpoint_funcionarios():
    """Verifica o endpoint de funcionários detalhadamente"""
    print("\n👥 Verificando endpoint de funcionários...")
    
    try:
        # Testar endpoint básico
        response = requests.get("http://localhost:5000/api/iamc/funcionarios", timeout=10)
        print(f"   📡 Status Code: {response.status_code}")
        print(f"   📋 Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   📄 Tipo de resposta: {type(data)}")
                print(f"   🔧 Estrutura da resposta: {list(data.keys()) if isinstance(data, dict) else 'Lista' if isinstance(data, list) else 'Outro'}")
                
                if isinstance(data, dict):
                    # Estrutura esperada: {"success": true, "data": [...], "total": X}
                    if 'success' in data:
                        print(f"   ✅ Campo 'success': {data.get('success')}")
                    if 'data' in data:
                        funcionarios = data.get('data', [])
                        print(f"   📊 Total de funcionários: {len(funcionarios)}")
                        if funcionarios:
                            primeiro = funcionarios[0]
                            print(f"   👤 Exemplo de funcionário: {primeiro.get('nome', 'N/A')} - {primeiro.get('email', 'N/A')}")
                            print(f"   🔑 Campos disponíveis: {list(primeiro.keys())}")
                        else:
                            print("   ⚠️  Lista de funcionários está vazia")
                    if 'total' in data:
                        print(f"   🔢 Total reportado: {data.get('total')}")
                else:
                    print(f"   ⚠️  Resposta não é um objeto: {data[:100] if isinstance(data, str) else str(data)[:100]}")
                
                return True
                
            except json.JSONDecodeError:
                print(f"   ❌ Resposta não é JSON válido: {response.text[:200]}")
                return False
        else:
            print(f"   ❌ Erro HTTP: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro na requisição: {str(e)}")
        return False

def verificar_backend_database():
    """Verifica se o backend consegue conectar ao banco"""
    print("\n💾 Verificando conexão com banco de dados...")
    
    try:
        # Importar o backend localmente
        sys.path.insert(0, 'backend')
        from extensions import get_iamc_connection
        
        conn = get_iamc_connection()
        if conn:
            cursor = conn.cursor()
            
            # Verificar se a tabela funcionarios existe
            cursor.execute("""
                SELECT COUNT(*) 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_NAME = 'funcionarios'
            """)
            table_exists = cursor.fetchone()[0]
            print(f"   📋 Tabela 'funcionarios' existe: {'✅ Sim' if table_exists else '❌ Não'}")
            
            if table_exists:
                # Contar funcionários na tabela
                cursor.execute("SELECT COUNT(*) FROM funcionarios")
                count = cursor.fetchone()[0]
                print(f"   👥 Total de funcionários na tabela: {count}")
                
                if count > 0:
                    # Mostrar alguns exemplos
                    cursor.execute("SELECT TOP 3 funcionarioID, nome, email, estadoFuncionario FROM funcionarios")
                    examples = cursor.fetchall()
                    print("   📝 Exemplos de funcionários:")
                    for example in examples:
                        print(f"      • ID: {example[0]}, Nome: {example[1]}, Email: {example[2]}, Estado: {example[3]}")
            
            cursor.close()
            conn.close()
            return True
        else:
            print("   ❌ Não foi possível conectar ao banco IAMC")
            return False
            
    except ImportError:
        print("   ⚠️  Não foi possível importar módulos do backend")
        return False
    except Exception as e:
        print(f"   ❌ Erro ao verificar banco: {str(e)}")
        return False

def verificar_cors():
    """Verifica se há problemas de CORS"""
    print("\n🔒 Verificando configuração CORS...")
    
    try:
        headers = {
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        
        response = requests.options("http://localhost:5000/api/iamc/funcionarios", 
                                 headers=headers, timeout=5)
        
        print(f"   📡 Preflight Status: {response.status_code}")
        cors_headers = {k: v for k, v in response.headers.items() if 'access-control' in k.lower()}
        print(f"   🔧 Headers CORS: {cors_headers}")
        
        if 'access-control-allow-origin' in response.headers:
            origin = response.headers['access-control-allow-origin']
            print(f"   ✅ CORS Origin permitido: {origin}")
            return True
        else:
            print("   ❌ CORS não configurado corretamente")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro na verificação CORS: {str(e)}")
        return False

def main():
    print("🚀 DIAGNÓSTICO: Lista de Funcionários Vazia")
    print("=" * 60)
    
    backend_ok = verificar_backend_funcionando()
    endpoint_ok = verificar_endpoint_funcionarios() if backend_ok else False
    db_ok = verificar_backend_database()
    cors_ok = verificar_cors() if backend_ok else False
    
    print("\n" + "=" * 60)
    print("📋 RESUMO DO DIAGNÓSTICO:")
    print(f"   Backend rodando: {'✅ OK' if backend_ok else '❌ FALHA'}")
    print(f"   Endpoint funcionários: {'✅ OK' if endpoint_ok else '❌ FALHA'}")
    print(f"   Banco de dados: {'✅ OK' if db_ok else '❌ FALHA'}")
    print(f"   Configuração CORS: {'✅ OK' if cors_ok else '❌ FALHA'}")
    
    print("\n💡 PRÓXIMOS PASSOS:")
    if not backend_ok:
        print("   1. Iniciar o backend: cd backend && python app.py")
    elif not endpoint_ok:
        print("   1. Verificar logs do backend para erros")
        print("   2. Verificar se as rotas estão registradas corretamente")
    elif not db_ok:
        print("   1. Verificar conexão com SQL Server IAMC")
        print("   2. Verificar se a tabela funcionarios tem dados")
    elif not cors_ok:
        print("   1. Verificar configuração CORS no backend")
    else:
        print("   1. Verificar console do navegador para erros JavaScript")
        print("   2. Verificar Network tab no DevTools")
    
    print("\n🔍 DEBUGGING ADICIONAL:")
    print("   1. Abrir DevTools no navegador (F12)")
    print("   2. Ir para a aba Console")
    print("   3. Recarregar a página de funcionários")
    print("   4. Verificar mensagens de log que começam com 🔍, 📊, ✅, ❌")

if __name__ == "__main__":
    main()
