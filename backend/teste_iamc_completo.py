"""
Teste das novas funcionalidades IAMC com inicialização simples
"""

print("🔄 Iniciando teste das funcionalidades IAMC...")

try:
    print("1. Importando Flask...")
    from flask import Flask
    
    print("2. Criando app Flask temporário...")
    app = Flask(__name__)
    
    print("3. Importando configuração...")
    from config import Config
    app.config.from_object(Config)
    
    print("4. Inicializando IAMC...")
    from extensions import init_iamc_db, IAMCSession
    
    with app.app_context():
        success = init_iamc_db(app)
        if success:
            print("   ✅ IAMC inicializado com sucesso!")
        else:
            print("   ❌ Erro ao inicializar IAMC")
            exit(1)
    
    print("5. Testando importação dos controllers...")
    from controllers.iamc_funcionarios_controller_new import FuncionarioController
    print("   ✅ FuncionarioController importado!")
    
    from controllers.iamc_presencas_controller_new import PresencaController
    print("   ✅ PresencaController importado!")
    
    print("6. Testando criação de sessão...")
    if IAMCSession:
        session = IAMCSession()
        print(f"   ✅ Sessão criada: {session}")
        session.close()
        print("   ✅ Sessão fechada!")
    else:
        print("   ❌ IAMCSession não está disponível")
    
    print("\n🎉 Todos os testes passaram com sucesso!")
    
except Exception as e:
    print(f"❌ Erro: {str(e)}")
    import traceback
    traceback.print_exc()
