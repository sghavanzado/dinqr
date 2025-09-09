#!/usr/bin/env python3
"""
Teste simples para verificar se os endpoints de foto estão funcionando.
"""

import requests

def test_basic_funcionarios():
    """Teste básico dos funcionários."""
    try:
        url = "http://localhost:5000/api/iamc/funcionarios"
        response = requests.get(url, timeout=5)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            funcionarios = data.get('funcionarios', [])
            print(f"Funcionários encontrados: {len(funcionarios)}")
            
            if funcionarios:
                primeiro = funcionarios[0]
                print(f"Primeiro funcionário: {primeiro.get('Nome')} - Foto: {primeiro.get('Foto', 'N/A')}")
                return primeiro.get('FuncionarioID')
        else:
            print(f"Erro: {response.text}")
            
    except Exception as e:
        print(f"Erro na conexão: {e}")
    
    return None

if __name__ == "__main__":
    print("🧪 Teste Simples de Foto")
    funcionario_id = test_basic_funcionarios()
    
    if funcionario_id:
        print(f"✅ Funcionário ID {funcionario_id} disponível para teste de foto")
    else:
        print("❌ Não foi possível obter funcionário para teste")
