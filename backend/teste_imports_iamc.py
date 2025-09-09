"""
Teste simples de importação dos novos controllers IAMC
"""

print("🔄 Testando importações dos novos controllers IAMC...")

try:
    print("1. Importando FuncionarioController...")
    from controllers.iamc_funcionarios_controller_new import FuncionarioController, DepartamentoController
    print("   ✅ FuncionarioController e DepartamentoController importados com sucesso!")
    
    print("2. Importando PresencaController...")
    from controllers.iamc_presencas_controller_new import PresencaController, LicencaController, BeneficioController, FolhaSalarialController
    print("   ✅ Controllers de Presenças importados com sucesso!")
    
    print("3. Testando conexão IAMC...")
    from extensions import IAMCSession
    session = IAMCSession()
    print(f"   ✅ Sessão IAMC criada: {session}")
    session.close()
    print("   ✅ Sessão IAMC fechada com sucesso!")
    
    print("4. Testando modelos...")
    from models.iamc_funcionarios_new import Funcionario, Departamento
    from models.iamc_presencas_new import Presenca, Licenca, Beneficio, FolhaSalarial
    print("   ✅ Modelos IAMC importados com sucesso!")
    
    print("\n🎉 Todos os testes de importação passaram com sucesso!")
    
except ImportError as e:
    print(f"❌ Erro de importação: {str(e)}")
except Exception as e:
    print(f"❌ Erro inesperado: {str(e)}")
