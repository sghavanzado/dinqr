#!/usr/bin/env python3
"""Script para verificar la tabla settings."""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from utils.db_utils import obtener_conexion_local
    
    print("Checking settings table...")
    conn = obtener_conexion_local()
    cursor = conn.cursor()
    cursor.execute("SELECT [key], value FROM settings ORDER BY [key]")
    records = cursor.fetchall()
    
    if records:
        print(f"Found {len(records)} settings:")
        for record in records:
            print(f"  - {record[0]}: {record[1]}")
    else:
        print("No settings found in database")
        
    conn.close()
    
except Exception as e:
    print(f"✗ Error checking settings table: {str(e)}")
    import traceback
    traceback.print_exc()
