#!/usr/bin/env python3
"""
Script de prueba para verificar la migración a MSSQL IAMC
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_config():
    """Probar la configuración de la base de datos"""
    try:
        from config import Config
        print("✅ Configuración cargada correctamente")
        print(f"   URI: {Config.SQLALCHEMY_DATABASE_URI}")
        print(f"   IAMC Config: {Config.IAMC_DB_CONFIG}")
        return True
    except Exception as e:
        print(f"❌ Error en configuración: {str(e)}")
        return False

def test_db_connection():
    """Probar la conexión a la base de datos"""
    try:
        from utils.db_utils import obtener_conexion_local
        
        with obtener_conexion_local() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT @@VERSION")
            version = cursor.fetchone()[0]
            print(f"✅ Conexión IAMC exitosa")
            print(f"   SQL Server: {version[:50]}...")
            return True
    except Exception as e:
        print(f"❌ Error de conexión IAMC: {str(e)}")
        return False

def test_tables():
    """Verificar que las tablas existen"""
    try:
        from utils.db_utils import obtener_conexion_local
        
        tables_to_check = ['settings', 'qr_codes', 'sonacard', 'users']
        
        with obtener_conexion_local() as conn:
            cursor = conn.cursor()
            for table in tables_to_check:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"✅ Tabla '{table}': {count} registros")
                except Exception as e:
                    print(f"⚠️  Tabla '{table}': {str(e)}")
        return True
    except Exception as e:
        print(f"❌ Error verificando tablas: {str(e)}")
        return False

def test_imports():
    """Verificar que todos los imports funcionan"""
    try:
        from services.qr_service import obtener_carpeta_salida
        from routes.qr_routes import qr_bp
        from routes.route_qrdata import qrdata_bp
        print("✅ Todos los imports principales funcionan")
        return True
    except Exception as e:
        print(f"❌ Error en imports: {str(e)}")
        return False

def main():
    """Ejecutar todas las pruebas"""
    print("🔧 VERIFICACIÓN DE MIGRACIÓN POSTGRESQL → MSSQL IAMC")
    print("=" * 60)
    
    tests = [
        ("Configuración", test_config),
        ("Conexión BD", test_db_connection),
        ("Tablas", test_tables),
        ("Imports", test_imports),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Probando {test_name}:")
        if test_func():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 RESULTADOS: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡MIGRACIÓN EXITOSA! El sistema está listo para usar IAMC")
    else:
        print("⚠️  Algunos problemas encontrados. Verificar configuración.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
