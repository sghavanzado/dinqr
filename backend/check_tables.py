#!/usr/bin/env python3
"""
Script para verificar qué tablas existen en IAMC
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.db_utils import obtener_conexion_local

print("=== VERIFICANDO TABLAS EN IAMC ===")

try:
    conn = obtener_conexion_local()
    cursor = conn.cursor()
    
    # Consultar tablas
    cursor.execute("SELECT name FROM sys.tables")
    tables = [row[0] for row in cursor.fetchall()]
    
    print(f"\n📋 Tablas en base de datos IAMC:")
    for table in sorted(tables):
        print(f"  - {table}")
        
    # Verificar si existe tabla settings
    if 'settings' in tables:
        print(f"\n✅ Tabla 'settings' encontrada")
        cursor.execute("SELECT [key], value FROM settings")
        settings = cursor.fetchall()
        print(f"🔧 Configuraciones en settings:")
        for key, value in settings:
            print(f"  - {key}: {value}")
    else:
        print(f"\n❌ Tabla 'settings' NO encontrada")
        print(f"📝 Necesitamos crear la tabla settings con configuraciones básicas")
        
    # Verificar tabla qr_codes  
    if 'qr_codes' in tables:
        print(f"\n✅ Tabla 'qr_codes' encontrada")
        cursor.execute("SELECT COUNT(*) FROM qr_codes")
        count = cursor.fetchone()[0]
        print(f"📊 Total QR codes: {count}")
        
        if count > 0:
            cursor.execute("SELECT TOP 5 contact_id FROM qr_codes")
            sample_ids = [str(row[0]) for row in cursor.fetchall()]
            print(f"🔍 Primeros 5 contact_ids: {', '.join(sample_ids)}")
    else:
        print(f"\n❌ Tabla 'qr_codes' NO encontrada")
        
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
