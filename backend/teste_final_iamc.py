#!/usr/bin/env python3
"""
Teste final completo de todos os endpoints IAMC.
"""

import json
from flask import Flask
from flask.testing import FlaskClient

# Importar a aplicação
from app import app

def test_all_endpoints():
    """
    Testa todos os endpoints IAMC para garantir que estão funcionando corretamente.
    """
    print("🧪 TESTE FINAL COMPLETO - Endpoints IAMC")
    print("=" * 60)
    
    with app.test_client() as client:
        
        # Lista de endpoints para testar
        endpoints = [
            ('/api/iamc/status', 'Status do Sistema'),
            ('/api/iamc/funcionarios', 'Lista de Funcionários'),
            ('/api/iamc/departamentos', 'Lista de Departamentos'),
            ('/api/iamc/cargos', 'Lista de Cargos'),
            ('/api/iamc/presencas', 'Lista de Presenças'),
            ('/api/iamc/beneficios', 'Lista de Benefícios'),
            ('/api/iamc/funcionario-beneficios', 'Associações Funcionário-Benefício'),
            ('/api/iamc/folha-salarial', 'Folhas Salariais'),
            ('/api/iamc/historico-cargo', 'Histórico de Cargos'),
        ]
        
        results = []
        
        for endpoint, description in endpoints:
            print(f"\n📡 Testando: {description}")
            print(f"   Endpoint: {endpoint}")
            
            try:
                response = client.get(endpoint)
                status_code = response.status_code
                
                print(f"   Status: {status_code}")
                
                if status_code == 200:
                    try:
                        data = response.get_json()
                        
                        if isinstance(data, list):
                            count = len(data)
                            print(f"   ✅ Sucesso - {count} registros retornados")
                            
                            if count > 0:
                                # Mostrar estrutura do primeiro registro
                                first_record = data[0]
                                fields = list(first_record.keys()) if isinstance(first_record, dict) else []
                                print(f"   📋 Campos: {', '.join(fields)}")
                        
                        elif isinstance(data, dict):
                            if 'success' in data and data['success']:
                                print(f"   ✅ Sucesso - Resposta: {data.get('status', 'OK')}")
                            else:
                                print(f"   ⚠️ Resposta: {data}")
                        
                        results.append({
                            'endpoint': endpoint,
                            'description': description,
                            'status': 'SUCCESS',
                            'status_code': status_code,
                            'record_count': len(data) if isinstance(data, list) else 1
                        })
                        
                    except Exception as json_error:
                        print(f"   ❌ Erro ao parsear JSON: {json_error}")
                        results.append({
                            'endpoint': endpoint,
                            'description': description,
                            'status': 'JSON_ERROR',
                            'status_code': status_code,
                            'error': str(json_error)
                        })
                
                elif status_code == 404:
                    print(f"   ⚠️ Endpoint não encontrado (404)")
                    results.append({
                        'endpoint': endpoint,
                        'description': description,
                        'status': 'NOT_FOUND',
                        'status_code': status_code
                    })
                
                else:
                    print(f"   ❌ Erro {status_code}: {response.get_data(as_text=True)}")
                    results.append({
                        'endpoint': endpoint,
                        'description': description,
                        'status': 'ERROR',
                        'status_code': status_code,
                        'error': response.get_data(as_text=True)
                    })
                    
            except Exception as e:
                print(f"   ❌ Exceção: {str(e)}")
                results.append({
                    'endpoint': endpoint,
                    'description': description,
                    'status': 'EXCEPTION',
                    'error': str(e)
                })
        
        # Resumo final
        print(f"\n" + "=" * 60)
        print("📊 RESUMO DOS TESTES")
        print(f"=" * 60)
        
        successful = [r for r in results if r['status'] == 'SUCCESS']
        failed = [r for r in results if r['status'] != 'SUCCESS']
        
        print(f"✅ Sucessos: {len(successful)}/{len(results)}")
        print(f"❌ Falhas: {len(failed)}/{len(results)}")
        
        if failed:
            print(f"\n🚨 ENDPOINTS COM PROBLEMAS:")
            for result in failed:
                print(f"   • {result['endpoint']} - {result['status']}")
                if 'error' in result:
                    print(f"     Erro: {result['error']}")
        
        if successful:
            print(f"\n✅ ENDPOINTS FUNCIONANDO:")
            for result in successful:
                count_info = f" ({result.get('record_count', 0)} registros)" if 'record_count' in result else ""
                print(f"   • {result['endpoint']}{count_info}")
        
        print(f"\n" + "=" * 60)
        
        # Status geral
        if len(successful) == len(results):
            print("🎉 TODOS OS ENDPOINTS ESTÃO FUNCIONANDO PERFEITAMENTE!")
            print("\n🚀 PRÓXIMOS PASSOS:")
            print("   1. Use a coleção Postman: IAMC_Postman_Collection_Melhorada.json")
            print("   2. Teste operações CRUD (GET, POST, PUT, DELETE)")
            print("   3. Valide os dados retornados")
            print("   4. Documente eventuais ajustes necessários")
        else:
            print("⚠️ ALGUNS ENDPOINTS PRECISAM DE ATENÇÃO")
            print("   Por favor, verifique os erros listados acima")
        
        return len(successful) == len(results)

if __name__ == "__main__":
    with app.app_context():
        test_all_endpoints()
