"""
Script simple para probar los endpoints de configuración de passes
"""
import requests
import json

def test_endpoint(url, method='GET', data=None):
    try:
        if method == 'GET':
            response = requests.get(url, timeout=5)
        elif method == 'POST':
            response = requests.post(url, json=data, timeout=5)
        elif method == 'DELETE':
            response = requests.delete(url, timeout=5)
        elif method == 'PUT':
            response = requests.put(url, json=data, timeout=5)
        
        print(f"✅ {method} {url} - Status: {response.status_code}")
        if response.status_code in [200, 201]:
            return response.json()
        else:
            print(f"❌ Error: {response.text}")
            return None
    except Exception as e:
        print(f"❌ {method} {url} - Error: {str(e)}")
        return None

def main():
    base_url = "http://localhost:5000/api/iamc/passes"
    
    print("=== TESTING PASSES CONFIGURATION ENDPOINTS ===\n")
    
    # Test configuracao endpoint
    print("1. Testing configuration endpoint...")
    config_data = test_endpoint(f"{base_url}/configuracao")
    if config_data and config_data.get('success'):
        print(f"   - Found {len(config_data['data']['temas_disponiveis'])} themes")
        print(f"   - Found {len(config_data['data']['formatos_saida'])} formats")
    
    # Test temas endpoint
    print("\n2. Testing themes endpoint...")
    temas_data = test_endpoint(f"{base_url}/temas")
    if temas_data and temas_data.get('success'):
        print(f"   - Found {temas_data['data']['total']} themes in database")
    
    # Test formatos endpoint
    print("\n3. Testing formats endpoint...")
    formatos_data = test_endpoint(f"{base_url}/formatos")
    if formatos_data and formatos_data.get('success'):
        print(f"   - Found {formatos_data['data']['total']} formats in database")
    
    # Test creating a new theme
    print("\n4. Testing create theme...")
    new_theme = {
        "nome": "Teste API",
        "cor_primaria": "#ff5722",
        "cor_secundaria": "#fff3e0",
        "cor_texto": "#000000",
        "layout_tipo": "horizontal",
        "ativo": True
    }
    create_result = test_endpoint(f"{base_url}/temas", 'POST', new_theme)
    if create_result and create_result.get('success'):
        theme_id = create_result['data']['id']
        print(f"   - Created theme with ID: {theme_id}")
        
        # Test delete the created theme
        print("\n5. Testing delete theme...")
        delete_result = test_endpoint(f"{base_url}/temas/{theme_id}", 'DELETE')
        if delete_result and delete_result.get('success'):
            print("   - Theme deleted successfully!")
    
    # Test creating a new format
    print("\n6. Testing create format...")
    new_format = {
        "nome": "Teste Format API",
        "extensao": "pdf",
        "descricao": "Formato de teste via API",
        "largura": 90.0,
        "altura": 55.0,
        "dpi": 300,
        "orientacao": "horizontal",
        "ativo": True
    }
    create_format_result = test_endpoint(f"{base_url}/formatos", 'POST', new_format)
    if create_format_result and create_format_result.get('success'):
        format_id = create_format_result['data']['id']
        print(f"   - Created format with ID: {format_id}")
        
        # Test delete the created format
        print("\n7. Testing delete format...")
        delete_format_result = test_endpoint(f"{base_url}/formatos/{format_id}", 'DELETE')
        if delete_format_result and delete_format_result.get('success'):
            print("   - Format deleted successfully!")
    
    print("\n=== TEST COMPLETED ===")

if __name__ == "__main__":
    main()
