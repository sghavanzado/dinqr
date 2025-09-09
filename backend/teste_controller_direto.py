"""
Teste direto do FuncionarioController - Criar funcionário
"""

print("🔄 Teste direto do Controller de Funcionários")
print("=" * 50)

try:
    # 1. Configurar Flask app
    from flask import Flask
    from config import Config
    
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 2. Inicializar IAMC
    from extensions import init_iamc_db
    
    with app.app_context():
        success = init_iamc_db(app)
        if not success:
            print("❌ Erro ao inicializar IAMC")
            exit(1)
        
        # 3. Testar Controller
        from controllers.iamc_funcionarios_controller_new import FuncionarioController
        
        # Simular request JSON para teste
        import json
        from unittest.mock import Mock
        
        # Mock do request.get_json()
        test_data = {
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
        
        # Mock do Flask request
        import flask
        with app.test_request_context(json=test_data):
            print("📝 Dados de teste:")
            print(json.dumps(test_data, indent=2))
            
            print("\n🔄 Executando FuncionarioController.criar()...")
            response, status_code = FuncionarioController.criar()
            
            print(f"📊 Status Code: {status_code}")
            print(f"📄 Response: {response.get_json() if hasattr(response, 'get_json') else response}")
            
            if status_code == 201:
                print("✅ Funcionário criado com sucesso!")
            else:
                print(f"❌ Erro ao criar funcionário: {status_code}")

except Exception as e:
    print(f"❌ Erro: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
print("🏁 Teste concluído!")
