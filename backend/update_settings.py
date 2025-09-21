#!/usr/bin/env python3
"""Script para actualizar la configuración de tabla a IAMC."""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from utils.db_utils import obtener_conexion_local
    
    print("Updating settings table to use IAMC...")
    conn = obtener_conexion_local()
    cursor = conn.cursor()
    
    # Actualizar la configuración de tabela a IAMC
    cursor.execute("UPDATE settings SET value = ? WHERE [key] = ?", ('IAMC', 'tabela'))
    conn.commit()
    
    print("✓ Updated 'tabela' setting to 'IAMC'")
    
    # Verificar que se actualizó correctamente
    cursor.execute("SELECT value FROM settings WHERE [key] = ?", ('tabela',))
    result = cursor.fetchone()
    if result:
        print(f"Current value for 'tabela': {result[0]}")
    
    conn.close()
    
except Exception as e:
    print(f"✗ Error updating settings: {str(e)}")
    import traceback
    traceback.print_exc()
