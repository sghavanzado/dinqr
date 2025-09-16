#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script to verify cargo creation with departamento assignment
"""

import requests
import json

def test_create_cargo():
    """Test creating a cargo with departamento assignment"""
    
    url = "http://localhost:5000/api/iamc/cargos"
    
    # Test data (as sent by frontend)
    data = {
        "Nome": "Diretor de Teste",
        "Descricao": "Cargo criado via teste de API",
        "Nivel": "Executivo",
        "DepartamentoID": 1
    }
    
    print("🧪 Testando criação de cargo com departamento...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data)
        print(f"\n📊 Status Code: {response.status_code}")
        print(f"📄 Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            print("✅ Cargo criado com sucesso!")
            return True
        else:
            print("❌ Erro ao criar cargo")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar ao servidor backend")
        print("   Certifique-se de que o backend está rodando em localhost:5000")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")
        return False

def test_list_departamentos():
    """Test listing departamentos to get valid IDs"""
    
    url = "http://localhost:5000/api/iamc/departamentos"
    
    print("📋 Listando departamentos disponíveis...")
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('data'):
                print("✅ Departamentos encontrados:")
                for dept in data['data']:
                    print(f"   • ID: {dept.get('DepartamentoID')} - Nome: {dept.get('Nome')}")
                return True
        
        print("❌ Erro ao listar departamentos")
        return False
        
    except Exception as e:
        print(f"❌ Erro ao listar departamentos: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Teste de Criação de Cargo com Departamento")
    print("=" * 60)
    
    # First list available departamentos
    if test_list_departamentos():
        print("\n" + "=" * 60)
        
        # Then test cargo creation
        test_create_cargo()
    
    print("\n" + "=" * 60)
