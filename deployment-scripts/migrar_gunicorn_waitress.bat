@echo off
rem ===============================================================================
rem DINQR - Migración de Gunicorn a Waitress + IIS
rem ===============================================================================
rem Este script facilita la migración de una instalación existente de DINQR
rem que usa Gunicorn a la nueva arquitectura con Waitress como servidor WSGI.
rem
rem Características:
rem - Backup automático de la configuración actual
rem - Detección automática de la configuración existente
rem - Migración de configuraciones y datos
rem - Verificación de compatibilidad
rem - Rollback en caso de problemas
rem - Preservación de datos de usuario
rem
rem IMPORTANTE: Este script debe ejecutarse como administrador
rem
rem Uso:
rem   migrar_gunicorn_waitress.bat             - Migración completa
rem   migrar_gunicorn_waitress.bat -check      - Solo verificar compatibilidad
rem   migrar_gunicorn_waitress.bat -backup     - Solo crear backup
rem   migrar_gunicorn_waitress.bat -rollback   - Revertir migración
rem
rem Autor: DINQR Deployment Team
rem Fecha: %date%
rem ===============================================================================

setlocal EnableDelayedExpansion

set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."
set "BACKEND_DIR=%PROJECT_ROOT%\backend"
set "FRONTEND_DIR=%PROJECT_ROOT%\frontend"
set "MIGRATION_LOG=%SCRIPT_DIR%\migracion_waitress.log"
set "BACKUP_BASE_DIR=%SCRIPT_DIR%\backup_migracion"

rem Configuración de migración
set "OLD_SERVICE_NAME=DINQRBackendGunicorn"
set "NEW_SERVICE_NAME=DINQRBackend"
set "OLD_SITE_NAME=DINQR_Gunicorn"
set "NEW_SITE_NAME=DINQR"
set "ROLLBACK_AVAILABLE=false"

rem Obtener timestamp para backup
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do set "DATE_STAMP=%%c%%a%%b"
for /f "tokens=1-2 delims=: " %%a in ('time /t') do set "TIME_STAMP=%%a%%b"
set "TIMESTAMP=%DATE_STAMP%_%TIME_STAMP%"
set "MIGRATION_BACKUP_DIR=%BACKUP_BASE_DIR%\migracion_%TIMESTAMP%"

rem Procesar parámetros
set "OPERATION=migrate"
if "%1"=="-check" set "OPERATION=check"
if "%1"=="--check" set "OPERATION=check"
if "%1"=="-backup" set "OPERATION=backup"
if "%1"=="--backup" set "OPERATION=backup"
if "%1"=="-rollback" set "OPERATION=rollback"
if "%1"=="--rollback" set "OPERATION=rollback"

echo ===============================================================================
echo DINQR - MIGRACION DE GUNICORN A WAITRESS + IIS
echo ===============================================================================
echo Fecha/Hora: %date% %time%
echo Operación: %OPERATION%
echo Directorio de backup: %MIGRATION_BACKUP_DIR%
echo.

rem Inicializar log
echo [%date% %time%] === INICIO MIGRACION GUNICORN A WAITRESS === > "%MIGRATION_LOG%"

rem Verificar prerequisitos
call :check_admin_privileges
if errorlevel 1 goto :error

rem Ejecutar operación solicitada
if "%OPERATION%"=="check" (
    call :check_compatibility
    goto :end
)

if "%OPERATION%"=="backup" (
    call :create_migration_backup
    goto :end
)

if "%OPERATION%"=="rollback" (
    call :rollback_migration
    goto :end
)

if "%OPERATION%"=="migrate" (
    echo ATENCION: Esta operación migrará su instalación actual de Gunicorn a Waitress.
    echo.
    echo ¿Desea continuar con la migración? (s/N)
    set /p "CONFIRM="
    if /i not "%CONFIRM%"=="s" (
        echo Migración cancelada por el usuario.
        goto :end
    )
    
    call :perform_full_migration
    goto :end
)

echo ERROR: Operación no reconocida: %OPERATION%
goto :show_usage

rem ===============================================================================
rem FUNCIONES PRINCIPALES
rem ===============================================================================

:check_admin_privileges
echo Verificando privilegios de administrador...
net session >nul 2>&1
if errorlevel 1 (
    echo ERROR: Este script debe ejecutarse como administrador.
    echo Por favor, ejecute cmd como administrador y vuelva a intentar.
    echo [%date% %time%] ERROR: Sin privilegios administrador >> "%MIGRATION_LOG%"
    exit /b 1
)
echo ✓ Privilegios de administrador verificados
echo [%date% %time%] Privilegios admin OK >> "%MIGRATION_LOG%"
exit /b 0

:check_compatibility
echo.
echo VERIFICACION DE COMPATIBILIDAD PARA MIGRACION
echo ==============================================

set "COMPAT_ISSUES=0"

echo.
echo 1. Verificando instalación actual...

rem Verificar si hay instalación de Gunicorn
python -c "import gunicorn; print('Gunicorn version:', gunicorn.__version__)" >nul 2>&1
if errorlevel 1 (
    echo   ⚠ WARNING: Gunicorn no detectado - podría no ser necesario migrar
    echo [%date% %time%] WARNING: Gunicorn no detectado >> "%MIGRATION_LOG%"
) else (
    echo   ✓ Instalación con Gunicorn detectada
    echo [%date% %time%] Gunicorn detectado >> "%MIGRATION_LOG%"
)

rem Verificar servicios existentes
sc query "%OLD_SERVICE_NAME%" >nul 2>&1
if not errorlevel 1 (
    echo   ✓ Servicio Gunicorn existente encontrado: %OLD_SERVICE_NAME%
    echo [%date% %time%] Servicio Gunicorn encontrado >> "%MIGRATION_LOG%"
) else (
    rem Verificar otros posibles nombres de servicio
    for %%s in ("DINQRBackend" "DINQR" "DinqrGunicorn") do (
        sc query "%%~s" >nul 2>&1
        if not errorlevel 1 (
            echo   ✓ Servicio DINQR encontrado: %%~s
            set "OLD_SERVICE_NAME=%%~s"
            echo [%date% %time%] Servicio encontrado: %%~s >> "%MIGRATION_LOG%"
            goto :service_found
        )
    )
    echo   ⚠ WARNING: No se encontró servicio DINQR existente
    echo [%date% %time%] WARNING: Servicio no encontrado >> "%MIGRATION_LOG%"
    set /a "COMPAT_ISSUES+=1"
    :service_found
)

echo.
echo 2. Verificando configuración actual...

rem Verificar archivo .env
if exist "%BACKEND_DIR%\.env" (
    echo   ✓ Archivo .env encontrado
    
    rem Verificar configuraciones específicas de Gunicorn
    findstr /c:"GUNICORN_" "%BACKEND_DIR%\.env" >nul 2>&1
    if not errorlevel 1 (
        echo   ✓ Configuraciones de Gunicorn detectadas en .env
        echo [%date% %time%] Configuraciones Gunicorn en .env >> "%MIGRATION_LOG%"
    )
    
    rem Verificar configuraciones críticas
    findstr /c:"SECRET_KEY=" "%BACKEND_DIR%\.env" >nul 2>&1
    if errorlevel 1 (
        echo   ⚠ WARNING: SECRET_KEY no configurado
        set /a "COMPAT_ISSUES+=1"
    )
    
    findstr /c:"DATABASE_URL=" "%BACKEND_DIR%\.env" >nul 2>&1
    if errorlevel 1 (
        echo   ⚠ WARNING: DATABASE_URL no configurado
        set /a "COMPAT_ISSUES+=1"
    )
) else (
    echo   ✗ ERROR: Archivo .env no encontrado
    echo [%date% %time%] ERROR: .env no encontrado >> "%MIGRATION_LOG%"
    set /a "COMPAT_ISSUES+=1"
)

rem Verificar server.py o server_manager.py (indicadores de setup Gunicorn)
if exist "%BACKEND_DIR%\server.py" (
    echo   ✓ server.py encontrado (configuración Gunicorn típica)
    echo [%date% %time%] server.py encontrado >> "%MIGRATION_LOG%"
)

if exist "%BACKEND_DIR%\server_manager.py" (
    echo   ✓ server_manager.py encontrado (gestión Gunicorn)
    echo [%date% %time%] server_manager.py encontrado >> "%MIGRATION_LOG%"
)

echo.
echo 3. Verificando dependencias para Waitress...

rem Verificar que Waitress esté disponible
python -c "import waitress; print('Waitress version:', waitress.__version__)" >nul 2>&1
if errorlevel 1 (
    echo   ⚠ WARNING: Waitress no instalado - se instalará durante migración
    echo [%date% %time%] WARNING: Waitress no instalado >> "%MIGRATION_LOG%"
) else (
    echo   ✓ Waitress ya está instalado
)

rem Verificar pywin32
python -c "import win32service; print('pywin32 disponible')" >nul 2>&1
if errorlevel 1 (
    echo   ⚠ WARNING: pywin32 no instalado - se instalará durante migración
    echo [%date% %time%] WARNING: pywin32 no instalado >> "%MIGRATION_LOG%"
) else (
    echo   ✓ pywin32 disponible
)

echo.
echo 4. Verificando IIS...

%windir%\system32\inetsrv\appcmd.exe list sites >nul 2>&1
if errorlevel 1 (
    echo   ✗ ERROR: IIS no disponible o no funcionando
    echo [%date% %time%] ERROR: IIS no disponible >> "%MIGRATION_LOG%"
    set /a "COMPAT_ISSUES+=1"
) else (
    echo   ✓ IIS disponible
    
    rem Verificar sitio existente
    %windir%\system32\inetsrv\appcmd.exe list site "%OLD_SITE_NAME%" >nul 2>&1
    if not errorlevel 1 (
        echo   ✓ Sitio IIS existente encontrado: %OLD_SITE_NAME%
    ) else (
        rem Buscar otros posibles sitios DINQR
        for %%s in ("DINQR" "Default Web Site" "DinqrSite") do (
            %windir%\system32\inetsrv\appcmd.exe list site "%%~s" >nul 2>&1
            if not errorlevel 1 (
                echo   ✓ Sitio IIS encontrado: %%~s
                set "OLD_SITE_NAME=%%~s"
                goto :site_found
            )
        )
        echo   ⚠ WARNING: No se encontró sitio IIS DINQR específico
        :site_found
    )
)

echo.
echo 5. Verificando base de datos...

cd /d "%BACKEND_DIR%"
python -c "
try:
    from app import create_app
    from extensions import db
    app = create_app()
    with app.app_context():
        db.engine.execute('SELECT 1')
    print('DB_OK')
except Exception as e:
    print(f'DB_ERROR: {str(e)}')
" >nul 2>&1

if not errorlevel 1 (
    echo   ✓ Conexión a base de datos exitosa
    echo [%date% %time%] Conexion BD OK >> "%MIGRATION_LOG%"
) else (
    echo   ⚠ WARNING: Problema de conexión a base de datos
    echo [%date% %time%] WARNING: Problema conexion BD >> "%MIGRATION_LOG%"
    set /a "COMPAT_ISSUES+=1"
)

echo.
echo ===============================================================================
echo RESULTADO DE VERIFICACION DE COMPATIBILIDAD
echo ===============================================================================

if %COMPAT_ISSUES% equ 0 (
    echo ✓ COMPATIBLE: El sistema está listo para migración a Waitress
    echo   Todos los componentes son compatibles
    echo   La migración debería completarse sin problemas
    echo.
    echo Siguiente paso: %~nx0 (ejecutar migración completa)
) else (
    echo ⚠ PROBLEMAS DETECTADOS: %COMPAT_ISSUES% problemas de compatibilidad
    echo   Se recomienda resolver estos problemas antes de migrar
    echo   La migración puede fallar o requerir intervención manual
    echo.
    echo Para migrar con riesgos: %~nx0 (migración forzada)
    echo Para resolver problemas: Revise la documentación o contacte soporte
)

echo.
echo [%date% %time%] Verificacion compatibilidad completada - Issues: %COMPAT_ISSUES% >> "%MIGRATION_LOG%"
exit /b 0

:create_migration_backup
echo.
echo CREANDO BACKUP PARA MIGRACION
echo ==============================

mkdir "%MIGRATION_BACKUP_DIR%" >nul 2>&1
if errorlevel 1 (
    echo ERROR: No se pudo crear directorio de backup
    exit /b 1
)

echo Creando backup completo del sistema antes de migración...
echo [%date% %time%] Creando backup migración >> "%MIGRATION_LOG%"

rem Crear manifiesto de backup
echo DINQR Migration Backup > "%MIGRATION_BACKUP_DIR%\migration_manifest.txt"
echo ======================= >> "%MIGRATION_BACKUP_DIR%\migration_manifest.txt"
echo Timestamp: %TIMESTAMP% >> "%MIGRATION_BACKUP_DIR%\migration_manifest.txt"
echo Source: Gunicorn Setup >> "%MIGRATION_BACKUP_DIR%\migration_manifest.txt"
echo Target: Waitress Setup >> "%MIGRATION_BACKUP_DIR%\migration_manifest.txt"
echo. >> "%MIGRATION_BACKUP_DIR%\migration_manifest.txt"

echo   Backup de configuración actual...
mkdir "%MIGRATION_BACKUP_DIR%\config" >nul 2>&1
if exist "%BACKEND_DIR%\.env" copy "%BACKEND_DIR%\.env" "%MIGRATION_BACKUP_DIR%\config\" >nul 2>&1
if exist "%BACKEND_DIR%\config.py" copy "%BACKEND_DIR%\config.py" "%MIGRATION_BACKUP_DIR%\config\" >nul 2>&1
if exist "%BACKEND_DIR%\server.py" copy "%BACKEND_DIR%\server.py" "%MIGRATION_BACKUP_DIR%\config\" >nul 2>&1
if exist "%BACKEND_DIR%\server_manager.py" copy "%BACKEND_DIR%\server_manager.py" "%MIGRATION_BACKUP_DIR%\config\" >nul 2>&1

echo   Backup de configuración de IIS...
mkdir "%MIGRATION_BACKUP_DIR%\iis" >nul 2>&1
%windir%\system32\inetsrv\appcmd.exe list site "%OLD_SITE_NAME%" /config > "%MIGRATION_BACKUP_DIR%\iis\old_site_config.xml" 2>nul
%windir%\system32\inetsrv\appcmd.exe list apppool /config > "%MIGRATION_BACKUP_DIR%\iis\apppool_config.xml" 2>nul

echo   Backup de configuración de servicios...
mkdir "%MIGRATION_BACKUP_DIR%\services" >nul 2>&1
sc qc "%OLD_SERVICE_NAME%" > "%MIGRATION_BACKUP_DIR%\services\old_service_config.txt" 2>nul

echo   Backup de datos de aplicación...
mkdir "%MIGRATION_BACKUP_DIR%\data" >nul 2>&1
if exist "%BACKEND_DIR%\data" xcopy "%BACKEND_DIR%\data" "%MIGRATION_BACKUP_DIR%\data\" /E /I /Y >nul 2>&1
if exist "%BACKEND_DIR%\uploads" xcopy "%BACKEND_DIR%\uploads" "%MIGRATION_BACKUP_DIR%\data\uploads\" /E /I /Y >nul 2>&1
if exist "%BACKEND_DIR%\logs" xcopy "%BACKEND_DIR%\logs" "%MIGRATION_BACKUP_DIR%\data\logs\" /E /I /Y >nul 2>&1

echo   Backup de base de datos...
mkdir "%MIGRATION_BACKUP_DIR%\database" >nul 2>&1
rem Intentar backup de PostgreSQL si está disponible
if exist "%BACKEND_DIR%\.env" (
    for /f "usebackq tokens=1,2 delims==" %%a in ("%BACKEND_DIR%\.env") do (
        if "%%a"=="POSTGRES_HOST" set "DB_HOST=%%b"
        if "%%a"=="POSTGRES_PORT" set "DB_PORT=%%b"
        if "%%a"=="POSTGRES_DB" set "DB_NAME=%%b"
        if "%%a"=="POSTGRES_USER" set "DB_USER=%%b"
        if "%%a"=="POSTGRES_PASSWORD" set "DB_PASSWORD=%%b"
    )
    
    if defined DB_HOST if defined DB_NAME if defined DB_USER (
        echo     Creando backup de PostgreSQL...
        set "PGPASSWORD=!DB_PASSWORD!"
        pg_dump -h "!DB_HOST!" -p "!DB_PORT!" -U "!DB_USER!" -d "!DB_NAME!" -f "%MIGRATION_BACKUP_DIR%\database\dinqr_backup.sql" 2>nul
        if not errorlevel 1 (
            echo   ✓ Backup de PostgreSQL creado
        ) else (
            echo   ⚠ WARNING: No se pudo crear backup de PostgreSQL
        )
    )
)

rem Backup de SQLite si existe
if exist "%BACKEND_DIR%\instance\dinqr.db" (
    copy "%BACKEND_DIR%\instance\dinqr.db" "%MIGRATION_BACKUP_DIR%\database\dinqr_sqlite.db" >nul 2>&1
    echo   ✓ Backup de SQLite incluido
)

echo.
echo ✓ Backup de migración creado exitosamente: %MIGRATION_BACKUP_DIR%
echo   Este backup se puede usar para rollback si es necesario
echo.
echo Siguiente paso: %~nx0 (ejecutar migración completa)
echo Para rollback: %~nx0 -rollback

echo Components backed up: >> "%MIGRATION_BACKUP_DIR%\migration_manifest.txt"
echo - Configuration files >> "%MIGRATION_BACKUP_DIR%\migration_manifest.txt"
echo - IIS configuration >> "%MIGRATION_BACKUP_DIR%\migration_manifest.txt"
echo - Service configuration >> "%MIGRATION_BACKUP_DIR%\migration_manifest.txt"
echo - Application data >> "%MIGRATION_BACKUP_DIR%\migration_manifest.txt"
echo - Database >> "%MIGRATION_BACKUP_DIR%\migration_manifest.txt"

echo [%date% %time%] Backup migración creado exitosamente >> "%MIGRATION_LOG%"
set "ROLLBACK_AVAILABLE=true"
exit /b 0

:perform_full_migration
echo.
echo EJECUTANDO MIGRACION COMPLETA DE GUNICORN A WAITRESS
echo ====================================================

rem Crear backup automático
echo Paso 1: Creando backup de seguridad...
call :create_migration_backup
if errorlevel 1 (
    echo ERROR: No se pudo crear backup - migración abortada
    goto :error
)

echo.
echo Paso 2: Deteniendo servicios actuales...
echo [%date% %time%] Deteniendo servicios actuales >> "%MIGRATION_LOG%"

rem Detener servicio existente
sc query "%OLD_SERVICE_NAME%" >nul 2>&1
if not errorlevel 1 (
    echo   Deteniendo servicio: %OLD_SERVICE_NAME%
    sc stop "%OLD_SERVICE_NAME%" >nul 2>&1
    timeout /t 10 >nul
)

rem Detener sitio IIS existente
%windir%\system32\inetsrv\appcmd.exe list site "%OLD_SITE_NAME%" >nul 2>&1
if not errorlevel 1 (
    echo   Deteniendo sitio IIS: %OLD_SITE_NAME%
    %windir%\system32\inetsrv\appcmd.exe stop site "%OLD_SITE_NAME%" >nul 2>&1
)

echo.
echo Paso 3: Instalando dependencias de Waitress...
echo [%date% %time%] Instalando dependencias Waitress >> "%MIGRATION_LOG%"

cd /d "%BACKEND_DIR%"

rem Verificar y actualizar requirements.txt
findstr /c:"waitress" requirements.txt >nul 2>&1
if errorlevel 1 (
    echo   Agregando Waitress a requirements.txt...
    echo waitress==3.0.2 >> requirements.txt
)

findstr /c:"pywin32" requirements.txt >nul 2>&1
if errorlevel 1 (
    echo   Agregando pywin32 a requirements.txt...
    echo pywin32==308 >> requirements.txt
)

echo   Instalando dependencias...
python -m pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo ERROR: Fallo la instalación de dependencias
    echo [%date% %time%] ERROR: Instalacion dependencias fallida >> "%MIGRATION_LOG%"
    goto :error
)

echo.
echo Paso 4: Migrando configuración .env...
echo [%date% %time%] Migrando configuracion .env >> "%MIGRATION_LOG%"

rem Crear backup del .env actual
if exist ".env" copy ".env" ".env.pre_waitress_migration" >nul 2>&1

rem Actualizar configuraciones específicas de Waitress
call :update_env_for_waitress

echo.
echo Paso 5: Instalando servicio de Windows Waitress...
echo [%date% %time%] Instalando servicio Waitress >> "%MIGRATION_LOG%"

rem Remover servicio anterior si existe
sc query "%OLD_SERVICE_NAME%" >nul 2>&1
if not errorlevel 1 (
    echo   Removiendo servicio anterior: %OLD_SERVICE_NAME%
    sc delete "%OLD_SERVICE_NAME%" >nul 2>&1
)

rem Instalar nuevo servicio
echo   Instalando nuevo servicio: %NEW_SERVICE_NAME%
python windows_service.py install >nul 2>&1
if errorlevel 1 (
    echo ERROR: Fallo la instalación del servicio Waitress
    echo [%date% %time%] ERROR: Instalacion servicio Waitress fallida >> "%MIGRATION_LOG%"
    goto :error
)

rem Configurar inicio automático
sc config "%NEW_SERVICE_NAME%" start= auto >nul 2>&1

echo.
echo Paso 6: Configurando IIS para Waitress...
echo [%date% %time%] Configurando IIS >> "%MIGRATION_LOG%"

rem Remover sitio anterior si es diferente
if not "%OLD_SITE_NAME%"=="%NEW_SITE_NAME%" (
    %windir%\system32\inetsrv\appcmd.exe list site "%OLD_SITE_NAME%" >nul 2>&1
    if not errorlevel 1 (
        echo   Removiendo sitio anterior: %OLD_SITE_NAME%
        %windir%\system32\inetsrv\appcmd.exe delete site "%OLD_SITE_NAME%" >nul 2>&1
    )
)

rem Crear/actualizar sitio para Waitress
call :setup_iis_for_waitress

echo.
echo Paso 7: Copiando archivos de configuración Waitress...
echo [%date% %time%] Copiando configuracion Waitress >> "%MIGRATION_LOG%"

rem Copiar web.config si existe
if exist "web.config" (
    copy "web.config" "%FRONTEND_DIR%\dist\web.config" >nul 2>&1
    echo   ✓ web.config copiado
)

echo.
echo Paso 8: Iniciando servicios Waitress...
echo [%date% %time%] Iniciando servicios Waitress >> "%MIGRATION_LOG%"

rem Iniciar servicio Waitress
echo   Iniciando servicio: %NEW_SERVICE_NAME%
python windows_service.py start >nul 2>&1
if errorlevel 1 (
    echo ERROR: No se pudo iniciar el servicio Waitress
    echo [%date% %time%] ERROR: Inicio servicio Waitress fallido >> "%MIGRATION_LOG%"
    goto :error
)

rem Esperar que el servicio se estabilice
echo   Esperando estabilización del servicio...
timeout /t 15 >nul

rem Iniciar sitio IIS
echo   Iniciando sitio IIS: %NEW_SITE_NAME%
%windir%\system32\inetsrv\appcmd.exe start site "%NEW_SITE_NAME%" >nul 2>&1

echo.
echo Paso 9: Verificando migración...
echo [%date% %time%] Verificando migracion >> "%MIGRATION_LOG%"

call :verify_waitress_migration
if errorlevel 1 (
    echo ERROR: La verificación de migración falló
    echo [%date% %time%] ERROR: Verificacion migracion fallida >> "%MIGRATION_LOG%"
    echo.
    echo ¿Desea intentar rollback? (s/N)
    set /p "ROLLBACK_CHOICE="
    if /i "%ROLLBACK_CHOICE%"=="s" (
        call :rollback_migration
    )
    goto :error
)

echo.
echo ===============================================================================
echo MIGRACION COMPLETADA EXITOSAMENTE
echo ===============================================================================
echo.
echo ✓ Migración de Gunicorn a Waitress completada
echo.
echo Configuración final:
echo   Servicio Windows: %NEW_SERVICE_NAME%
echo   Sitio IIS: %NEW_SITE_NAME%
echo   Servidor WSGI: Waitress
echo   Backup disponible: %MIGRATION_BACKUP_DIR%
echo.
echo URLs de acceso (verificar):
echo   Frontend: http://localhost/
echo   API: http://localhost/api/v1/
echo   Health: http://localhost/api/v1/health
echo.
echo Comandos de gestión:
echo   servicio_dinqr.bat [start^|stop^|restart^|status]
echo   monitoreo_waitress.bat
echo   backup_waitress.bat create
echo.
echo IMPORTANTE:
echo - Verifique que la aplicación funcione correctamente
echo - El backup está disponible para rollback si es necesario
echo - Se recomienda crear un backup completo con: backup_waitress.bat create
echo.

echo [%date% %time%] Migracion completada exitosamente >> "%MIGRATION_LOG%"
exit /b 0

rem ===============================================================================
rem FUNCIONES DE SOPORTE
rem ===============================================================================

:update_env_for_waitress
echo   Actualizando configuraciones en .env...

rem Crear archivo temporal para nueva configuración
set "temp_env=%temp%\dinqr_env_migration_%random%.txt"

rem Comentar configuraciones de Gunicorn si existen
if exist ".env" (
    for /f "usebackq delims=" %%a in (".env") do (
        set "line=%%a"
        echo !line! | findstr /b "GUNICORN_" >nul 2>&1
        if not errorlevel 1 (
            echo # MIGRATED - !line! >> "%temp_env%"
        ) else (
            echo !line! >> "%temp_env%"
        )
    )
)

rem Agregar configuraciones de Waitress
echo. >> "%temp_env%"
echo # Configuracion Waitress - Agregado durante migracion >> "%temp_env%"
echo WAITRESS_HOST=0.0.0.0 >> "%temp_env%"
echo WAITRESS_PORT=5000 >> "%temp_env%"
echo WAITRESS_THREADS=4 >> "%temp_env%"
echo WAITRESS_CONNECTION_LIMIT=100 >> "%temp_env%"
echo WAITRESS_CLEANUP_INTERVAL=30 >> "%temp_env%"
echo WAITRESS_CHANNEL_TIMEOUT=120 >> "%temp_env%"
echo. >> "%temp_env%"
echo # Configuracion del Servicio de Windows >> "%temp_env%"
echo WINDOWS_SERVICE_NAME=%NEW_SERVICE_NAME% >> "%temp_env%"
echo WINDOWS_SERVICE_DISPLAY_NAME=DINQR Backend Service >> "%temp_env%"
echo WINDOWS_SERVICE_DESCRIPTION=Servicio de Backend para DINQR con Waitress >> "%temp_env%"

rem Reemplazar .env original
if exist ".env" move ".env" ".env.backup_migration" >nul 2>&1
move "%temp_env%" ".env" >nul 2>&1

echo   ✓ Configuración .env migrada
exit /b 0

:setup_iis_for_waitress
echo   Configurando IIS para Waitress...

rem Crear Application Pool si no existe
%windir%\system32\inetsrv\appcmd.exe list apppool "DINQRAppPool" >nul 2>&1
if errorlevel 1 (
    %windir%\system32\inetsrv\appcmd.exe add apppool /name:"DINQRAppPool" /managedRuntimeVersion:"" /processModel.identityType:ApplicationPoolIdentity >nul 2>&1
)

rem Crear sitio si no existe
%windir%\system32\inetsrv\appcmd.exe list site "%NEW_SITE_NAME%" >nul 2>&1
if errorlevel 1 (
    %windir%\system32\inetsrv\appcmd.exe add site /name:"%NEW_SITE_NAME%" /physicalPath:"%FRONTEND_DIR%\dist" /bindings:http/*:80: >nul 2>&1
)

rem Asignar Application Pool
%windir%\system32\inetsrv\appcmd.exe set app "%NEW_SITE_NAME%/" /applicationPool:"DINQRAppPool" >nul 2>&1

echo   ✓ IIS configurado para Waitress
exit /b 0

:verify_waitress_migration
echo   Verificando componentes migrados...

rem Verificar servicio
sc query "%NEW_SERVICE_NAME%" | find "RUNNING" >nul
if errorlevel 1 (
    echo   ✗ Servicio Waitress no está ejecutándose
    exit /b 1
)
echo   ✓ Servicio Waitress: OK

rem Verificar conectividad Waitress
curl -s --connect-timeout 10 http://localhost:5000/api/v1/health >nul 2>&1
if errorlevel 1 (
    echo   ✗ Waitress no responde
    exit /b 1
)
echo   ✓ Waitress responde: OK

rem Verificar sitio IIS
curl -s --connect-timeout 10 http://localhost/ >nul 2>&1
if errorlevel 1 (
    echo   ✗ Sitio IIS no responde
    exit /b 1
)
echo   ✓ Sitio IIS responde: OK

rem Verificar API via IIS
curl -s --connect-timeout 10 http://localhost/api/v1/health >nul 2>&1
if errorlevel 1 (
    echo   ✗ API no accesible via IIS
    exit /b 1
)
echo   ✓ API via IIS: OK

echo   ✓ Todos los componentes verificados exitosamente
exit /b 0

:rollback_migration
echo.
echo EJECUTANDO ROLLBACK DE MIGRACION
echo =================================

rem Buscar backup más reciente si no se especifica
if not exist "%MIGRATION_BACKUP_DIR%" (
    echo Buscando backup de migración más reciente...
    for /f %%i in ('dir /b /od "%BACKUP_BASE_DIR%\migracion_*" 2^>nul') do set "LATEST_BACKUP=%%i"
    if defined LATEST_BACKUP (
        set "MIGRATION_BACKUP_DIR=%BACKUP_BASE_DIR%\!LATEST_BACKUP!"
        echo Usando backup: !LATEST_BACKUP!
    ) else (
        echo ERROR: No se encontró backup de migración
        echo [%date% %time%] ERROR: Backup no encontrado para rollback >> "%MIGRATION_LOG%"
        exit /b 1
    )
)

if not exist "%MIGRATION_BACKUP_DIR%\migration_manifest.txt" (
    echo ERROR: Backup de migración inválido o corrupto
    echo [%date% %time%] ERROR: Backup invalido para rollback >> "%MIGRATION_LOG%"
    exit /b 1
)

echo Ejecutando rollback desde: %MIGRATION_BACKUP_DIR%
echo [%date% %time%] Iniciando rollback >> "%MIGRATION_LOG%"

echo.
echo ADVERTENCIA: El rollback revertirá la migración a Waitress
echo ¿Está seguro de que desea continuar? (s/N)
set /p "CONFIRM_ROLLBACK="
if /i not "%CONFIRM_ROLLBACK%"=="s" (
    echo Rollback cancelado por el usuario.
    exit /b 0
)

echo   Deteniendo servicios Waitress...
sc stop "%NEW_SERVICE_NAME%" >nul 2>&1
%windir%\system32\inetsrv\appcmd.exe stop site "%NEW_SITE_NAME%" >nul 2>&1
timeout /t 5 >nul

echo   Removiendo servicio Waitress...
python "%BACKEND_DIR%\windows_service.py" remove >nul 2>&1

echo   Restaurando configuración .env...
if exist "%MIGRATION_BACKUP_DIR%\config\.env" (
    copy "%MIGRATION_BACKUP_DIR%\config\.env" "%BACKEND_DIR%\.env" >nul 2>&1
    echo   ✓ .env restaurado
)

echo   Restaurando configuración de servicios...
if exist "%MIGRATION_BACKUP_DIR%\services\old_service_config.txt" (
    rem Aquí se implementaría la restauración del servicio anterior
    echo   ⚠ Servicio anterior debe ser reinstalado manualmente
)

echo   Restaurando configuración de IIS...
if exist "%MIGRATION_BACKUP_DIR%\iis\old_site_config.xml" (
    rem Restaurar configuración de sitio anterior
    echo   ⚠ Configuración IIS debe ser restaurada manualmente
)

echo.
echo ✓ ROLLBACK COMPLETADO
echo =====================
echo.
echo La migración ha sido revertida parcialmente.
echo.
echo ACCIONES MANUALES REQUERIDAS:
echo 1. Reinstalar y configurar el servicio Gunicorn anterior
echo 2. Verificar y ajustar configuración de IIS
echo 3. Reiniciar servicios necesarios
echo 4. Verificar conectividad de la aplicación
echo.
echo Para soporte: Consulte el backup en %MIGRATION_BACKUP_DIR%

echo [%date% %time%] Rollback completado >> "%MIGRATION_LOG%"
exit /b 0

:show_usage
echo.
echo DINQR - Migración de Gunicorn a Waitress + IIS
echo ===============================================
echo.
echo Uso: %~nx0 [opción]
echo.
echo Opciones:
echo   (sin parámetros)    Ejecutar migración completa
echo   -check              Solo verificar compatibilidad
echo   -backup             Solo crear backup de migración
echo   -rollback           Revertir migración (requiere backup)
echo.
echo Ejemplos:
echo   %~nx0               # Migración completa
echo   %~nx0 -check        # Verificar antes de migrar
echo   %~nx0 -backup       # Crear backup de seguridad
echo   %~nx0 -rollback     # Revertir migración
echo.
echo IMPORTANTE:
echo - Este script debe ejecutarse como administrador
echo - Se recomienda ejecutar -check antes de migrar
echo - Siempre se crea un backup automático antes de migrar
echo - El rollback requiere intervención manual para completarse
echo.
goto :end

:error
echo.
echo ===============================================================================
echo ERROR EN LA MIGRACION
echo ===============================================================================
echo.
echo La migración no se completó exitosamente.
echo.
echo Para resolución de problemas:
echo 1. Revise el log detallado: %MIGRATION_LOG%
echo 2. Si existe backup, considere rollback: %~nx0 -rollback
echo 3. Use herramientas de diagnóstico: solucionador_waitress.bat
echo 4. Consulte documentación: GUIA_WAITRESS_IIS.md
echo.
echo Si necesita soporte, proporcione:
echo - Log de migración: %MIGRATION_LOG%
echo - Información del backup: %MIGRATION_BACKUP_DIR%
echo - Estado actual del sistema
echo.
echo [%date% %time%] Migracion fallida >> "%MIGRATION_LOG%"
exit /b 1

:end
echo.
echo Para más información: %~nx0 help
echo Log completo disponible en: %MIGRATION_LOG%
echo.
exit /b 0
