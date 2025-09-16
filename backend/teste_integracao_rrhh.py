#!/usr/bin/env python3
"""
Script para testar a integração completa RRHH com backend e frontend
Verifica conexões, endpoints e dados de exemplo
"""

import sys
import os
import requests
import json
from datetime import datetime

# Configuração
BASE_URL = "http://localhost:5000"
IAMC_API = f"{BASE_URL}/api/iamc"

def test_iamc_status():
    """Testar status geral do módulo IAMC"""
    print("🔍 Testando status IAMC...")
    try:
        response = requests.get(f"{IAMC_API}/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status IAMC: {data.get('status')}")
            return True
        else:
            print(f"❌ Erro no status IAMC: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao conectar com IAMC: {str(e)}")
        return False

def test_funcionarios_endpoints():
    """Testar endpoints de funcionários"""
    print("\n👥 Testando endpoints de funcionários...")
    
    # Test listar funcionários
    try:
        response = requests.get(f"{IAMC_API}/funcionarios", timeout=10)
        if response.status_code == 200:
            data = response.json()
            total = data.get('total', 0)
            print(f"✅ Listagem funcionários: {total} registros encontrados")
        else:
            print(f"❌ Erro na listagem de funcionários: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao listar funcionários: {str(e)}")
        return False
    
    return True

def test_dashboard_metrics():
    """Testar métricas do dashboard"""
    print("\n📊 Testando métricas do dashboard...")
    
    try:
        response = requests.get(f"{IAMC_API}/dashboard/metrics", timeout=10)
        if response.status_code == 200:
            data = response.json()
            metrics = data.get('metrics', {})
            print(f"✅ Dashboard metrics:")
            print(f"   - Total funcionários: {metrics.get('totalFuncionarios', 0)}")
            print(f"   - Funcionários ativos: {metrics.get('funcionariosAtivos', 0)}")
            print(f"   - Funcionários inativos: {metrics.get('funcionariosInativos', 0)}")
            return True
        else:
            print(f"❌ Erro nas métricas do dashboard: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao obter métricas: {str(e)}")
        return False

def test_departamentos():
    """Testar endpoints de departamentos"""
    print("\n🏢 Testando endpoints de departamentos...")
    
    try:
        response = requests.get(f"{IAMC_API}/departamentos", timeout=10)
        if response.status_code == 200:
            data = response.json()
            departamentos = data.get('departamentos', [])
            print(f"✅ Departamentos: {len(departamentos)} registros encontrados")
            return True
        else:
            print(f"❌ Erro na listagem de departamentos: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao listar departamentos: {str(e)}")
        return False

def test_presencas():
    """Testar endpoints de presenças"""
    print("\n📅 Testando endpoints de presenças...")
    
    try:
        response = requests.get(f"{IAMC_API}/presencas", timeout=10)
        if response.status_code == 200:
            data = response.json()
            presencas = data.get('data', [])
            print(f"✅ Presenças: {len(presencas)} registros encontrados")
            return True
        else:
            print(f"❌ Erro na listagem de presenças: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao listar presenças: {str(e)}")
        return False

def test_licencas():
    """Testar endpoints de licenças"""
    print("\n🏖️ Testando endpoints de licenças...")
    
    try:
        response = requests.get(f"{IAMC_API}/licencas", timeout=10)
        if response.status_code == 200:
            data = response.json()
            licencas = data.get('data', [])
            print(f"✅ Licenças: {len(licencas)} registros encontrados")
            return True
        else:
            print(f"❌ Erro na listagem de licenças: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao listar licenças: {str(e)}")
        return False

def main():
    """Função principal para executar todos os testes"""
    print("🚀 TESTE DE INTEGRAÇÃO RRHH - BACKEND E FRONTEND")
    print("=" * 60)
    print(f"📅 Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Base URL: {BASE_URL}")
    print(f"🔗 IAMC API: {IAMC_API}")
    print("=" * 60)
    
    success_count = 0
    total_tests = 6
    
    # Executar testes
    tests = [
        test_iamc_status,
        test_funcionarios_endpoints,
        test_dashboard_metrics,
        test_departamentos,
        test_presencas,
        test_licencas
    ]
    
    for test in tests:
        if test():
            success_count += 1
    
    # Resumo final
    print("\n" + "=" * 60)
    print("📋 RESUMO DOS TESTES")
    print("=" * 60)
    print(f"✅ Testes bem-sucedidos: {success_count}/{total_tests}")
    print(f"❌ Testes falharam: {total_tests - success_count}/{total_tests}")
    
    if success_count == total_tests:
        print("\n🎉 TODOS OS TESTES PASSARAM! Integração RRHH funcionando corretamente.")
        return 0
    else:
        print(f"\n⚠️ {total_tests - success_count} teste(s) falharam. Verifique os logs acima.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
