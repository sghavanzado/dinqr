"""
Script de prueba para verificar la implementación de configuraciones avanzadas
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    print("=== TESTING PASSES CONFIGURATION ===")
    
    # Importar módulos necesarios
    from routes.passes_routes import criar_tabelas_configuracao, obter_tema_por_id, obter_formato_por_id
    from utils.db_utils import obtener_conexion_local
    
    print("✅ Imports successful")
    
    # Crear tablas
    print("📋 Creating database tables...")
    criar_tabelas_configuracao()
    print("✅ Tables created successfully")
    
    # Verificar conexión a la base de datos
    print("🔌 Testing database connection...")
    conn = obtener_conexion_local()
    cursor = conn.cursor()
    
    # Verificar si las tablas existen
    cursor.execute("""
        SELECT COUNT(*) as count FROM pass_temas_avancado
    """)
    temas_count = cursor.fetchone()[0]
    print(f"✅ Temas table exists with {temas_count} records")
    
    cursor.execute("""
        SELECT COUNT(*) as count FROM pass_formatos_avancado
    """)
    formatos_count = cursor.fetchone()[0]
    print(f"✅ Formatos table exists with {formatos_count} records")
    
    # Probar obtener un tema
    if temas_count > 0:
        tema = obter_tema_por_id(1)
        if tema:
            print(f"✅ Retrieved theme: {tema['nome']}")
        else:
            print("❌ Could not retrieve theme with ID 1")
    
    # Probar obtener un formato
    if formatos_count > 0:
        formato = obter_formato_por_id(1)
        if formato:
            print(f"✅ Retrieved format: {formato['nome']}")
        else:
            print("❌ Could not retrieve format with ID 1")
    
    conn.close()
    print("✅ Database connection closed")
    
    print("\n=== CONFIGURATION TEST COMPLETED SUCCESSFULLY ===")
    
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
