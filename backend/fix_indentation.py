#!/usr/bin/env python3
"""
Script para corregir errores de indentación en qr_routes.py
"""

import re
from pathlib import Path

def fix_qr_routes_indentation():
    """Corregir errores de indentación en qr_routes.py"""
    file_path = Path("routes/qr_routes.py")
    
    if not file_path.exists():
        print(f"❌ No se encontró {file_path}")
        return False
    
    try:
        content = file_path.read_text(encoding='utf-8')
        
        # Patrón para encontrar bloques finally problemáticos
        # Buscar: finally: seguido de if conn_local: seguido de comentario vacío
        pattern = r'finally:\s*\n\s*if conn_local:\s*\n\s*# Conexión liberada automáticamente\s*\n'
        replacement = '# Conexión se libera automáticamente con context manager\n'
        
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        
        # También corregir referencias a "base de datos local" que deberían ser "IAMC"
        content = content.replace('base de datos local', 'base de datos IAMC')
        
        # Corregir bloques try-except-finally que no tienen código en finally
        pattern2 = r'(\s*)finally:\s*\n\s*if [^:]+:\s*\n\s*# [^\n]*\n'
        replacement2 = r'\1# Conexión se libera automáticamente\n'
        content = re.sub(pattern2, replacement2, content)
        
        file_path.write_text(content, encoding='utf-8')
        print(f"✅ Corregidos errores de indentación en {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error corrigiendo {file_path}: {str(e)}")
        return False

def main():
    """Función principal"""
    print("🔧 CORRIGIENDO ERRORES DE INDENTACIÓN")
    print("=" * 50)
    
    if fix_qr_routes_indentation():
        print("✅ Corrección completada")
    else:
        print("❌ Error en la corrección")

if __name__ == "__main__":
    main()
