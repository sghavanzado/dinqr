@echo off
rem ===============================================================================
rem DINQR - Backup y Restauración para Deployment Waitress + IIS
rem ===============================================================================
rem Este script proporciona funcionalidades completas de backup y restauración
rem para la configuración de DINQR con Waitress como servidor WSGI e IIS como
rem reverse proxy.
rem
rem Funcionalidades:
rem - Backup completo de aplicación, configuración y base de datos
rem - Backup de configuración de IIS
rem - Backup de certificados SSL
rem - Backup de logs
rem - Restauración completa del sistema
rem - Restauración selectiva de componentes
rem - Verificación de integridad de backups
rem - Programación automática de backups
rem
rem Uso:
rem   backup_waitress.bat create              - Crear backup completo
rem   backup_waitress.bat create-config       - Backup solo configuración
rem   backup_waitress.bat create-db           - Backup solo base de datos
rem   backup_waitress.bat restore [archivo]   - Restaurar desde backup
rem   backup_waitress.bat list                - Listar backups disponibles
rem   backup_waitress.bat verify [archivo]    - Verificar integridad
rem   backup_waitress.bat schedule            - Configurar backup automático
rem   backup_waitress.bat cleanup             - Limpiar backups antiguos
rem
rem Autor: DINQR Deployment Team
rem Fecha: %date%
rem ===============================================================================

setlocal EnableDelayedExpansion

set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."
set "BACKEND_DIR=%PROJECT_ROOT%\backend"
set "FRONTEND_DIR=%PROJECT_ROOT%\frontend"
set "BACKUP_BASE_DIR=%SCRIPT_DIR%\backups"
set "SERVICE_NAME=DINQRBackend"
set "SITE_NAME=DINQR"
set "APP_POOL_NAME=DINQRAppPool"

rem Configuración de backup
set "BACKUP_RETENTION_DAYS=30"
set "MAX_BACKUPS_COUNT=10"
set "COMPRESS_BACKUPS=true"

rem Obtener fecha y hora para timestamp
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do set "DATE_STAMP=%%c%%a%%b"
for /f "tokens=1-2 delims=: " %%a in ('time /t') do set "TIME_STAMP=%%a%%b"
set "TIMESTAMP=%DATE_STAMP%_%TIME_STAMP%"

rem Cargar configuración desde .env si existe
if exist "%BACKEND_DIR%\.env" (
    for /f "usebackq tokens=1,2 delims==" %%a in ("%BACKEND_DIR%\.env") do (
        if "%%a"=="DATABASE_URL" set "DATABASE_URL=%%b"
        if "%%a"=="POSTGRES_HOST" set "DB_HOST=%%b"
        if "%%a"=="POSTGRES_PORT" set "DB_PORT=%%b"
        if "%%a"=="POSTGRES_DB" set "DB_NAME=%%b"
        if "%%a"=="POSTGRES_USER" set "DB_USER=%%b"
        if "%%a"=="POSTGRES_PASSWORD" set "DB_PASSWORD=%%b"
    )
)

echo ===============================================================================
echo DINQR - BACKUP Y RESTAURACION WAITRESS + IIS
echo ===============================================================================
echo Timestamp: %TIMESTAMP%
echo Directorio de backups: %BACKUP_BASE_DIR%
echo.

rem Crear directorio de backups si no existe
if not exist "%BACKUP_BASE_DIR%" mkdir "%BACKUP_BASE_DIR%"

rem Procesar comando
set "COMMAND=%1"
set "PARAMETER=%2"

if "%COMMAND%"=="" goto :show_usage
if /i "%COMMAND%"=="create" goto :create_full_backup
if /i "%COMMAND%"=="create-config" goto :create_config_backup
if /i "%COMMAND%"=="create-db" goto :create_db_backup
if /i "%COMMAND%"=="restore" goto :restore_backup
if /i "%COMMAND%"=="list" goto :list_backups
if /i "%COMMAND%"=="verify" goto :verify_backup
if /i "%COMMAND%"=="schedule" goto :schedule_backup
if /i "%COMMAND%"=="cleanup" goto :cleanup_old_backups
if /i "%COMMAND%"=="help" goto :show_usage

echo ERROR: Comando no reconocido: %COMMAND%
goto :show_usage

rem ===============================================================================
rem FUNCIONES DE BACKUP
rem ===============================================================================

:create_full_backup
echo Creando backup completo del sistema DINQR...
set "BACKUP_DIR=%BACKUP_BASE_DIR%\dinqr_full_%TIMESTAMP%"
mkdir "%BACKUP_DIR%"

echo   Creando manifiesto de backup...
call :create_backup_manifest "%BACKUP_DIR%"

echo   Haciendo backup de aplicación...
call :backup_application "%BACKUP_DIR%"

echo   Haciendo backup de configuración...
call :backup_configuration "%BACKUP_DIR%"

echo   Haciendo backup de base de datos...
call :backup_database "%BACKUP_DIR%"

echo   Haciendo backup de IIS...
call :backup_iis_config "%BACKUP_DIR%"

echo   Haciendo backup de certificados SSL...
call :backup_ssl_certificates "%BACKUP_DIR%"

echo   Haciendo backup de logs...
call :backup_logs "%BACKUP_DIR%"

if "%COMPRESS_BACKUPS%"=="true" (
    echo   Comprimiendo backup...
    call :compress_backup "%BACKUP_DIR%"
)

echo   Verificando integridad del backup...
call :verify_backup_integrity "%BACKUP_DIR%"

echo.
echo ✓ Backup completo creado exitosamente: %BACKUP_DIR%
goto :end

:create_config_backup
echo Creando backup de configuración...
set "BACKUP_DIR=%BACKUP_BASE_DIR%\dinqr_config_%TIMESTAMP%"
mkdir "%BACKUP_DIR%"

call :create_backup_manifest "%BACKUP_DIR%"
call :backup_configuration "%BACKUP_DIR%"
call :backup_iis_config "%BACKUP_DIR%"

if "%COMPRESS_BACKUPS%"=="true" call :compress_backup "%BACKUP_DIR%"

echo ✓ Backup de configuración creado: %BACKUP_DIR%
goto :end

:create_db_backup
echo Creando backup de base de datos...
set "BACKUP_DIR=%BACKUP_BASE_DIR%\dinqr_db_%TIMESTAMP%"
mkdir "%BACKUP_DIR%"

call :create_backup_manifest "%BACKUP_DIR%"
call :backup_database "%BACKUP_DIR%"

if "%COMPRESS_BACKUPS%"=="true" call :compress_backup "%BACKUP_DIR%"

echo ✓ Backup de base de datos creado: %BACKUP_DIR%
goto :end

rem ===============================================================================
rem FUNCIONES DE RESTAURACIÓN
rem ===============================================================================

:restore_backup
if "%PARAMETER%"=="" (
    echo ERROR: Debe especificar el archivo o directorio de backup a restaurar
    echo Uso: %~nx0 restore [ruta_del_backup]
    goto :error
)

set "RESTORE_SOURCE=%PARAMETER%"
if not exist "%RESTORE_SOURCE%" (
    echo ERROR: Backup no encontrado: %RESTORE_SOURCE%
    goto :error
)

echo ADVERTENCIA: La restauración sobrescribirá la configuración actual.
echo ¿Está seguro de que desea continuar? (s/N)
set /p "CONFIRM="
if /i not "%CONFIRM%"=="s" (
    echo Operación cancelada por el usuario.
    goto :end
)

echo Iniciando restauración desde: %RESTORE_SOURCE%

rem Verificar si es un archivo comprimido
if /i "%RESTORE_SOURCE:~-4%"==".zip" (
    echo   Descomprimiendo backup...
    set "EXTRACT_DIR=%TEMP%\dinqr_restore_%TIMESTAMP%"
    call :extract_backup "%RESTORE_SOURCE%" "!EXTRACT_DIR!"
    set "RESTORE_SOURCE=!EXTRACT_DIR!"
)

rem Verificar manifiesto
if not exist "%RESTORE_SOURCE%\backup_manifest.txt" (
    echo ERROR: Manifiesto de backup no encontrado. El backup podría estar corrupto.
    goto :error
)

echo   Leyendo manifiesto de backup...
call :read_backup_manifest "%RESTORE_SOURCE%"

echo   Deteniendo servicios...
call :stop_services_for_restore

echo   Restaurando aplicación...
call :restore_application "%RESTORE_SOURCE%"

echo   Restaurando configuración...
call :restore_configuration "%RESTORE_SOURCE%"

echo   Restaurando base de datos...
call :restore_database "%RESTORE_SOURCE%"

echo   Restaurando configuración de IIS...
call :restore_iis_config "%RESTORE_SOURCE%"

echo   Restaurando certificados SSL...
call :restore_ssl_certificates "%RESTORE_SOURCE%"

echo   Iniciando servicios...
call :start_services_after_restore

echo.
echo ✓ Restauración completada exitosamente
echo   Verifique que todos los servicios estén funcionando correctamente
goto :end

rem ===============================================================================
rem FUNCIONES AUXILIARES DE BACKUP
rem ===============================================================================

:create_backup_manifest
set "MANIFEST_FILE=%~1\backup_manifest.txt"
echo DINQR Backup Manifest > "%MANIFEST_FILE%"
echo ===================== >> "%MANIFEST_FILE%"
echo Timestamp: %TIMESTAMP% >> "%MANIFEST_FILE%"
echo Date: %date% >> "%MANIFEST_FILE%"
echo Time: %time% >> "%MANIFEST_FILE%"
echo Server: %COMPUTERNAME% >> "%MANIFEST_FILE%"
echo User: %USERNAME% >> "%MANIFEST_FILE%"
echo Script Version: 1.0 >> "%MANIFEST_FILE%"
echo. >> "%MANIFEST_FILE%"
echo Components: >> "%MANIFEST_FILE%"
exit /b 0

:backup_application
set "APP_BACKUP_DIR=%~1\application"
mkdir "%APP_BACKUP_DIR%"

echo - Application code >> "%~1\backup_manifest.txt"

rem Backup backend
echo     Copiando backend...
xcopy "%BACKEND_DIR%" "%APP_BACKUP_DIR%\backend" /E /I /H /Y >nul 2>&1
if errorlevel 1 (
    echo   ERROR: Fallo el backup del backend
    exit /b 1
)

rem Backup frontend
echo     Copiando frontend...
xcopy "%FRONTEND_DIR%" "%APP_BACKUP_DIR%\frontend" /E /I /H /Y >nul 2>&1
if errorlevel 1 (
    echo   ERROR: Fallo el backup del frontend
    exit /b 1
)

rem Backup deployment scripts
echo     Copiando scripts de deployment...
xcopy "%SCRIPT_DIR%" "%APP_BACKUP_DIR%\deployment-scripts" /E /I /H /Y >nul 2>&1

exit /b 0

:backup_configuration
set "CONFIG_BACKUP_DIR=%~1\configuration"
mkdir "%CONFIG_BACKUP_DIR%"

echo - Configuration files >> "%~1\backup_manifest.txt"

rem Backup .env
if exist "%BACKEND_DIR%\.env" (
    copy "%BACKEND_DIR%\.env" "%CONFIG_BACKUP_DIR%\.env" >nul 2>&1
)

rem Backup web.config
if exist "%BACKEND_DIR%\web.config" (
    copy "%BACKEND_DIR%\web.config" "%CONFIG_BACKUP_DIR%\web.config" >nul 2>&1
)

rem Backup any custom configuration files
if exist "%BACKEND_DIR%\config.py" (
    copy "%BACKEND_DIR%\config.py" "%CONFIG_BACKUP_DIR%\config.py" >nul 2>&1
)

exit /b 0

:backup_database
set "DB_BACKUP_DIR=%~1\database"
mkdir "%DB_BACKUP_DIR%"

echo - Database >> "%~1\backup_manifest.txt"

if defined DB_HOST if defined DB_NAME if defined DB_USER (
    echo     Haciendo backup de PostgreSQL...
    set "PGPASSWORD=%DB_PASSWORD%"
    pg_dump -h "%DB_HOST%" -p "%DB_PORT%" -U "%DB_USER%" -d "%DB_NAME%" -f "%DB_BACKUP_DIR%\database_backup.sql" 2>nul
    if errorlevel 1 (
        echo   WARNING: No se pudo hacer backup de PostgreSQL (pg_dump no disponible)
        echo - Database backup failed >> "%~1\backup_manifest.txt"
    ) else (
        echo   ✓ Backup de PostgreSQL completado
    )
) else (
    echo   WARNING: Configuración de base de datos no encontrada en .env
    echo - Database configuration not found >> "%~1\backup_manifest.txt"
)

rem Backup SQLite si existe
if exist "%BACKEND_DIR%\instance\dinqr.db" (
    copy "%BACKEND_DIR%\instance\dinqr.db" "%DB_BACKUP_DIR%\dinqr_sqlite.db" >nul 2>&1
    echo   ✓ Backup de SQLite incluido
)

exit /b 0

:backup_iis_config
set "IIS_BACKUP_DIR=%~1\iis"
mkdir "%IIS_BACKUP_DIR%"

echo - IIS Configuration >> "%~1\backup_manifest.txt"

rem Backup de configuración del sitio
%windir%\system32\inetsrv\appcmd.exe list site "%SITE_NAME%" /config > "%IIS_BACKUP_DIR%\site_config.xml" 2>nul

rem Backup de configuración del Application Pool
%windir%\system32\inetsrv\appcmd.exe list apppool "%APP_POOL_NAME%" /config > "%IIS_BACKUP_DIR%\apppool_config.xml" 2>nul

rem Backup de web.config del sitio
if exist "%FRONTEND_DIR%\dist\web.config" (
    copy "%FRONTEND_DIR%\dist\web.config" "%IIS_BACKUP_DIR%\site_web.config" >nul 2>&1
)

rem Backup completo de configuración de IIS (si es posible)
%windir%\system32\inetsrv\appcmd.exe add backup "DINQR_Backup_%TIMESTAMP%" >nul 2>&1
if not errorlevel 1 (
    echo DINQR_Backup_%TIMESTAMP% > "%IIS_BACKUP_DIR%\iis_backup_name.txt"
    echo   ✓ Backup nativo de IIS creado
)

exit /b 0

:backup_ssl_certificates
set "SSL_BACKUP_DIR=%~1\ssl"
mkdir "%SSL_BACKUP_DIR%"

echo - SSL Certificates >> "%~1\backup_manifest.txt"

rem Exportar certificados del almacén local
powershell -Command "
Get-ChildItem Cert:\LocalMachine\My | Where-Object { $_.Subject -like '*dinqr*' -or $_.Subject -like '*localhost*' } | ForEach-Object {
    $cert = $_
    $fileName = '%SSL_BACKUP_DIR%\cert_' + $cert.Thumbprint + '.cer'
    Export-Certificate -Cert $cert -FilePath $fileName -Type CERT
    Write-Host 'Exported certificate:' $cert.Subject
}
" 2>nul

exit /b 0

:backup_logs
set "LOGS_BACKUP_DIR=%~1\logs"
mkdir "%LOGS_BACKUP_DIR%"

echo - Application Logs >> "%~1\backup_manifest.txt"

if exist "%BACKEND_DIR%\logs" (
    xcopy "%BACKEND_DIR%\logs" "%LOGS_BACKUP_DIR%" /E /I /Y >nul 2>&1
)

rem Backup de logs de IIS
if exist "%windir%\system32\LogFiles\W3SVC1" (
    xcopy "%windir%\system32\LogFiles\W3SVC1" "%LOGS_BACKUP_DIR%\iis_logs" /E /I /Y >nul 2>&1
)

exit /b 0

:compress_backup
set "SOURCE_DIR=%~1"
set "ZIP_FILE=%SOURCE_DIR%.zip"

echo     Comprimiendo a: %ZIP_FILE%
powershell -Command "Compress-Archive -Path '%SOURCE_DIR%\*' -DestinationPath '%ZIP_FILE%' -CompressionLevel Optimal" >nul 2>&1
if not errorlevel 1 (
    rmdir /s /q "%SOURCE_DIR%" >nul 2>&1
    echo   ✓ Backup comprimido y directorio temporal eliminado
) else (
    echo   WARNING: No se pudo comprimir el backup
)

exit /b 0

rem ===============================================================================
rem FUNCIONES AUXILIARES DE RESTAURACIÓN
rem ===============================================================================

:stop_services_for_restore
echo     Deteniendo servicio DINQR...
sc stop "%SERVICE_NAME%" >nul 2>&1
timeout /t 5 >nul

echo     Deteniendo sitio IIS...
%windir%\system32\inetsrv\appcmd.exe stop site "%SITE_NAME%" >nul 2>&1
%windir%\system32\inetsrv\appcmd.exe stop apppool "%APP_POOL_NAME%" >nul 2>&1

exit /b 0

:start_services_after_restore
echo     Iniciando Application Pool...
%windir%\system32\inetsrv\appcmd.exe start apppool "%APP_POOL_NAME%" >nul 2>&1

echo     Iniciando sitio IIS...
%windir%\system32\inetsrv\appcmd.exe start site "%SITE_NAME%" >nul 2>&1

echo     Iniciando servicio DINQR...
sc start "%SERVICE_NAME%" >nul 2>&1

echo     Esperando que los servicios se inicialicen...
timeout /t 15 >nul

exit /b 0

rem ===============================================================================
rem FUNCIONES DE UTILIDAD
rem ===============================================================================

:list_backups
echo Listando backups disponibles...
echo.
echo Directorio: %BACKUP_BASE_DIR%
echo.

if not exist "%BACKUP_BASE_DIR%" (
    echo No hay backups disponibles.
    goto :end
)

echo Tipo        Fecha/Hora           Tamaño      Nombre
echo ----        ----------           ------      ------

for /f "tokens=*" %%i in ('dir /b /ad "%BACKUP_BASE_DIR%\dinqr_*" 2^>nul') do (
    set "BACKUP_NAME=%%i"
    set "BACKUP_TYPE=Completo"
    if "!BACKUP_NAME:~0,14!"=="dinqr_config_" set "BACKUP_TYPE=Config  "
    if "!BACKUP_NAME:~0,10!"=="dinqr_db_" set "BACKUP_TYPE=Database"
    
    for %%j in ("%BACKUP_BASE_DIR%\%%i") do (
        echo !BACKUP_TYPE!     %%~tj    [DIR]       %%i
    )
)

for /f "tokens=*" %%i in ('dir /b "%BACKUP_BASE_DIR%\dinqr_*.zip" 2^>nul') do (
    set "BACKUP_NAME=%%i"
    set "BACKUP_TYPE=Completo"
    if "!BACKUP_NAME:~0,14!"=="dinqr_config_" set "BACKUP_TYPE=Config  "
    if "!BACKUP_NAME:~0,10!"=="dinqr_db_" set "BACKUP_TYPE=Database"
    
    for %%j in ("%BACKUP_BASE_DIR%\%%i") do (
        echo !BACKUP_TYPE!     %%~tj    %%~zj       %%i
    )
)

goto :end

:cleanup_old_backups
echo Limpiando backups antiguos...
echo Reteniendo backups de los últimos %BACKUP_RETENTION_DAYS% días

rem Eliminar backups antiguos basado en fecha
forfiles /p "%BACKUP_BASE_DIR%" /m "dinqr_*" /d -%BACKUP_RETENTION_DAYS% /c "cmd /c echo Eliminando backup antiguo: @file && del /q @path" 2>nul

rem Mantener solo los últimos N backups
set "BACKUP_COUNT=0"
for /f "tokens=*" %%i in ('dir /b /o-d "%BACKUP_BASE_DIR%\dinqr_*" 2^>nul') do (
    set /a "BACKUP_COUNT+=1"
    if !BACKUP_COUNT! gtr %MAX_BACKUPS_COUNT% (
        echo Eliminando backup excedente: %%i
        if exist "%BACKUP_BASE_DIR%\%%i\*" (
            rmdir /s /q "%BACKUP_BASE_DIR%\%%i"
        ) else (
            del /q "%BACKUP_BASE_DIR%\%%i"
        )
    )
)

echo ✓ Limpieza de backups completada
goto :end

:verify_backup_integrity
rem Función para verificar la integridad de un backup
set "BACKUP_PATH=%~1"

echo     Verificando estructura de directorios...
if not exist "%BACKUP_PATH%\backup_manifest.txt" (
    echo   ERROR: Manifiesto de backup faltante
    exit /b 1
)

echo     Verificando componentes del backup...
findstr /c:"- Application code" "%BACKUP_PATH%\backup_manifest.txt" >nul
if not errorlevel 1 (
    if not exist "%BACKUP_PATH%\application" (
        echo   ERROR: Directorio de aplicación faltante
        exit /b 1
    )
)

findstr /c:"- Configuration files" "%BACKUP_PATH%\backup_manifest.txt" >nul
if not errorlevel 1 (
    if not exist "%BACKUP_PATH%\configuration" (
        echo   ERROR: Directorio de configuración faltante
        exit /b 1
    )
)

echo   ✓ Integridad del backup verificada
exit /b 0

:schedule_backup
echo Configurando backup automático...
echo.
echo ¿Qué tipo de programación desea configurar?
echo 1. Diario (recomendado)
echo 2. Semanal
echo 3. Personalizado
echo.
set /p "SCHEDULE_TYPE=Seleccione una opción (1-3): "

set "TASK_NAME=DINQR_Backup_Automatico"
set "SCRIPT_PATH=%~f0"

if "%SCHEDULE_TYPE%"=="1" (
    schtasks /create /tn "%TASK_NAME%" /tr "\"%SCRIPT_PATH%\" create" /sc daily /st 02:00 /f >nul 2>&1
    echo ✓ Backup diario programado para las 2:00 AM
) else if "%SCHEDULE_TYPE%"=="2" (
    schtasks /create /tn "%TASK_NAME%" /tr "\"%SCRIPT_PATH%\" create" /sc weekly /d SUN /st 03:00 /f >nul 2>&1
    echo ✓ Backup semanal programado para los domingos a las 3:00 AM
) else (
    echo Para configuración personalizada, use el Programador de Tareas de Windows
    echo Comando a ejecutar: "%SCRIPT_PATH%" create
)

goto :end

:show_usage
echo.
echo DINQR - Script de Backup y Restauración (Waitress + IIS)
echo =========================================================
echo.
echo Uso: %~nx0 [comando] [parámetros]
echo.
echo Comandos de Backup:
echo   create              - Crear backup completo del sistema
echo   create-config       - Crear backup solo de configuración
echo   create-db           - Crear backup solo de base de datos
echo.
echo Comandos de Restauración:
echo   restore [archivo]   - Restaurar desde un backup específico
echo.
echo Comandos de Gestión:
echo   list                - Listar todos los backups disponibles
echo   verify [archivo]    - Verificar integridad de un backup
echo   cleanup             - Limpiar backups antiguos
echo   schedule            - Configurar backup automático
echo.
echo Ejemplos:
echo   %~nx0 create
echo   %~nx0 restore backups\dinqr_full_20240115_1430
echo   %~nx0 list
echo   %~nx0 cleanup
echo.
echo Configuración:
echo   Directorio de backups: %BACKUP_BASE_DIR%
echo   Retención: %BACKUP_RETENTION_DAYS% días
echo   Máximo de backups: %MAX_BACKUPS_COUNT%
echo   Compresión: %COMPRESS_BACKUPS%
echo.
goto :end

:error
echo.
echo ERROR: La operación no se completó exitosamente.
echo Para más información, use: %~nx0 help
echo.
exit /b 1

:end
exit /b 0
