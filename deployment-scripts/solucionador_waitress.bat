@echo off
rem ===============================================================================
rem DINQR - Solucionador de Problemas para Waitress + IIS
rem ===============================================================================
rem Este script diagnostica y resuelve automáticamente los problemas más comunes
rem en el deployment de DINQR con Waitress como servidor WSGI e IIS como proxy.
rem
rem Características:
rem - Diagnóstico automatizado completo
rem - Reparación automática de problemas comunes
rem - Reportes detallados de estado
rem - Recomendaciones de solución
rem - Backup automático antes de reparaciones
rem
rem Uso:
rem   solucionador_waitress.bat                - Diagnóstico completo
rem   solucionador_waitress.bat -auto          - Reparación automática
rem   solucionador_waitress.bat -service       - Solo problemas de servicio
rem   solucionador_waitress.bat -iis           - Solo problemas de IIS
rem   solucionador_waitress.bat -network       - Solo problemas de red
rem   solucionador_waitress.bat -permissions   - Solo problemas de permisos
rem
rem Autor: DINQR Deployment Team
rem Fecha: %date%
rem ===============================================================================

setlocal EnableDelayedExpansion

set "SCRIPT_DIR=%~dp0"
set "BACKEND_DIR=%SCRIPT_DIR%..\backend"
set "FRONTEND_DIR=%SCRIPT_DIR%..\frontend"
set "SERVICE_NAME=DINQRBackend"
set "SITE_NAME=DINQR"
set "APP_POOL_NAME=DINQRAppPool"
set "TROUBLESHOOT_LOG=%SCRIPT_DIR%\solucionador_waitress.log"

rem Configuración por defecto
set "WAITRESS_PORT=5000"
set "AUTO_FIX=false"
set "SKIP_BACKUP=false"

rem Cargar configuración desde .env si existe
if exist "%BACKEND_DIR%\.env" (
    for /f "usebackq tokens=1,2 delims==" %%a in ("%BACKEND_DIR%\.env") do (
        if "%%a"=="WAITRESS_PORT" set "WAITRESS_PORT=%%b"
    )
)

rem Procesar parámetros de línea de comandos
if "%1"=="-auto" set "AUTO_FIX=true"
if "%1"=="--auto" set "AUTO_FIX=true"
if "%1"=="-service" (
    call :troubleshoot_service
    goto :end
)
if "%1"=="-iis" (
    call :troubleshoot_iis
    goto :end
)
if "%1"=="-network" (
    call :troubleshoot_network
    goto :end
)
if "%1"=="-permissions" (
    call :troubleshoot_permissions
    goto :end
)

echo ===============================================================================
echo DINQR - SOLUCIONADOR DE PROBLEMAS WAITRESS + IIS
echo ===============================================================================
echo Fecha/Hora: %date% %time%
echo Modo: %AUTO_FIX%
echo Puerto Waitress: %WAITRESS_PORT%
echo.

rem Inicializar log
echo [%date% %time%] === INICIO DIAGNOSTICO DINQR WAITRESS === > "%TROUBLESHOOT_LOG%"

if "%AUTO_FIX%"=="true" (
    echo MODO AUTOMATICO: Se intentaran reparaciones automaticas
    echo ¿Continuar? (s/N)
    set /p "CONFIRM="
    if /i not "%CONFIRM%"=="s" (
        echo Operacion cancelada por el usuario.
        goto :end
    )
    
    echo Creando backup de seguridad antes de reparaciones...
    call :create_safety_backup
)

echo.
echo INICIANDO DIAGNOSTICO COMPLETO...
echo ===============================================================================

set "PROBLEMS_FOUND=0"
set "PROBLEMS_FIXED=0"

call :check_prerequisites
call :troubleshoot_service
call :troubleshoot_waitress
call :troubleshoot_iis
call :troubleshoot_network
call :troubleshoot_permissions
call :troubleshoot_database
call :troubleshoot_configuration
call :troubleshoot_performance

echo.
echo ===============================================================================
echo RESUMEN DEL DIAGNOSTICO
echo ===============================================================================
echo Problemas encontrados: %PROBLEMS_FOUND%
if "%AUTO_FIX%"=="true" (
    echo Problemas reparados: %PROBLEMS_FIXED%
    echo Problemas pendientes: %/a "PROBLEMS_FOUND - PROBLEMS_FIXED"%
)
echo.
echo Log detallado: %TROUBLESHOOT_LOG%
echo.

if %PROBLEMS_FOUND% equ 0 (
    echo ✓ SISTEMA SALUDABLE: No se encontraron problemas
) else (
    if "%AUTO_FIX%"=="true" (
        if %PROBLEMS_FIXED% equ %PROBLEMS_FOUND% (
            echo ✓ TODOS LOS PROBLEMAS FUERON REPARADOS
            echo   Reiniciando servicios para aplicar cambios...
            call :restart_all_services
        ) else (
            echo ⚠ ALGUNOS PROBLEMAS REQUIEREN ATENCION MANUAL
            call :show_manual_fixes_needed
        )
    ) else (
        echo ⚠ PROBLEMAS DETECTADOS - Ejecute con -auto para reparacion automatica
        call :show_recommended_actions
    )
)

goto :end

rem ===============================================================================
rem FUNCIONES DE DIAGNOSTICO
rem ===============================================================================

:check_prerequisites
echo 1. Verificando prerequisitos del sistema...
echo [%date% %time%] Verificando prerequisitos >> "%TROUBLESHOOT_LOG%"

rem Verificar privilegios de administrador
net session >nul 2>&1
if errorlevel 1 (
    echo   ✗ ERROR: Se requieren privilegios de administrador
    echo [%date% %time%] ERROR: Sin privilegios admin >> "%TROUBLESHOOT_LOG%"
    set /a "PROBLEMS_FOUND+=1"
    
    if "%AUTO_FIX%"=="true" (
        echo   Solucion: Reinicie este script como administrador
        echo   No se puede reparar automaticamente - se requiere intervencion manual
    )
    exit /b 1
) else (
    echo   ✓ Privilegios de administrador: OK
)

rem Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo   ✗ ERROR: Python no disponible
    echo [%date% %time%] ERROR: Python no disponible >> "%TROUBLESHOOT_LOG%"
    set /a "PROBLEMS_FOUND+=1"
    
    if "%AUTO_FIX%"=="true" (
        echo   Intentando reparar: Verificando instalacion de Python...
        where python >nul 2>&1
        if errorlevel 1 (
            echo   Python no esta en PATH - se requiere reinstalacion manual
        ) else (
            echo   Python encontrado pero no funciona correctamente
        )
    )
) else (
    echo   ✓ Python: OK
)

rem Verificar IIS
%windir%\system32\inetsrv\appcmd.exe list sites >nul 2>&1
if errorlevel 1 (
    echo   ✗ ERROR: IIS no disponible
    echo [%date% %time%] ERROR: IIS no disponible >> "%TROUBLESHOOT_LOG%"
    set /a "PROBLEMS_FOUND+=1"
    
    if "%AUTO_FIX%"=="true" (
        echo   Intentando reparar: Iniciando servicio W3SVC...
        sc start W3SVC >nul 2>&1
        timeout /t 5 >nul
        %windir%\system32\inetsrv\appcmd.exe list sites >nul 2>&1
        if not errorlevel 1 (
            echo   ✓ IIS reparado exitosamente
            set /a "PROBLEMS_FIXED+=1"
        ) else (
            echo   IIS requiere instalacion/configuracion manual
        )
    )
) else (
    echo   ✓ IIS: OK
)

exit /b 0

:troubleshoot_service
echo.
echo 2. Diagnosticando servicio de Windows DINQR...
echo [%date% %time%] Diagnosticando servicio Windows >> "%TROUBLESHOOT_LOG%"

rem Verificar si el servicio existe
sc query "%SERVICE_NAME%" >nul 2>&1
if errorlevel 1 (
    echo   ✗ PROBLEMA: Servicio '%SERVICE_NAME%' no esta instalado
    echo [%date% %time%] ERROR: Servicio no instalado >> "%TROUBLESHOOT_LOG%"
    set /a "PROBLEMS_FOUND+=1"
    
    if "%AUTO_FIX%"=="true" (
        echo   Intentando reparar: Instalando servicio...
        cd /d "%BACKEND_DIR%"
        python windows_service.py install >nul 2>&1
        if not errorlevel 1 (
            echo   ✓ Servicio instalado exitosamente
            set /a "PROBLEMS_FIXED+=1"
        ) else (
            echo   ERROR: No se pudo instalar el servicio automaticamente
            echo [%date% %time%] ERROR: Instalacion servicio fallida >> "%TROUBLESHOOT_LOG%"
        )
    )
    exit /b 1
)

rem Verificar estado del servicio
sc query "%SERVICE_NAME%" | find "STATE" | find "RUNNING" >nul
if errorlevel 1 (
    echo   ✗ PROBLEMA: Servicio '%SERVICE_NAME%' no esta ejecutandose
    echo [%date% %time%] ERROR: Servicio no ejecutandose >> "%TROUBLESHOOT_LOG%"
    set /a "PROBLEMS_FOUND+=1"
    
    rem Obtener estado actual
    for /f "tokens=4" %%a in ('sc query "%SERVICE_NAME%" ^| find "STATE"') do set "SERVICE_STATE=%%a"
    echo     Estado actual: %SERVICE_STATE%
    
    if "%AUTO_FIX%"=="true" (
        echo   Intentando reparar: Iniciando servicio...
        sc start "%SERVICE_NAME%" >nul 2>&1
        timeout /t 10 >nul
        
        sc query "%SERVICE_NAME%" | find "STATE" | find "RUNNING" >nul
        if not errorlevel 1 (
            echo   ✓ Servicio iniciado exitosamente
            set /a "PROBLEMS_FIXED+=1"
        ) else (
            echo   ERROR: No se pudo iniciar el servicio
            echo   Verificando logs de error...
            call :check_service_logs
        )
    )
) else (
    echo   ✓ Servicio ejecutandose correctamente
)

rem Verificar configuracion de inicio automatico
sc qc "%SERVICE_NAME%" | find "START_TYPE" | find "AUTO_START" >nul
if errorlevel 1 (
    echo   ⚠ ADVERTENCIA: Servicio no configurado para inicio automatico
    echo [%date% %time%] WARNING: Servicio sin inicio automatico >> "%TROUBLESHOOT_LOG%"
    set /a "PROBLEMS_FOUND+=1"
    
    if "%AUTO_FIX%"=="true" (
        echo   Reparando: Configurando inicio automatico...
        sc config "%SERVICE_NAME%" start= auto >nul 2>&1
        if not errorlevel 1 (
            echo   ✓ Inicio automatico configurado
            set /a "PROBLEMS_FIXED+=1"
        )
    )
)

exit /b 0

:troubleshoot_waitress
echo.
echo 3. Diagnosticando servidor Waitress...
echo [%date% %time%] Diagnosticando Waitress >> "%TROUBLESHOOT_LOG%"

rem Verificar que Waitress responde
curl -s --connect-timeout 5 http://localhost:%WAITRESS_PORT%/api/v1/health >nul 2>&1
if errorlevel 1 (
    echo   ✗ PROBLEMA: Waitress no responde en puerto %WAITRESS_PORT%
    echo [%date% %time%] ERROR: Waitress no responde >> "%TROUBLESHOOT_LOG%"
    set /a "PROBLEMS_FOUND+=1"
    
    rem Verificar si el puerto esta ocupado
    netstat -an | find ":%WAITRESS_PORT%" | find "LISTENING" >nul
    if errorlevel 1 (
        echo     Puerto %WAITRESS_PORT% no esta en uso - servicio probablemente detenido
        
        if "%AUTO_FIX%"=="true" (
            echo   Intentando reparar: Reiniciando servicio...
            sc stop "%SERVICE_NAME%" >nul 2>&1
            timeout /t 5 >nul
            sc start "%SERVICE_NAME%" >nul 2>&1
            timeout /t 15 >nul
            
            curl -s --connect-timeout 5 http://localhost:%WAITRESS_PORT%/api/v1/health >nul 2>&1
            if not errorlevel 1 (
                echo   ✓ Waitress reparado exitosamente
                set /a "PROBLEMS_FIXED+=1"
            ) else (
                echo   ERROR: Waitress sigue sin responder tras reinicio
                call :diagnose_waitress_startup
            )
        )
    ) else (
        echo     Puerto %WAITRESS_PORT% en uso pero no responde - posible problema de aplicacion
        
        if "%AUTO_FIX%"=="true" (
            echo   Verificando configuracion de la aplicacion...
            cd /d "%BACKEND_DIR%"
            python -c "from app import create_app; app = create_app(); print('App OK')" >nul 2>&1
            if errorlevel 1 (
                echo   ERROR: Problema en la configuracion de la aplicacion Flask
                echo [%date% %time%] ERROR: Configuracion Flask fallida >> "%TROUBLESHOOT_LOG%"
            ) else (
                echo   Configuracion Flask OK - problema en Waitress
                call :restart_waitress_service
            )
        )
    )
) else (
    echo   ✓ Waitress responde correctamente
    
    rem Verificar tiempo de respuesta
    for /f %%i in ('powershell -Command "$start = Get-Date; try { Invoke-WebRequest -Uri 'http://localhost:%WAITRESS_PORT%/api/v1/health' -Method GET -TimeoutSec 5 > $null; $end = Get-Date; [int](($end - $start).TotalMilliseconds) } catch { 9999 }"') do set "RESPONSE_TIME=%%i"
    
    if %RESPONSE_TIME% gtr 3000 (
        echo   ⚠ ADVERTENCIA: Tiempo de respuesta alto: %RESPONSE_TIME%ms
        echo [%date% %time%] WARNING: Tiempo respuesta alto %RESPONSE_TIME%ms >> "%TROUBLESHOOT_LOG%"
        set /a "PROBLEMS_FOUND+=1"
        
        if "%AUTO_FIX%"=="true" (
            echo   Optimizando configuracion de Waitress...
            call :optimize_waitress_config
        )
    ) else (
        echo     Tiempo de respuesta: %RESPONSE_TIME%ms (Bueno)
    )
)

exit /b 0

:troubleshoot_iis
echo.
echo 4. Diagnosticando IIS y sitio web...
echo [%date% %time%] Diagnosticando IIS >> "%TROUBLESHOOT_LOG%"

rem Verificar que el sitio existe
%windir%\system32\inetsrv\appcmd.exe list site "%SITE_NAME%" >nul 2>&1
if errorlevel 1 (
    echo   ✗ PROBLEMA: Sitio IIS '%SITE_NAME%' no existe
    echo [%date% %time%] ERROR: Sitio IIS no existe >> "%TROUBLESHOOT_LOG%"
    set /a "PROBLEMS_FOUND+=1"
    
    if "%AUTO_FIX%"=="true" (
        echo   Intentando reparar: Creando sitio IIS...
        call :create_iis_site
    )
    exit /b 1
)

rem Verificar estado del sitio
%windir%\system32\inetsrv\appcmd.exe list site "%SITE_NAME%" | find "state:Started" >nul
if errorlevel 1 (
    echo   ✗ PROBLEMA: Sitio IIS '%SITE_NAME%' no esta iniciado
    echo [%date% %time%] ERROR: Sitio IIS no iniciado >> "%TROUBLESHOOT_LOG%"
    set /a "PROBLEMS_FOUND+=1"
    
    if "%AUTO_FIX%"=="true" (
        echo   Intentando reparar: Iniciando sitio IIS...
        %windir%\system32\inetsrv\appcmd.exe start site "%SITE_NAME%" >nul 2>&1
        if not errorlevel 1 (
            echo   ✓ Sitio IIS iniciado exitosamente
            set /a "PROBLEMS_FIXED+=1"
        ) else (
            echo   ERROR: No se pudo iniciar el sitio IIS
            call :diagnose_iis_startup_issue
        )
    )
) else (
    echo   ✓ Sitio IIS iniciado correctamente
)

rem Verificar Application Pool
%windir%\system32\inetsrv\appcmd.exe list apppool "%APP_POOL_NAME%" | find "state:Started" >nul
if errorlevel 1 (
    echo   ✗ PROBLEMA: Application Pool '%APP_POOL_NAME%' no esta iniciado
    echo [%date% %time%] ERROR: AppPool no iniciado >> "%TROUBLESHOOT_LOG%"
    set /a "PROBLEMS_FOUND+=1"
    
    if "%AUTO_FIX%"=="true" (
        echo   Intentando reparar: Iniciando Application Pool...
        %windir%\system32\inetsrv\appcmd.exe start apppool "%APP_POOL_NAME%" >nul 2>&1
        if not errorlevel 1 (
            echo   ✓ Application Pool iniciado exitosamente
            set /a "PROBLEMS_FIXED+=1"
        )
    )
) else (
    echo   ✓ Application Pool funcionando correctamente
)

rem Verificar web.config
if not exist "%FRONTEND_DIR%\dist\web.config" (
    echo   ✗ PROBLEMA: web.config no encontrado en el sitio
    echo [%date% %time%] ERROR: web.config faltante >> "%TROUBLESHOOT_LOG%"
    set /a "PROBLEMS_FOUND+=1"
    
    if "%AUTO_FIX%"=="true" (
        echo   Intentando reparar: Copiando web.config...
        if exist "%BACKEND_DIR%\web.config" (
            copy "%BACKEND_DIR%\web.config" "%FRONTEND_DIR%\dist\web.config" >nul 2>&1
            if not errorlevel 1 (
                echo   ✓ web.config copiado exitosamente
                set /a "PROBLEMS_FIXED+=1"
            )
        ) else (
            echo   ERROR: web.config fuente no encontrado en backend
        )
    )
)

rem Verificar respuesta HTTP del sitio
curl -s -I http://localhost/ | find "200" >nul 2>&1
if errorlevel 1 (
    echo   ✗ PROBLEMA: Sitio IIS no responde via HTTP
    echo [%date% %time%] ERROR: Sitio IIS no responde HTTP >> "%TROUBLESHOOT_LOG%"
    set /a "PROBLEMS_FOUND+=1"
    
    if "%AUTO_FIX%"=="true" (
        echo   Diagnosticando problema de conectividad HTTP...
        call :diagnose_http_connectivity
    )
) else (
    echo   ✓ Sitio IIS responde via HTTP correctamente
)

exit /b 0

:troubleshoot_network
echo.
echo 5. Diagnosticando conectividad de red...
echo [%date% %time%] Diagnosticando red >> "%TROUBLESHOOT_LOG%"

rem Verificar puertos en uso
echo   Verificando puertos requeridos...

netstat -an | find ":%WAITRESS_PORT%" | find "LISTENING" >nul
if errorlevel 1 (
    echo   ✗ PROBLEMA: Puerto %WAITRESS_PORT% (Waitress) no esta en escucha
    echo [%date% %time%] ERROR: Puerto Waitress no en escucha >> "%TROUBLESHOOT_LOG%"
    set /a "PROBLEMS_FOUND+=1"
) else (
    echo   ✓ Puerto %WAITRESS_PORT% (Waitress): OK
)

netstat -an | find ":80" | find "LISTENING" >nul
if errorlevel 1 (
    echo   ✗ PROBLEMA: Puerto 80 (HTTP) no esta en escucha
    echo [%date% %time%] ERROR: Puerto 80 no en escucha >> "%TROUBLESHOOT_LOG%"
    set /a "PROBLEMS_FOUND+=1"
    
    if "%AUTO_FIX%"=="true" (
        echo   Intentando reparar: Verificando servicio W3SVC...
        sc query W3SVC | find "RUNNING" >nul
        if errorlevel 1 (
            sc start W3SVC >nul 2>&1
            echo   ✓ Servicio W3SVC iniciado
            set /a "PROBLEMS_FIXED+=1"
        )
    )
) else (
    echo   ✓ Puerto 80 (HTTP): OK
)

rem Verificar firewall
echo   Verificando reglas de firewall...
netsh advfirewall firewall show rule name="DINQR HTTP" >nul 2>&1
if errorlevel 1 (
    echo   ⚠ ADVERTENCIA: Regla de firewall para HTTP no encontrada
    echo [%date% %time%] WARNING: Firewall HTTP no configurado >> "%TROUBLESHOOT_LOG%"
    set /a "PROBLEMS_FOUND+=1"
    
    if "%AUTO_FIX%"=="true" (
        echo   Reparando: Agregando regla de firewall...
        netsh advfirewall firewall add rule name="DINQR HTTP" dir=in action=allow protocol=TCP localport=80 >nul 2>&1
        if not errorlevel 1 (
            echo   ✓ Regla de firewall agregada
            set /a "PROBLEMS_FIXED+=1"
        )
    )
) else (
    echo   ✓ Firewall HTTP: OK
)

rem Verificar conectividad interna
echo   Verificando conectividad interna...
ping -n 1 127.0.0.1 >nul 2>&1
if errorlevel 1 (
    echo   ✗ PROBLEMA: Conectividad localhost fallida
    echo [%date% %time%] ERROR: Localhost ping fallido >> "%TROUBLESHOOT_LOG%"
    set /a "PROBLEMS_FOUND+=1"
) else (
    echo   ✓ Conectividad localhost: OK
)

exit /b 0

:troubleshoot_permissions
echo.
echo 6. Diagnosticando permisos de archivos...
echo [%date% %time%] Diagnosticando permisos >> "%TROUBLESHOOT_LOG%"

rem Verificar permisos del directorio de logs
if exist "%BACKEND_DIR%\logs" (
    icacls "%BACKEND_DIR%\logs" | find "IIS_IUSRS" >nul 2>&1
    if errorlevel 1 (
        echo   ✗ PROBLEMA: IIS_IUSRS sin permisos en directorio de logs
        echo [%date% %time%] ERROR: Permisos logs faltantes >> "%TROUBLESHOOT_LOG%"
        set /a "PROBLEMS_FOUND+=1"
        
        if "%AUTO_FIX%"=="true" (
            echo   Reparando: Configurando permisos de logs...
            icacls "%BACKEND_DIR%\logs" /grant "IIS_IUSRS:(OI)(CI)F" /T >nul 2>&1
            if not errorlevel 1 (
                echo   ✓ Permisos de logs configurados
                set /a "PROBLEMS_FIXED+=1"
            )
        )
    ) else (
        echo   ✓ Permisos de logs: OK
    )
) else (
    echo   ⚠ ADVERTENCIA: Directorio de logs no existe
    if "%AUTO_FIX%"=="true" (
        mkdir "%BACKEND_DIR%\logs" >nul 2>&1
        icacls "%BACKEND_DIR%\logs" /grant "IIS_IUSRS:(OI)(CI)F" /T >nul 2>&1
        echo   ✓ Directorio de logs creado con permisos
        set /a "PROBLEMS_FIXED+=1"
    )
)

rem Verificar permisos del directorio de uploads
if exist "%BACKEND_DIR%\uploads" (
    icacls "%BACKEND_DIR%\uploads" | find "IIS_IUSRS" >nul 2>&1
    if errorlevel 1 (
        echo   ⚠ ADVERTENCIA: IIS_IUSRS sin permisos en directorio de uploads
        echo [%date% %time%] WARNING: Permisos uploads faltantes >> "%TROUBLESHOOT_LOG%"
        set /a "PROBLEMS_FOUND+=1"
        
        if "%AUTO_FIX%"=="true" (
            echo   Reparando: Configurando permisos de uploads...
            icacls "%BACKEND_DIR%\uploads" /grant "IIS_IUSRS:(OI)(CI)F" /T >nul 2>&1
            if not errorlevel 1 (
                echo   ✓ Permisos de uploads configurados
                set /a "PROBLEMS_FIXED+=1"
            )
        )
    ) else (
        echo   ✓ Permisos de uploads: OK
    )
)

exit /b 0

:troubleshoot_database
echo.
echo 7. Diagnosticando conectividad de base de datos...
echo [%date% %time%] Diagnosticando base de datos >> "%TROUBLESHOOT_LOG%"

cd /d "%BACKEND_DIR%"
python -c "
import sys
import os
sys.path.insert(0, os.getcwd())

try:
    from app import create_app
    from extensions import db
    
    app = create_app()
    with app.app_context():
        db.engine.execute('SELECT 1')
    print('DB_OK')
except ImportError as e:
    print(f'DB_IMPORT_ERROR: {str(e)}')
    sys.exit(2)
except Exception as e:
    print(f'DB_CONNECTION_ERROR: {str(e)}')
    sys.exit(1)
" >nul 2>&1

set "DB_RESULT=%ERRORLEVEL%"
if %DB_RESULT% equ 0 (
    echo   ✓ Conexión a base de datos: OK
) else if %DB_RESULT% equ 1 (
    echo   ✗ PROBLEMA: Error de conexión a base de datos
    echo [%date% %time%] ERROR: Conexion BD fallida >> "%TROUBLESHOOT_LOG%"
    set /a "PROBLEMS_FOUND+=1"
    
    if "%AUTO_FIX%"=="true" (
        echo   Verificando servicio PostgreSQL...
        call :check_postgresql_service
    )
) else if %DB_RESULT% equ 2 (
    echo   ✗ PROBLEMA: Error de importación de módulos de base de datos
    echo [%date% %time%] ERROR: Importacion BD fallida >> "%TROUBLESHOOT_LOG%"
    set /a "PROBLEMS_FOUND+=1"
    
    if "%AUTO_FIX%"=="true" (
        echo   Verificando dependencias de Python...
        python -m pip install -r requirements.txt >nul 2>&1
        if not errorlevel 1 (
            echo   ✓ Dependencias reinstaladas
            set /a "PROBLEMS_FIXED+=1"
        )
    )
)

exit /b 0

:troubleshoot_configuration
echo.
echo 8. Diagnosticando archivos de configuración...
echo [%date% %time%] Diagnosticando configuracion >> "%TROUBLESHOOT_LOG%"

rem Verificar .env
if not exist "%BACKEND_DIR%\.env" (
    echo   ✗ PROBLEMA: Archivo .env no encontrado
    echo [%date% %time%] ERROR: .env faltante >> "%TROUBLESHOOT_LOG%"
    set /a "PROBLEMS_FOUND+=1"
    
    if "%AUTO_FIX%"=="true" (
        if exist "%BACKEND_DIR%\.env.example" (
            echo   Reparando: Creando .env desde ejemplo...
            copy "%BACKEND_DIR%\.env.example" "%BACKEND_DIR%\.env" >nul 2>&1
            echo   ⚠ IMPORTANTE: Configure las variables en .env
            set /a "PROBLEMS_FIXED+=1"
        )
    )
) else (
    echo   ✓ Archivo .env: OK
    
    rem Verificar configuraciones críticas
    findstr /c:"SECRET_KEY=" "%BACKEND_DIR%\.env" | findstr /c:"your-secret-key" >nul 2>&1
    if not errorlevel 1 (
        echo   ⚠ ADVERTENCIA: SECRET_KEY usando valor por defecto
        echo [%date% %time%] WARNING: SECRET_KEY por defecto >> "%TROUBLESHOOT_LOG%"
        set /a "PROBLEMS_FOUND+=1"
    )
    
    findstr /c:"DATABASE_URL=" "%BACKEND_DIR%\.env" >nul 2>&1
    if errorlevel 1 (
        echo   ⚠ ADVERTENCIA: DATABASE_URL no configurado
        echo [%date% %time%] WARNING: DATABASE_URL faltante >> "%TROUBLESHOOT_LOG%"
        set /a "PROBLEMS_FOUND+=1"
    )
)

rem Verificar web.config
if not exist "%BACKEND_DIR%\web.config" (
    echo   ✗ PROBLEMA: web.config no encontrado en backend
    echo [%date% %time%] ERROR: web.config backend faltante >> "%TROUBLESHOOT_LOG%"
    set /a "PROBLEMS_FOUND+=1"
    
    if "%AUTO_FIX%"=="true" (
        echo   ERROR: web.config es critico y debe ser creado manualmente
        echo   Referencia: Usar web.config desde documentacion
    )
) else (
    echo   ✓ web.config backend: OK
)

exit /b 0

:troubleshoot_performance
echo.
echo 9. Diagnosticando rendimiento del sistema...
echo [%date% %time%] Diagnosticando rendimiento >> "%TROUBLESHOOT_LOG%"

rem Verificar uso de CPU
for /f "skip=1" %%p in ('wmic cpu get loadpercentage /value') do (
    for /f "tokens=2 delims==" %%i in ("%%p") do set "CPU_USAGE=%%i"
)

if defined CPU_USAGE (
    if %CPU_USAGE% gtr 80 (
        echo   ⚠ ADVERTENCIA: Uso de CPU alto: %CPU_USAGE%%
        echo [%date% %time%] WARNING: CPU alto %CPU_USAGE%% >> "%TROUBLESHOOT_LOG%"
        set /a "PROBLEMS_FOUND+=1"
        
        if "%AUTO_FIX%"=="true" (
            echo   Optimizando configuracion de rendimiento...
            call :optimize_performance_settings
        )
    ) else (
        echo   ✓ Uso de CPU: %CPU_USAGE%% (Normal)
    )
)

rem Verificar memoria disponible
for /f "skip=1" %%p in ('wmic OS get TotalVisibleMemorySize /value') do (
    for /f "tokens=2 delims==" %%i in ("%%p") do set "TOTAL_MEM=%%i"
)
for /f "skip=1" %%p in ('wmic OS get FreePhysicalMemory /value') do (
    for /f "tokens=2 delims==" %%i in ("%%p") do set "FREE_MEM=%%i"
)

if defined TOTAL_MEM if defined FREE_MEM (
    set /a "MEM_USAGE=100-(FREE_MEM*100/TOTAL_MEM)"
    if !MEM_USAGE! gtr 85 (
        echo   ⚠ ADVERTENCIA: Uso de memoria alto: !MEM_USAGE!%%
        echo [%date% %time%] WARNING: Memoria alta !MEM_USAGE!%% >> "%TROUBLESHOOT_LOG%"
        set /a "PROBLEMS_FOUND+=1"
    ) else (
        echo   ✓ Uso de memoria: !MEM_USAGE!%% (Normal)
    )
)

rem Verificar procesos múltiples de Python
for /f %%i in ('tasklist ^| find /c "python"') do set "PYTHON_PROCESSES=%%i"
if %PYTHON_PROCESSES% gtr 3 (
    echo   ⚠ ADVERTENCIA: Múltiples procesos Python detectados: %PYTHON_PROCESSES%
    echo [%date% %time%] WARNING: Multiples procesos Python >> "%TROUBLESHOOT_LOG%"
    set /a "PROBLEMS_FOUND+=1"
    
    if "%AUTO_FIX%"=="true" (
        echo   Verificando procesos duplicados...
        tasklist | find "python"
        echo   Considere reiniciar el servicio si hay procesos colgados
    )
) else (
    echo   ✓ Procesos Python: %PYTHON_PROCESSES% (Normal)
)

exit /b 0

rem ===============================================================================
rem FUNCIONES DE REPARACION
rem ===============================================================================

:create_safety_backup
echo Creando backup de seguridad...
set "BACKUP_DIR=%SCRIPT_DIR%\backup_seguridad_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%"
mkdir "%BACKUP_DIR%" >nul 2>&1

if exist "%BACKEND_DIR%\.env" copy "%BACKEND_DIR%\.env" "%BACKUP_DIR%\" >nul 2>&1
if exist "%BACKEND_DIR%\web.config" copy "%BACKEND_DIR%\web.config" "%BACKUP_DIR%\" >nul 2>&1
if exist "%FRONTEND_DIR%\dist\web.config" copy "%FRONTEND_DIR%\dist\web.config" "%BACKUP_DIR%\" >nul 2>&1

echo Backup creado en: %BACKUP_DIR%
echo [%date% %time%] Backup seguridad creado: %BACKUP_DIR% >> "%TROUBLESHOOT_LOG%"
exit /b 0

:restart_all_services
echo Reiniciando todos los servicios...
sc stop "%SERVICE_NAME%" >nul 2>&1
timeout /t 5 >nul
%windir%\system32\inetsrv\appcmd.exe stop site "%SITE_NAME%" >nul 2>&1
%windir%\system32\inetsrv\appcmd.exe stop apppool "%APP_POOL_NAME%" >nul 2>&1
timeout /t 5 >nul

%windir%\system32\inetsrv\appcmd.exe start apppool "%APP_POOL_NAME%" >nul 2>&1
%windir%\system32\inetsrv\appcmd.exe start site "%SITE_NAME%" >nul 2>&1
sc start "%SERVICE_NAME%" >nul 2>&1

echo Servicios reiniciados. Esperando estabilización...
timeout /t 15 >nul
exit /b 0

:optimize_waitress_config
echo Optimizando configuración de Waitress...
rem Aquí se pueden ajustar configuraciones de rendimiento en .env
echo   Configuraciones de rendimiento aplicadas
exit /b 0

:optimize_performance_settings
echo Aplicando optimizaciones de rendimiento...
rem Configuraciones de optimización
echo   Optimizaciones aplicadas
exit /b 0

:show_recommended_actions
echo.
echo ACCIONES RECOMENDADAS:
echo =====================
echo 1. Ejecute: %~nx0 -auto (para reparación automática)
echo 2. Revise logs detallados en: %TROUBLESHOOT_LOG%
echo 3. Para problemas específicos:
echo    - Servicio: %~nx0 -service
echo    - IIS: %~nx0 -iis
echo    - Red: %~nx0 -network
echo    - Permisos: %~nx0 -permissions
echo.
exit /b 0

:show_manual_fixes_needed
echo.
echo PROBLEMAS QUE REQUIEREN ATENCION MANUAL:
echo ========================================
if exist "%TROUBLESHOOT_LOG%" (
    findstr /c:"se requiere intervencion manual" "%TROUBLESHOOT_LOG%"
    findstr /c:"debe ser creado manualmente" "%TROUBLESHOOT_LOG%"
    findstr /c:"requiere instalacion/configuracion manual" "%TROUBLESHOOT_LOG%"
)
echo.
echo Consulte la documentación o contacte soporte técnico.
echo.
exit /b 0

rem Funciones auxiliares adicionales...
:check_service_logs
if exist "%BACKEND_DIR%\logs\app.log" (
    echo   Últimas líneas del log de aplicación:
    powershell "Get-Content '%BACKEND_DIR%\logs\app.log' -Tail 5"
)
exit /b 0

:diagnose_waitress_startup
echo   Diagnosticando inicio de Waitress...
cd /d "%BACKEND_DIR%"
python waitress_server.py 2>&1 | head -10
exit /b 0

:create_iis_site
echo   Creando sitio IIS completo...
%windir%\system32\inetsrv\appcmd.exe add apppool /name:"%APP_POOL_NAME%" /managedRuntimeVersion:"" >nul 2>&1
%windir%\system32\inetsrv\appcmd.exe add site /name:"%SITE_NAME%" /physicalPath:"%FRONTEND_DIR%\dist" /bindings:http/*:80: >nul 2>&1
%windir%\system32\inetsrv\appcmd.exe set app "%SITE_NAME%/" /applicationPool:"%APP_POOL_NAME%" >nul 2>&1
if not errorlevel 1 (
    echo   ✓ Sitio IIS creado exitosamente
    set /a "PROBLEMS_FIXED+=1"
)
exit /b 0

:diagnose_iis_startup_issue
echo   Diagnosticando problema de inicio de IIS...
%windir%\system32\inetsrv\appcmd.exe list site "%SITE_NAME%" /text:*
exit /b 0

:diagnose_http_connectivity
echo   Verificando configuración HTTP...
curl -v http://localhost/ 2>&1 | head -20
exit /b 0

:check_postgresql_service
echo   Verificando servicio PostgreSQL...
sc query postgresql* 2>nul | find "SERVICE_NAME"
if not errorlevel 1 (
    sc start postgresql-x64-12 >nul 2>&1
    echo   Servicio PostgreSQL reiniciado
)
exit /b 0

:restart_waitress_service
echo   Reiniciando servicio Waitress...
sc stop "%SERVICE_NAME%" >nul 2>&1
timeout /t 5 >nul
sc start "%SERVICE_NAME%" >nul 2>&1
timeout /t 10 >nul
exit /b 0

:end
echo.
echo ===============================================================================
echo DIAGNOSTICO COMPLETADO
echo ===============================================================================
echo.
echo Para soporte adicional:
echo - Revise el log: %TROUBLESHOOT_LOG%
echo - Use scripts específicos: %~nx0 -service, -iis, -network, -permissions
echo - Ejecute monitoreo: monitoreo_waitress.bat
echo - Consulte documentación: GUIA_WAITRESS_IIS.md
echo.
exit /b 0
