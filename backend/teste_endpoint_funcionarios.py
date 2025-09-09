"""
Teste simples do endpoint IAMC Funcionários - POST /api/iamc/funcionarios
"""

import requests
import json

# URL do endpoint
url = "http://127.0.0.1:5000/api/iamc/funcionarios"

# Dados de teste para criar um funcionário
funcionario_data = {
    "Nome": "João Silva",
    "Apelido": "Silva", 
    "BI": "123456789LA041",
    "DataNascimento": "1990-05-15",
    "Sexo": "M",
    "EstadoCivil": "Solteiro",
    "Email": "joao.silva@empresa.com",
    "Telefone": "+244 923 456 789",
    "Endereco": "Rua da Paz, 123, Luanda",
    "DataAdmissao": "2024-01-15",
    "EstadoFuncionario": "Activo"
}

print("🔄 IAMC - Teste do Endpoint POST /api/iamc/funcionarios")
print("=" * 60)

try:
    print(f"📡 Enviando POST para: {url}")
    print(f"📝 Dados: {json.dumps(funcionario_data, indent=2)}")
    
    # Fazer a requisição POST
    response = requests.post(url, json=funcionario_data, timeout=10)
    
    print(f"📊 Status Code: {response.status_code}")
    print(f"📄 Response Headers: {dict(response.headers)}")
    
    if response.headers.get('content-type', '').startswith('application/json'):
        response_data = response.json()
        print(f"✅ Response JSON: {json.dumps(response_data, indent=2)}")
    else:
        print(f"📄 Response Text: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("❌ Erro: Não foi possível conectar ao servidor.")
    print("   Verifique se o Flask app está rodando em http://127.0.0.1:5000")
except requests.exceptions.Timeout:
    print("⏱️ Erro: Timeout na requisição.")
except Exception as e:
    print(f"❌ Erro inesperado: {str(e)}")

print("\n" + "=" * 60)
print("🏁 Teste concluído!")
