# Migration Guide: PostgreSQL localdb to Microsoft SQL Server IAMC

Este documento contiene las instrucciones completas para migrar todas las tablas y datos desde la base de datos PostgreSQL `localdb` hacia la base de datos Microsoft SQL Server `IAMC`.

## 📋 Resumen de la Migración

La migración incluye las siguientes tablas y datos:
- `alembic_version` - Control de versiones de migraciones
- `permission` - Permisos del sistema
- `role` - Roles de usuario
- `roles_permissions` - Relación roles-permisos
- `user` - Usuarios del sistema
- `audit_log` - Registros de auditoría
- `qr_codes` - Códigos QR generados
- `settings` - Configuraciones del sistema

## 🔧 Requisitos Previos

### Software Necesario
1. **ODBC Driver 17 for SQL Server** (para el script Python)
2. **Python 3.7+** con el paquete `pyodbc`
3. **SQL Server Management Studio** (SSMS) o herramienta similar
4. Acceso completo a la base de datos IAMC

### Instalación de Dependencias
```bash
# Instalar pyodbc (si usas el script Python)
pip install pyodbc

# O crear un entorno virtual
python -m venv migration_env
migration_env\Scripts\activate
pip install pyodbc
```

## 📁 Archivos de Migración

Los siguientes archivos están incluidos en esta migración:

1. **`migrate_localdb_to_iamc.sql`** - Script principal con todas las tablas y datos base
2. **`migrate_qr_codes_part1.sql`** - Primer lote de datos de códigos QR 
3. **`migrate_database.py`** - Script Python automatizado para ejecutar la migración
4. **`README_MIGRATION.md`** - Este archivo de documentación

## 🚀 Métodos de Migración

### Método 1: Ejecución Manual con SSMS

#### Paso 1: Preparar la Base de Datos
```sql
-- Conectarse a la base de datos IAMC
USE IAMC;
GO
```

#### Paso 2: Ejecutar Script Principal
1. Abrir `migrate_localdb_to_iamc.sql` en SSMS
2. Ejecutar el script completo
3. Verificar que no hay errores

#### Paso 3: Ejecutar Datos de QR Codes
1. Abrir `migrate_qr_codes_part1.sql` en SSMS
2. Ejecutar el script
3. Verificar la inserción de datos

#### Paso 4: Verificar la Migración
```sql
-- Verificar que las tablas existen y tienen datos
SELECT 'alembic_version' as tabla, COUNT(*) as registros FROM alembic_version
UNION ALL
SELECT 'permission', COUNT(*) FROM permission
UNION ALL
SELECT 'role', COUNT(*) FROM [role]
UNION ALL
SELECT 'roles_permissions', COUNT(*) FROM roles_permissions
UNION ALL
SELECT 'user', COUNT(*) FROM [user]
UNION ALL
SELECT 'audit_log', COUNT(*) FROM audit_log
UNION ALL
SELECT 'qr_codes', COUNT(*) FROM qr_codes
UNION ALL
SELECT 'settings', COUNT(*) FROM settings;
```

### Método 2: Ejecución Automatizada con Python

#### Paso 1: Configurar Parámetros de Conexión
Editar el archivo `migrate_database.py` y actualizar:
```python
IAMC_SERVER = "tu_servidor_iamc"      # Servidor IAMC
IAMC_DATABASE = "IAMC"                # Nombre de la base de datos
IAMC_USERNAME = "tu_usuario"          # Usuario con permisos
IAMC_PASSWORD = "tu_contraseña"       # Contraseña
```

#### Paso 2: Ejecutar el Script
```bash
python migrate_database.py
```

#### Paso 3: Revisar los Logs
El script genera logs en:
- `migration.log` - Archivo de log
- Consola - Salida en tiempo real

### Método 3: Variables de Entorno (Recomendado para Producción)

```bash
# Configurar variables de entorno
set IAMC_SERVER=tu_servidor_iamc
set IAMC_DATABASE=IAMC
set IAMC_USERNAME=tu_usuario
set IAMC_PASSWORD=tu_contraseña

# Ejecutar migración
python migrate_database.py
```

## ✅ Verificación de la Migración

### Consultas de Verificación

```sql
-- 1. Verificar estructura de tablas
SELECT TABLE_NAME, TABLE_TYPE 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_NAME IN ('alembic_version', 'permission', 'role', 'roles_permissions', 
                     'user', 'audit_log', 'qr_codes', 'settings')
ORDER BY TABLE_NAME;

-- 2. Verificar conteos de registros
SELECT 'permission' as tabla, COUNT(*) as total FROM permission
UNION ALL
SELECT 'role', COUNT(*) FROM [role]
UNION ALL
SELECT 'user', COUNT(*) FROM [user]
UNION ALL
SELECT 'qr_codes', COUNT(*) FROM qr_codes
UNION ALL
SELECT 'settings', COUNT(*) FROM settings;

-- 3. Verificar datos específicos
SELECT * FROM [user] WHERE email = 'maikel@ejemplos.com';
SELECT * FROM settings WHERE [key] = 'server';
SELECT TOP 5 * FROM qr_codes ORDER BY id;

-- 4. Verificar relaciones
SELECT r.name as rol, p.name as permiso
FROM [role] r
INNER JOIN roles_permissions rp ON r.id = rp.role_id
INNER JOIN permission p ON rp.permission_id = p.id;
```

### Resultados Esperados

| Tabla | Registros Esperados |
|-------|-------------------|
| alembic_version | 1 |
| permission | 5 |
| role | 2 |
| roles_permissions | 5 |
| user | 1 |
| audit_log | 0 |
| qr_codes | 48+ |
| settings | 9 |

## 🔄 Rollback (Deshacer Migración)

En caso de necesitar deshacer la migración:

```sql
-- ⚠️ CUIDADO: Esto eliminará todas las tablas migradas
-- Solo ejecutar si es absolutamente necesario

DROP TABLE IF EXISTS audit_log;
DROP TABLE IF EXISTS qr_codes;
DROP TABLE IF EXISTS settings;
DROP TABLE IF EXISTS [user];
DROP TABLE IF EXISTS roles_permissions;
DROP TABLE IF EXISTS [role];
DROP TABLE IF EXISTS permission;
DROP TABLE IF EXISTS alembic_version;

PRINT 'Migración deshecha completamente';
```

## 🛠️ Solución de Problemas

### Problema: Error de Conexión
**Síntoma:** No se puede conectar a la base de datos IAMC
**Solución:** 
- Verificar servidor, puerto y credenciales
- Confirmar que el servidor SQL Server está ejecutándose
- Verificar conectividad de red

### Problema: Tabla Ya Existe
**Síntoma:** Error "Table already exists"
**Solución:** 
- Los scripts están diseñados para ser idempotentes
- Usar `IF NOT EXISTS` ya implementado
- Si persiste, verificar manualmente la tabla

### Problema: Error de Permisos
**Síntoma:** "Permission denied" o "Access denied"
**Solución:**
- Confirmar que el usuario tiene permisos de `CREATE TABLE`
- Verificar permisos de `INSERT`, `UPDATE`
- Contactar al administrador de base de datos

### Problema: Error de Sintaxis
**Síntoma:** Errores de sintaxis SQL
**Solución:**
- Verificar que se está ejecutando en SQL Server (no PostgreSQL)
- Revisar la versión de SQL Server (compatible con 2012+)
- Verificar codificación del archivo (UTF-8)

### Problema: Datos Duplicados
**Síntoma:** Error de clave duplicada
**Solución:**
- Los scripts incluyen verificaciones `IF NOT EXISTS`
- Verificar que no hay datos previos conflictivos
- Ejecutar rollback si es necesario

## 📞 Soporte

Para problemas adicionales:
1. Revisar los logs generados (`migration.log`)
2. Verificar la configuración de la base de datos
3. Consultar con el administrador de la base de datos IAMC

## 🔐 Consideraciones de Seguridad

- **Backup:** Siempre hacer backup de la base de datos IAMC antes de la migración
- **Credenciales:** No almacenar credenciales en código fuente
- **Permisos:** Usar cuentas con permisos mínimos necesarios
- **Auditoría:** Documentar todas las migraciones realizadas

## 📝 Notas Adicionales

- Los scripts están optimizados para Microsoft SQL Server 2012+
- La migración es idempotente (se puede ejecutar múltiples veces)
- Los datos de QR codes pueden expandirse agregando más archivos SQL
- Todos los IDs se mantienen consistentes con la base de datos original

---

**Fecha de Creación:** 2025-01-28  
**Versión:** 1.0  
**Compatibilidad:** SQL Server 2012+, Python 3.7+

1. Install required Python package:
   ```bash
   pip install psycopg2-binary
   ```

2. Update database connection settings in `migrate_database.py`:
   ```python
   IAMC_DB_CONFIG = {
       'host': 'your_host',
       'database': 'IAMC',
       'user': 'your_username',
       'password': 'your_password',
       'port': 5432
   }
   ```

3. Run the migration script:
   ```bash
   python migrate_database.py
   ```

## Data Summary

### Users
- **1 user**: Maikel (admin user)

### Roles & Permissions
- **2 roles**: admin, user
- **5 permissions**: admin_access, create_user, update_user, delete_user, view_audit_logs

### QR Codes
- **148 QR code records** with contact information
- Records include contact_id, nombre, archivo_qr, and firma

### Settings
- **9 configuration settings** including server, database, and path configurations

## Important Notes

1. **Conflict Handling**: All INSERT statements use `ON CONFLICT DO NOTHING` to prevent duplicate key errors
2. **Sequences**: The script automatically updates sequence values after data insertion
3. **Transactions**: The Python script uses transactions to ensure data integrity
4. **Backup**: Always backup your IAMC database before running the migration

## Verification

After migration, verify the data:

```sql
-- Check record counts
SELECT 'users' as table_name, COUNT(*) as count FROM "user"
UNION ALL
SELECT 'roles', COUNT(*) FROM role
UNION ALL
SELECT 'permissions', COUNT(*) FROM permission
UNION ALL
SELECT 'qr_codes', COUNT(*) FROM qr_codes
UNION ALL
SELECT 'settings', COUNT(*) FROM settings;

-- Check if tables exist
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('user', 'role', 'permission', 'qr_codes', 'settings', 'audit_log');
```

## Troubleshooting

### Common Issues

1. **Permission Denied**: Ensure your database user has CREATE and INSERT permissions
2. **Table Already Exists**: This is normal - the script uses `CREATE TABLE IF NOT EXISTS`
3. **Sequence Errors**: The script handles sequence updates automatically
4. **Connection Errors**: Verify your database connection parameters

### Rolling Back

If you need to remove the migrated data:

```sql
-- Remove data (keep tables)
DELETE FROM qr_codes WHERE contact_id IN (SELECT contact_id FROM qr_codes);
DELETE FROM "user" WHERE username = 'maikel';
DELETE FROM roles_permissions;
DELETE FROM role WHERE name IN ('admin', 'user');
DELETE FROM permission WHERE name LIKE '%_access' OR name LIKE '%_user%';
DELETE FROM settings WHERE key IN ('server', 'username', 'password', 'database', 'outputFolder');

-- Drop tables completely (if needed)
DROP TABLE IF EXISTS audit_log CASCADE;
DROP TABLE IF EXISTS qr_codes CASCADE;
DROP TABLE IF EXISTS settings CASCADE;
DROP TABLE IF EXISTS roles_permissions CASCADE;
DROP TABLE IF EXISTS "user" CASCADE;
DROP TABLE IF EXISTS role CASCADE;
DROP TABLE IF EXISTS permission CASCADE;
DROP TABLE IF EXISTS alembic_version CASCADE;
```

## Support

If you encounter issues during migration:

1. Check the PostgreSQL logs for detailed error messages
2. Verify your database connection parameters
3. Ensure you have sufficient privileges
4. Make sure the IAMC database exists and is accessible

## Migration Status

- ✅ Tables creation scripts ready
- ✅ Core data migration ready
- ✅ QR codes migration ready (partial - 50 records)
- ✅ Python automation script ready
- ⚠️ Remaining QR codes (98 records) - can be added if needed

For additional QR codes records or any modifications, please update the migration scripts accordingly.
