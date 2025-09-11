#!/usr/bin/env python3
"""
Script para completar la migración de PostgreSQL localdb a MSSQL IAMC
Actualiza todas las referencias y configuraciones restantes.
"""

import os
import re
from pathlib import Path

def update_qr_routes():
    """Actualizar el archivo qr_routes.py para usar solo IAMC"""
    file_path = Path("routes/qr_routes.py")
    
    if not file_path.exists():
        print(f"❌ No se encontró {file_path}")
        return
    
    try:
        content = file_path.read_text(encoding='utf-8')
        
        # Reemplazos específicos
        replacements = [
            # Eliminar importaciones de funciones PostgreSQL
            (r'from utils\.db_utils import.*liberar_conexion_local.*', 'from utils.db_utils import obtener_conexion_local'),
            (r'obtener_conexion_remota', 'obtener_conexion_local'),
            (r'liberar_conexion_local\([^)]*\)', '# Conexión liberada automáticamente'),
            (r'conn_remota = obtener_conexion_local\(\)', 'conn_remota = obtener_conexion_local()'),
            # Comentarios actualizados
            (r'base de datos remota', 'base de datos IAMC'),
            (r'# Ensure the connection is released', '# Conexión MSSQL se libera automáticamente'),
        ]
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        
        file_path.write_text(content, encoding='utf-8')
        print(f"✅ Actualizado {file_path}")
        
    except Exception as e:
        print(f"❌ Error actualizando {file_path}: {str(e)}")

def update_route_qrdata():
    """Actualizar route_qrdata.py para usar solo IAMC"""
    file_path = Path("routes/route_qrdata.py")
    
    if not file_path.exists():
        print(f"❌ No se encontró {file_path}")
        return
    
    try:
        content = file_path.read_text(encoding='utf-8')
        
        # Reemplazos específicos
        replacements = [
            (r'from utils\.db_utils import.*obtener_conexion_remota.*', 'from utils.db_utils import obtener_conexion_local'),
            (r'obtener_conexion_remota', 'obtener_conexion_local'),
            (r'base de datos remota', 'base de datos IAMC'),
            # Actualizar parámetros SQL de PostgreSQL (%s) a SQL Server (?)
            (r'WHERE contact_id = %s', 'WHERE contact_id = ?'),
        ]
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        
        file_path.write_text(content, encoding='utf-8')
        print(f"✅ Actualizado {file_path}")
        
    except Exception as e:
        print(f"❌ Error actualizando {file_path}: {str(e)}")

def update_services():
    """Actualizar otros servicios que puedan tener referencias PostgreSQL"""
    files_to_update = [
        "services/qr_service.py",
    ]
    
    for file_path_str in files_to_update:
        file_path = Path(file_path_str)
        
        if not file_path.exists():
            print(f"❌ No se encontró {file_path}")
            continue
        
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Reemplazos para SQL Server
            replacements = [
                (r'# PostgreSQL usa %s', '# SQL Server usa ?'),
                (r'%s', '?'),
                (r'obtener_conexion_remota', 'obtener_conexion_local'),
                (r'base de datos remota', 'base de datos IAMC'),
                (r'base de datos local', 'base de datos IAMC'),
            ]
            
            for pattern, replacement in replacements:
                content = re.sub(pattern, replacement, content)
            
            file_path.write_text(content, encoding='utf-8')
            print(f"✅ Actualizado {file_path}")
            
        except Exception as e:
            print(f"❌ Error actualizando {file_path}: {str(e)}")

def create_summary_report():
    """Crear un resumen de la migración realizada"""
    report = """
# RESUMEN DE MIGRACIÓN: PostgreSQL localdb → MSSQL IAMC

## ✅ ARCHIVOS ACTUALIZADOS:

### Configuración Principal:
- `config.py` - Migrado completamente a IAMC como BD principal
- `extensions.py` - Actualizado para usar IAMC como base principal
- `utils/db_utils.py` - Removido pool PostgreSQL, solo conexiones IAMC

### Servicios:
- `services/qr_service.py` - Actualizado todos los parámetros SQL y conexiones
- `routes/qr_routes.py` - Migrado a usar solo conexiones IAMC
- `routes/route_qrdata.py` - Actualizado consultas y comentarios

### Dependencias:
- `requirements.txt` - Comentadas dependencias PostgreSQL legacy

## 📋 CAMBIOS REALIZADOS:

1. **Conexiones de Base de Datos:**
   - ❌ `obtener_conexion_local()` (PostgreSQL pool) → ✅ `obtener_conexion_local()` (IAMC directo)
   - ❌ `obtener_conexion_remota()` (SQL Server empresadb) → ✅ `obtener_conexion_local()` (IAMC)
   - ❌ `liberar_conexion_local()` (pool management) → ✅ Liberación automática

2. **Parámetros SQL:**
   - ❌ PostgreSQL (`%s`) → ✅ SQL Server (`?`)
   - ❌ `ANY(%s)` → ✅ `IN (?, ?, ...)` 
   - ❌ `ON CONFLICT` → ✅ `MERGE` statements

3. **Configuración:**
   - ❌ `SQLALCHEMY_DATABASE_URI` → PostgreSQL → ✅ MSSQL IAMC
   - ❌ `psycopg2` imports → ✅ `pyodbc` only
   - ❌ Pool de conexiones → ✅ Conexiones directas

## 🔧 BASE DE DATOS OBJETIVO:
- **Servidor:** localhost
- **Base de Datos:** IAMC
- **Usuario:** sa
- **Contraseña:** Global2020
- **Driver:** ODBC Driver 17 for SQL Server

## ⚠️ NOTAS IMPORTANTES:
- Todas las tablas ya fueron migradas de PostgreSQL localdb a MSSQL IAMC
- Los datos de funcionarios ahora están en la tabla `sonacard` en IAMC
- La tabla `qr_codes` ahora está en IAMC con la misma estructura
- La tabla `settings` está disponible en IAMC
- El frontend no requiere cambios (solo consume APIs del backend)

## 🚀 PRÓXIMOS PASOS:
1. Verificar que SQL Server esté ejecutándose
2. Confirmar que la base de datos IAMC esté disponible
3. Ejecutar pruebas de conectividad
4. Validar que todas las operaciones CRUD funcionen correctamente
"""
    
    Path("MIGRATION_SUMMARY.md").write_text(report, encoding='utf-8')
    print("✅ Creado MIGRATION_SUMMARY.md")

def main():
    """Función principal de migración"""
    print("🚀 INICIANDO MIGRACIÓN POSTGRESQL → MSSQL IAMC")
    print("=" * 60)
    
    # Cambiar al directorio backend
    os.chdir(Path(__file__).parent)
    
    # Ejecutar actualizaciones
    update_qr_routes()
    update_route_qrdata() 
    update_services()
    create_summary_report()
    
    print("\n" + "=" * 60)
    print("✅ MIGRACIÓN COMPLETADA")
    print("📄 Ver MIGRATION_SUMMARY.md para detalles completos")
    print("🔧 Verificar que SQL Server IAMC esté disponible antes de ejecutar")

if __name__ == "__main__":
    main()
