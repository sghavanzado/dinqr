"""
Script de teste rápido para validar se os controllers IAMC estão funcionando
Execute este script para testar os endpoints básicos após as correções
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000/api/iamc"

def testar_status():
    """Testa o endpoint de status"""
    try:
        response = requests.get(f"{BASE_URL}/status")
        print(f"✅ Status IAMC: {response.status_code}")
        if response.status_code == 200:
            print(f"📊 Resposta: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro no status: {e}")
        return False

def testar_criar_departamento():
    """Testa a criação de departamento"""
    try:
        dados = {
            "Nome": "Tecnologia da Informação - Teste",
            "Descricao": "Departamento de TI para testes"
        }
        
        response = requests.post(f"{BASE_URL}/departamentos", json=dados)
        print(f"✅ Criar Departamento: {response.status_code}")
        
        if response.status_code in [200, 201]:
            dept_data = response.json()
            print(f"📊 Departamento criado: {dept_data}")
            if 'departamento' in dept_data:
                return dept_data['departamento'].get('DepartamentoID')
        else:
            print(f"❌ Erro: {response.text}")
        return None
    except Exception as e:
        print(f"❌ Erro ao criar departamento: {e}")
        return None

def testar_criar_funcionario():
    """Testa a criação de funcionário"""
    try:
        dados = {
            "Nome": "João Silva Teste",
            "Apelido": "Silva",
            "BI": f"TEST{datetime.now().strftime('%H%M%S')}LA041",  # BI único
            "DataNascimento": "1990-05-15",
            "Sexo": "M",
            "EstadoCivil": "Solteiro",
            "Email": f"teste{datetime.now().strftime('%H%M%S')}@empresa.com",
            "Telefone": "+244 923 456 789",
            "Endereco": "Rua da Paz, 123, Luanda",
            "DataAdmissao": "2024-01-15",
            "EstadoFuncionario": "Activo"
        }
        
        response = requests.post(f"{BASE_URL}/funcionarios", json=dados)
        print(f"✅ Criar Funcionário: {response.status_code}")
        
        if response.status_code in [200, 201]:
            func_data = response.json()
            print(f"📊 Funcionário criado: {func_data}")
            if 'funcionario' in func_data:
                return func_data['funcionario'].get('FuncionarioID')
        else:
            print(f"❌ Erro: {response.text}")
        return None
    except Exception as e:
        print(f"❌ Erro ao criar funcionário: {e}")
        return None

def testar_listar_funcionarios():
    """Testa a listagem de funcionários"""
    try:
        response = requests.get(f"{BASE_URL}/funcionarios")
        print(f"✅ Listar Funcionários: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Total de funcionários: {len(data) if isinstance(data, list) else 'N/A'}")
            return True
        else:
            print(f"❌ Erro: {response.text}")
        return False
    except Exception as e:
        print(f"❌ Erro ao listar funcionários: {e}")
        return False

def testar_registrar_presenca(funcionario_id):
    """Testa o registro de presença"""
    if not funcionario_id:
        print("⚠️ Pulando teste de presença - sem funcionário ID")
        return False
        
    try:
        dados = {
            "FuncionarioID": funcionario_id,
            "Data": "2024-12-09",
            "HoraEntrada": "08:00:00",
            "HoraSaida": "17:00:00",
            "Observacao": "Presença de teste"
        }
        
        response = requests.post(f"{BASE_URL}/presencas", json=dados)
        print(f"✅ Registrar Presença: {response.status_code}")
        
        if response.status_code in [200, 201]:
            print(f"📊 Presença registrada: {response.json()}")
            return True
        else:
            print(f"❌ Erro: {response.text}")
        return False
    except Exception as e:
        print(f"❌ Erro ao registrar presença: {e}")
        return False

def main():
    """Função principal do teste"""
    print("🚀 IAMC - Teste Rápido dos Controllers")
    print("=" * 50)
    
    # Teste 1: Status
    print("\n1. Testando Status...")
    if not testar_status():
        print("❌ Falha no status. Verifique se o servidor está rodando.")
        return
    
    # Teste 2: Criar departamento
    print("\n2. Testando Criação de Departamento...")
    dept_id = testar_criar_departamento()
    
    # Teste 3: Criar funcionário
    print("\n3. Testando Criação de Funcionário...")
    func_id = testar_criar_funcionario()
    
    # Teste 4: Listar funcionários
    print("\n4. Testando Listagem de Funcionários...")
    testar_listar_funcionarios()
    
    # Teste 5: Registrar presença
    print("\n5. Testando Registro de Presença...")
    testar_registrar_presenca(func_id)
    
    print("\n" + "=" * 50)
    print("✅ Teste concluído!")
    
    if dept_id:
        print(f"🏢 Departamento criado com ID: {dept_id}")
    if func_id:
        print(f"👤 Funcionário criado com ID: {func_id}")
    
    print("\n📝 Próximos passos:")
    print("1. Usar Postman com a coleção melhorada")
    print("2. Testar todos os endpoints CRUD")
    print("3. Verificar logs em backend/logs/app.log")

if __name__ == "__main__":
    main()
