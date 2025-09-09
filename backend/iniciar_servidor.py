"""
Script para iniciar o servidor Flask com tratamento de erros
"""

try:
    print("🚀 Iniciando servidor Flask IAMC...")
    
    # Verificar imports
    print("📦 Verificando imports...")
    from app import app
    print("   ✅ App importado com sucesso!")
    
    # Verificar configuração
    print("⚙️ Verificando configuração...")
    print(f"   🔧 Debug: {app.config.get('DEBUG', False)}")
    print(f"   🔧 IAMC URI: {app.config.get('IAMC_SQLALCHEMY_DATABASE_URI', 'Not set')[:50]}...")
    
    # Iniciar servidor
    print("🌐 Iniciando servidor em http://127.0.0.1:5000...")
    app.run(host='127.0.0.1', port=5000, debug=True)
    
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
