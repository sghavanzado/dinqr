"""
Teste detalhado para localizar o erro 'db' não definido
"""

import traceback

print("🔍 Diagnosticando erro 'db' não definido...")

try:
    print("1. Testando import do config...")
    from config import Config
    print("   ✅ Config importado com sucesso!")
    
except Exception as e:
    print(f"   ❌ Erro no config: {str(e)}")
    traceback.print_exc()

try:
    print("2. Testando import do extensions...")
    from extensions import IAMCSession
    print("   ✅ Extensions importado com sucesso!")
    
except Exception as e:
    print(f"   ❌ Erro no extensions: {str(e)}")
    traceback.print_exc()

try:
    print("3. Testando import do modelo funcionários...")
    from models.iamc_funcionarios_new import Funcionario
    print("   ✅ Modelo funcionários importado com sucesso!")
    
except Exception as e:
    print(f"   ❌ Erro no modelo funcionários: {str(e)}")
    traceback.print_exc()

try:
    print("4. Testando import do modelo presenças...")
    from models.iamc_presencas_new import Presenca
    print("   ✅ Modelo presenças importado com sucesso!")
    
except Exception as e:
    print(f"   ❌ Erro no modelo presenças: {str(e)}")
    traceback.print_exc()

try:
    print("5. Testando import do controller funcionários...")
    from controllers.iamc_funcionarios_controller_new import FuncionarioController
    print("   ✅ Controller funcionários importado com sucesso!")
    
except Exception as e:
    print(f"   ❌ Erro no controller funcionários: {str(e)}")
    traceback.print_exc()

print("\n🏁 Diagnóstico concluído!")
