"""
Teste direto GET funcionários
"""

import requests

try:
    response = requests.get("http://127.0.0.1:5000/api/iamc/funcionarios")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Erro: {e}")
