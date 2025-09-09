"""
Teste rápido do status IAMC
"""

import requests
import json

def test_iamc_status():
    url = "http://127.0.0.1:5000/api/iamc/status"
    
    try:
        print(f"🔄 Testando: {url}")
        response = requests.get(url, timeout=5)
        
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Resposta: {json.dumps(data, indent=2)}")
            return True
        else:
            print(f"❌ Erro: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Servidor não está respondendo em http://127.0.0.1:5000")
        return False
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return False

def test_funcionarios_get():
    url = "http://127.0.0.1:5000/api/iamc/funcionarios"
    
    try:
        print(f"\n🔄 Testando: {url}")
        response = requests.get(url, timeout=5)
        
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Lista de funcionários obtida com sucesso!")
            print(f"📄 Total: {len(data.get('data', []))} funcionários")
            return True
        else:
            print(f"❌ Erro: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Servidor não está respondendo")
        return False
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Teste Rápido dos Endpoints IAMC")
    print("=" * 40)
    
    # Teste 1: Status
    status_ok = test_iamc_status()
    
    # Teste 2: Funcionários (se status OK)
    if status_ok:
        funcionarios_ok = test_funcionarios_get()
        
        if funcionarios_ok:
            print("\n🎉 Servidor IAMC está funcionando corretamente!")
            print("📋 Você pode usar o Postman agora:")
            print("   - Collection: IAMC_Postman_Collection_Melhorada.json")
            print("   - Environment: IAMC_Postman_Environment.json")
            print("   - Base URL: http://127.0.0.1:5000")
        else:
            print("\n⚠️ Status OK, mas há problemas com endpoints de dados")
    else:
        print("\n❌ Servidor não está funcionando")
    
    print("\n" + "=" * 40)
