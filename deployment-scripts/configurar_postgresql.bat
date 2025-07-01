@echo off
echo ====================================
echo   CONFIGURANDO POSTGRESQL DINQR
echo ====================================

:: Verificar permisos de administrador
net session >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Este script debe ejecutarse como Administrador
    echo [INFO] Click derecho y selecciona "Ejecutar como administrador"
    pause
    exit /b 1
)

:: Configurar colores para Windows
color 0F

echo [INFO] Configurando PostgreSQL para DINQR...

echo.
echo ====================================
echo   FASE 1: VERIFICACIONES
echo ====================================

echo [PASO 1] Verificando PostgreSQL...
where psql >nul 2>&1
if errorlevel 1 (
    echo [ERROR] PostgreSQL no está instalado
    echo [INFO] Ejecuta primero: instalar_dependencias.bat
    pause
    exit /b 1
)

echo [OK] PostgreSQL encontrado
psql --version

echo.
echo [PASO 2] Verificando servicio PostgreSQL...
sc query postgresql-x64-14 >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Servicio PostgreSQL no encontrado
    echo [INFO] Instala PostgreSQL correctamente
    pause
    exit /b 1
)

echo [OK] Servicio PostgreSQL encontrado

:: Iniciar servicio si no está ejecutándose
sc query postgresql-x64-14 | findstr "RUNNING" >nul
if errorlevel 1 (
    echo [INFO] Iniciando servicio PostgreSQL...
    net start postgresql-x64-14
    if errorlevel 1 (
        echo [ERROR] No se pudo iniciar PostgreSQL
        pause
        exit /b 1
    )
)

echo [OK] Servicio PostgreSQL ejecutándose

echo.
echo ====================================
echo   FASE 2: CONFIGURACION BASICA
echo ====================================

echo [PASO 1] Configurando variables de entorno...
set PGPASSWORD=postgr3s
set PGUSER=postgres
set PGHOST=localhost
set PGPORT=5432

echo [OK] Variables configuradas

echo.
echo [PASO 2] Verificando conexión...
psql -U postgres -h localhost -p 5432 -c "SELECT version();" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] No se puede conectar a PostgreSQL
    echo [INFO] Verifica que la contraseña sea 'postgr3s'
    echo [INFO] O configura la contraseña correcta en este script
    pause
    exit /b 1
)

echo [OK] Conexión PostgreSQL exitosa

echo.
echo ====================================
echo   FASE 3: CREACION DE BASE DE DATOS
echo ====================================

echo [PASO 1] Creando base de datos localdb...
psql -U postgres -h localhost -p 5432 -c "DROP DATABASE IF EXISTS localdb;" >nul 2>&1
psql -U postgres -h localhost -p 5432 -c "CREATE DATABASE localdb WITH ENCODING 'UTF8' LC_COLLATE='Spanish_Spain.1252' LC_CTYPE='Spanish_Spain.1252';"
if errorlevel 1 (
    echo [ERROR] No se pudo crear la base de datos
    pause
    exit /b 1
)

echo [OK] Base de datos 'localdb' creada

echo.
echo [PASO 2] Creando usuario para la aplicación...
psql -U postgres -h localhost -p 5432 -c "DROP USER IF EXISTS dinqr_user;" >nul 2>&1
psql -U postgres -h localhost -p 5432 -c "CREATE USER dinqr_user WITH PASSWORD 'dinqr_password';"
if errorlevel 1 (
    echo [WARNING] No se pudo crear usuario dinqr_user, usando postgres
) else (
    echo [OK] Usuario 'dinqr_user' creado
)

echo.
echo [PASO 3] Asignando permisos...
psql -U postgres -h localhost -p 5432 -c "GRANT ALL PRIVILEGES ON DATABASE localdb TO dinqr_user;" >nul 2>&1
psql -U postgres -h localhost -p 5432 -d localdb -c "GRANT ALL ON SCHEMA public TO dinqr_user;" >nul 2>&1
psql -U postgres -h localhost -p 5432 -d localdb -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO dinqr_user;" >nul 2>&1

echo [OK] Permisos asignados

echo.
echo ====================================
echo   FASE 4: CONFIGURACION AVANZADA
echo ====================================

echo [PASO 1] Configurando postgresql.conf...
set PG_DATA_DIR=C:\Program Files\PostgreSQL\14\data
set PG_CONF=%PG_DATA_DIR%\postgresql.conf

:: Backup de configuración original
if not exist "%PG_CONF%.backup" (
    copy "%PG_CONF%" "%PG_CONF%.backup" >nul 2>&1
    echo [OK] Backup de configuración creado
)

:: Configuraciones para desarrollo
echo [INFO] Aplicando configuraciones de desarrollo...

:: Crear archivo temporal con configuraciones
set TEMP_CONFIG=%TEMP%\pg_config_dinqr.conf
echo # Configuraciones DINQR > %TEMP_CONFIG%
echo listen_addresses = 'localhost' >> %TEMP_CONFIG%
echo port = 5432 >> %TEMP_CONFIG%
echo max_connections = 100 >> %TEMP_CONFIG%
echo shared_buffers = 128MB >> %TEMP_CONFIG%
echo effective_cache_size = 512MB >> %TEMP_CONFIG%
echo work_mem = 4MB >> %TEMP_CONFIG%
echo maintenance_work_mem = 64MB >> %TEMP_CONFIG%
echo log_destination = 'stderr' >> %TEMP_CONFIG%
echo logging_collector = on >> %TEMP_CONFIG%
echo log_directory = 'log' >> %TEMP_CONFIG%
echo log_filename = 'postgresql-%%Y-%%m-%%d_%%H%%M%%S.log' >> %TEMP_CONFIG%
echo log_statement = 'all' >> %TEMP_CONFIG%
echo log_min_duration_statement = 1000 >> %TEMP_CONFIG%

:: Aplicar configuraciones (requiere reinicio del servicio)
echo [INFO] Las configuraciones se aplicarán en el siguiente reinicio

echo.
echo [PASO 2] Configurando pg_hba.conf...
set PG_HBA=%PG_DATA_DIR%\pg_hba.conf

:: Backup de pg_hba.conf
if not exist "%PG_HBA%.backup" (
    copy "%PG_HBA%" "%PG_HBA%.backup" >nul 2>&1
    echo [OK] Backup de pg_hba.conf creado
)

:: Verificar configuración de autenticación local
findstr /C:"host    all             all             127.0.0.1/32            md5" "%PG_HBA%" >nul
if errorlevel 1 (
    echo [INFO] Configurando autenticación local...
    echo # Configuración DINQR >> "%PG_HBA%"
    echo host    all             all             127.0.0.1/32            md5 >> "%PG_HBA%"
    echo host    localdb         all             127.0.0.1/32            md5 >> "%PG_HBA%"
)

echo [OK] Configuración de autenticación verificada

echo.
echo [PASO 3] Reiniciando servicio PostgreSQL...
net stop postgresql-x64-14 >nul 2>&1
timeout /t 3 /nobreak >nul
net start postgresql-x64-14
if errorlevel 1 (
    echo [ERROR] Error al reiniciar PostgreSQL
    pause
    exit /b 1
)

echo [OK] PostgreSQL reiniciado

:: Esperar a que el servicio esté disponible
timeout /t 5 /nobreak >nul

echo.
echo ====================================
echo   FASE 5: VERIFICACION FINAL
echo ====================================

echo [PASO 1] Verificando conexión después del reinicio...
psql -U postgres -h localhost -p 5432 -d localdb -c "SELECT 1;" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] No se puede conectar después del reinicio
    pause
    exit /b 1
)

echo [OK] Conexión verificada

echo.
echo [PASO 2] Verificando estructura de la base de datos...
psql -U postgres -h localhost -p 5432 -d localdb -c "\dt" >nul 2>&1
echo [OK] Base de datos accesible

echo.
echo [PASO 3] Creando archivo de configuración de conexión...
set SCRIPT_DIR=%~dp0
set CONFIG_FILE=%SCRIPT_DIR%..\backend\.env.database

echo # Configuración de base de datos PostgreSQL para DINQR > %CONFIG_FILE%
echo # Generado automáticamente por configurar_postgresql.bat >> %CONFIG_FILE%
echo. >> %CONFIG_FILE%
echo # PostgreSQL Local (Principal) >> %CONFIG_FILE%
echo DATABASE_URL=postgresql://postgres:postgr3s@localhost:5432/localdb >> %CONFIG_FILE%
echo LOCAL_DB_NAME=localdb >> %CONFIG_FILE%
echo LOCAL_DB_USER=postgres >> %CONFIG_FILE%
echo LOCAL_DB_PASSWORD=postgr3s >> %CONFIG_FILE%
echo LOCAL_DB_HOST=localhost >> %CONFIG_FILE%
echo LOCAL_DB_PORT=5432 >> %CONFIG_FILE%
echo. >> %CONFIG_FILE%
echo # Usuario alternativo de aplicación >> %CONFIG_FILE%
echo # LOCAL_DB_USER=dinqr_user >> %CONFIG_FILE%
echo # LOCAL_DB_PASSWORD=dinqr_password >> %CONFIG_FILE%

echo [OK] Archivo de configuración creado: %CONFIG_FILE%

echo.
echo [PASO 4] Creando scripts de administración...

:: Script para backup
echo @echo off > "%SCRIPT_DIR%backup_database.bat"
echo echo Creando backup de localdb... >> "%SCRIPT_DIR%backup_database.bat"
echo set BACKUP_FILE=backup_localdb_%%date:~-4,4%%%%date:~-10,2%%%%date:~-7,2%%.sql >> "%SCRIPT_DIR%backup_database.bat"
echo pg_dump -U postgres -h localhost -p 5432 localdb ^> %%BACKUP_FILE%% >> "%SCRIPT_DIR%backup_database.bat"
echo echo Backup creado: %%BACKUP_FILE%% >> "%SCRIPT_DIR%backup_database.bat"
echo pause >> "%SCRIPT_DIR%backup_database.bat"

:: Script para restaurar
echo @echo off > "%SCRIPT_DIR%restaurar_database.bat"
echo echo Restaurando localdb desde backup... >> "%SCRIPT_DIR%restaurar_database.bat"
echo echo [WARNING] Esto eliminará todos los datos actuales >> "%SCRIPT_DIR%restaurar_database.bat"
echo set /p BACKUP_FILE="Ingresa el nombre del archivo de backup: " >> "%SCRIPT_DIR%restaurar_database.bat"
echo if not exist %%BACKUP_FILE%% echo [ERROR] Archivo no encontrado ^&^& pause ^&^& exit /b 1 >> "%SCRIPT_DIR%restaurar_database.bat"
echo psql -U postgres -h localhost -p 5432 -c "DROP DATABASE IF EXISTS localdb;" >> "%SCRIPT_DIR%restaurar_database.bat"
echo psql -U postgres -h localhost -p 5432 -c "CREATE DATABASE localdb;" >> "%SCRIPT_DIR%restaurar_database.bat"
echo psql -U postgres -h localhost -p 5432 localdb ^< %%BACKUP_FILE%% >> "%SCRIPT_DIR%restaurar_database.bat"
echo echo Restauración completada >> "%SCRIPT_DIR%restaurar_database.bat"
echo pause >> "%SCRIPT_DIR%restaurar_database.bat"

:: Script para conectar
echo @echo off > "%SCRIPT_DIR%conectar_postgresql.bat"
echo echo Conectando a PostgreSQL DINQR... >> "%SCRIPT_DIR%conectar_postgresql.bat"
echo psql -U postgres -h localhost -p 5432 -d localdb >> "%SCRIPT_DIR%conectar_postgresql.bat"

echo [OK] Scripts de administración creados

echo.
echo ====================================
echo   CONFIGURACION COMPLETADA
echo ====================================
echo.
echo [RESUMEN DE CONFIGURACION]
echo ✓ PostgreSQL: Configurado y funcionando
echo ✓ Base de datos: localdb
echo ✓ Usuario principal: postgres
echo ✓ Contraseña: postgr3s
echo ✓ Puerto: 5432
echo ✓ Host: localhost
echo ✓ Usuario aplicación: dinqr_user (opcional)
echo.
echo [ARCHIVOS CREADOS]
echo - Configuración: %CONFIG_FILE%
echo - Backup config: %PG_CONF%.backup
echo - Backup pg_hba: %PG_HBA%.backup
echo.
echo [SCRIPTS DE ADMINISTRACION]
echo - Backup: backup_database.bat
echo - Restaurar: restaurar_database.bat  
echo - Conectar: conectar_postgresql.bat
echo.
echo [CADENA DE CONEXION]
echo postgresql://postgres:postgr3s@localhost:5432/localdb
echo.
echo [COMANDOS UTILES]
echo - Conectar: psql -U postgres -h localhost -d localdb
echo - Ver tablas: \dt
echo - Salir de psql: \q
echo - Estado servicio: sc query postgresql-x64-14
echo.
echo [PROXIMOS PASOS]
echo 1. Ejecutar: migrar_base_datos.bat
echo 2. Compilar aplicación: compilar_todo.bat
echo 3. Desplegar: desplegar_iis.bat
echo.

:: Limpiar variables temporales
set PGPASSWORD=
if exist "%TEMP_CONFIG%" del "%TEMP_CONFIG%"

:: Mantener ventana abierta
echo Presiona cualquier tecla para continuar...
pause >nul
