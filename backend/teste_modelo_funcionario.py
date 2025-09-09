"""
Teste direto do modelo Funcionario para verificar se funciona
"""

print("🔄 Testando modelo Funcionario diretamente...")

try:
    # 1. Configurar Flask app
    from flask import Flask
    from config import Config
    
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 2. Inicializar IAMC
    from extensions import init_iamc_db, IAMCSession
    
    with app.app_context():
        success = init_iamc_db(app)
        if not success:
            print("❌ Erro ao inicializar IAMC")
            exit(1)
        
        print("✅ IAMC inicializado!")
        
        # 3. Testar modelo
        from models.iamc_funcionarios_new import Funcionario
        print("✅ Modelo Funcionario importado!")
        
        # 4. Testar sessão
        session = IAMCSession()
        print("✅ Sessão criada!")
        
        # 5. Testar consulta simples (sem paginação)
        print("🔄 Testando consulta simples...")
        funcionarios = session.query(Funcionario).limit(5).all()
        print(f"✅ Encontrados {len(funcionarios)} funcionários!")
        
        # 6. Testar to_dict() se houver funcionários
        if funcionarios:
            funcionario = funcionarios[0]
            print("🔄 Testando to_dict()...")
            data = funcionario.to_dict()
            print(f"✅ to_dict() funcionou: {list(data.keys())}")
        else:
            print("ℹ️ Nenhum funcionário encontrado na base de dados")
        
        session.close()
        print("✅ Sessão fechada!")
        
        print("\n🎉 Modelo funcionando corretamente!")

except Exception as e:
    print(f"❌ Erro: {str(e)}")
    import traceback
    traceback.print_exc()
