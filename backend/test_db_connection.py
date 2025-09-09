#!/usr/bin/env python3
"""
Script para probar la conexión a la base de datos SQL Server externa
Ejecutar desde el directorio backend/
"""

import sys
import os
sys.path.append('.')

try:
    from utils.db_utils import obtener_conexion_remota
    import logging
    
    logging.basicConfig(level=logging.INFO)
    
    print("🔗 Probando conexión a SQL Server...")
    print(f"   Servidor: {os.environ.get('DB_SERVER', 'localhost')}")
    print(f"   Base de datos: {os.environ.get('DB_NAME', 'empresadb')}")
    print(f"   Usuario: {os.environ.get('DB_USERNAME', 'sa')}")
    print("")
    
    # Intentar conectar
    with obtener_conexion_remota() as conn:
        cursor = conn.cursor()
        
        # Probar consulta básica
        cursor.execute("SELECT COUNT(*) as total FROM sonacard")
        resultado = cursor.fetchone()
        
        print("✅ Conexión exitosa!")
        print(f"   Total de registros en vista sonacard: {resultado[0]}")
        
        # Probar estructura de la vista
        cursor.execute("""
            SELECT TOP 5 sap, nome, funcao, area 
            FROM sonacard 
            WHERE nome IS NOT NULL 
            ORDER BY sap
        """)
        
        registros = cursor.fetchall()
        
        print("\n📋 Ejemplo de registros:")
        print("   SAP     | Nome                | Funcao          | Area")
        print("   --------|---------------------|-----------------|------------------")
        
        for registro in registros:
            sap = str(registro[0]) if registro[0] else 'N/A'
            nome = (registro[1][:18] + '..') if registro[1] and len(registro[1]) > 20 else (registro[1] or 'N/A')
            funcao = (registro[2][:13] + '..') if registro[2] and len(registro[2]) > 15 else (registro[2] or 'N/A')
            area = (registro[3][:16] + '..') if registro[3] and len(registro[3]) > 18 else (registro[3] or 'N/A')
            
            print(f"   {sap:<7} | {nome:<19} | {funcao:<15} | {area}")
            
        print(f"\n🎯 La vista 'sonacard' está accesible y contiene {resultado[0]} registros")
        
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("   Asegúrate de que pyodbc esté instalado: pip install pyodbc")
    
except ConnectionError as e:
    print(f"❌ Error de conexión: {e}")
    print("\n🔧 Posibles soluciones:")
    print("   1. Verificar que el servidor localhost esté accesible")
    print("   2. Verificar credenciales: sa / Global2020")
    print("   3. Verificar que la base de datos 'empresadb' existe")
    print("   4. Verificar que SQL Server esté instalado")
    print("   5. Verificar conectividad de red al puerto 1433")
    
except Exception as e:
    print(f"❌ Error inesperado: {e}")
    print(f"   Tipo de error: {type(e).__name__}")
    
finally:
    print("\n" + "="*60)
    print("Script de prueba completado")
