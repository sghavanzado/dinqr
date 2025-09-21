#!/usr/bin/env python3
"""Script para verificar la estructura de la tabla qr_codes."""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from utils.db_utils import obtener_conexion_local
    
    print("Checking qr_codes table structure...")
    conn = obtener_conexion_local()
    cursor = conn.cursor()
    
    # Obtener estructura de la tabla
    cursor.execute("""
        SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = 'qr_codes'
        ORDER BY ORDINAL_POSITION
    """)
    
    columns = cursor.fetchall()
    
    if columns:
        print(f"Found {len(columns)} columns in qr_codes table:")
        for col in columns:
            print(f"  - {col[0]} ({col[1]}) - Nullable: {col[2]} - Default: {col[3]}")
    else:
        print("No columns found or table doesn't exist")
    
    # Verificar datos existentes
    cursor.execute("SELECT COUNT(*) FROM qr_codes")
    count = cursor.fetchone()[0]
    print(f"Current records in qr_codes: {count}")
    
    if count > 0:
        cursor.execute("SELECT TOP 5 * FROM qr_codes")
        records = cursor.fetchall()
        print("Sample records:")
        for record in records:
            print(f"  - {record}")
    
    conn.close()
    
except Exception as e:
    print(f"✗ Error: {str(e)}")
    import traceback
    traceback.print_exc()
