#!/usr/bin/env python3
"""
Script simple para diagnosticar la aplicación Flask
"""

import sys
import traceback

def main():
    try:
        print("🔧 Iniciando diagnóstico de la aplicación...")
        
        # Test 1: Imports básicos
        print("📦 Probando imports básicos...")
        from config import Config
        print("   ✅ Config importado")
        
        from utils.db_utils import obtener_conexion_local
        print("   ✅ DB Utils importado")
        
        # Test 2: Conexión BD
        print("🗄️ Probando conexión a IAMC...")
        with obtener_conexion_local() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT @@VERSION")
            version = cursor.fetchone()[0]
            print(f"   ✅ Conectado a: {version[:50]}...")
        
        # Test 3: Import de la aplicación
        print("🚀 Probando import de la aplicación...")
        from app import create_app
        print("   ✅ create_app importado")
        
        # Test 4: Crear la aplicación
        print("🏗️ Creando la aplicación Flask...")
        app = create_app()
        print(f"   ✅ Aplicación creada: {app}")
        
        # Test 5: Configuración de la app
        print("⚙️ Verificando configuración...")
        print(f"   DEBUG: {app.config.get('DEBUG')}")
        print(f"   HOST: {app.config.get('HOST')}")
        print(f"   PORT: {app.config.get('PORT')}")
        print(f"   SQLALCHEMY_URI: {app.config.get('SQLALCHEMY_DATABASE_URI')[:50]}...")
        
        # Test 6: Blueprints registrados
        print("📋 Blueprints registrados:")
        for bp_name, bp in app.blueprints.items():
            print(f"   ✅ {bp_name}: {bp}")
        
        print("\n🎉 ¡Todos los tests pasaron! La aplicación debería funcionar.")
        print("Intentando ejecutar el servidor...")
        
        # Ejecutar la aplicación
        app.run(
            host=app.config.get('HOST', '127.0.0.1'),
            port=app.config.get('PORT', 5000),
            debug=app.config.get('DEBUG', True)
        )
        
    except Exception as e:
        print(f"\n❌ Error encontrado:")
        print(f"   Tipo: {type(e).__name__}")
        print(f"   Mensaje: {str(e)}")
        print(f"\n📋 Traceback completo:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()
