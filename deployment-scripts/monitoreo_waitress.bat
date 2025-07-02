@echo off
rem ===============================================================================
rem DINQR - Monitor de Salud Waitress + IIS
rem ===============================================================================
rem Este script proporciona monitoreo continuo del estado de DINQR
rem con Waitress como servidor WSGI e IIS como reverse proxy.
rem
rem Características:
rem - Verificación del servicio de Windows
rem - Verificación de conectividad de Waitress
rem - Verificación de respuesta de IIS
rem - Verificación de base de datos
rem - Monitoreo de recursos del sistema
rem - Alertas por email (opcional)
rem - Generación de reportes
rem
rem Uso:
rem   monitoreo_waitress.bat         - Verificación única
rem   monitoreo_waitress.bat -watch  - Monitoreo continuo
rem   monitoreo_waitress.bat -report - Generar reporte detallado
rem
rem Autor: DINQR Deployment Team
rem Fecha: %date%
rem ===============================================================================

setlocal EnableDelayedExpansion

set "SCRIPT_DIR=%~dp0"
set "BACKEND_DIR=%SCRIPT_DIR%..\backend"
set "SERVICE_NAME=DINQRBackend"
set "SITE_NAME=DINQR"
set "MONITORING_LOG=%SCRIPT_DIR%\monitoreo_waitress.log"
set "ALERT_LOG=%SCRIPT_DIR%\alertas_sistema.log"

rem Configuración por defecto
set "WAITRESS_PORT=5000"
set "CHECK_INTERVAL=30"
set "MAX_RESPONSE_TIME=5000"
set "ENABLE_EMAIL_ALERTS=false"
set "EMAIL_RECIPIENT="

rem Cargar configuración desde .env si existe
if exist "%BACKEND_DIR%\.env" (
    for /f "usebackq tokens=1,2 delims==" %%a in ("%BACKEND_DIR%\.env") do (
        if "%%a"=="WAITRESS_PORT" set "WAITRESS_PORT=%%b"
        if "%%a"=="MONITORING_EMAIL" set "EMAIL_RECIPIENT=%%b"
        if "%%a"=="ENABLE_EMAIL_ALERTS" set "ENABLE_EMAIL_ALERTS=%%b"
    )
)

rem Verificar parámetros de línea de comandos
set "WATCH_MODE=false"
set "REPORT_MODE=false"
if "%1"=="-watch" set "WATCH_MODE=true"
if "%1"=="--watch" set "WATCH_MODE=true"
if "%1"=="-report" set "REPORT_MODE=true"
if "%1"=="--report" set "REPORT_MODE=true"

echo ===============================================================================
echo DINQR - MONITOR DE SALUD WAITRESS + IIS
echo ===============================================================================
echo Fecha/Hora: %date% %time%
echo Servicio: %SERVICE_NAME%
echo Puerto Waitress: %WAITRESS_PORT%
echo Sitio IIS: %SITE_NAME%
echo Log: %MONITORING_LOG%
echo.

if "%WATCH_MODE%"=="true" (
    echo MODO CONTINUO - Presione Ctrl+C para detener
    echo Intervalo de verificación: %CHECK_INTERVAL% segundos
    echo.
)

if "%REPORT_MODE%"=="true" (
    call :generate_detailed_report
    goto :end
)

rem Inicializar log de monitoreo
echo [%date% %time%] === INICIO MONITOREO DINQR === >> "%MONITORING_LOG%"

:monitoring_loop
call :perform_health_checks
if "%WATCH_MODE%"=="true" (
    timeout /t %CHECK_INTERVAL% >nul
    goto :monitoring_loop
)

goto :end

rem ===============================================================================
rem FUNCIONES DE MONITOREO
rem ===============================================================================

:perform_health_checks
set "ALL_CHECKS_PASSED=true"
set "TIMESTAMP=%date% %time%"

echo [%TIMESTAMP%] Iniciando verificaciones de salud...
echo [%TIMESTAMP%] Verificaciones de salud iniciadas >> "%MONITORING_LOG%"

rem 1. Verificar servicio de Windows
call :check_windows_service
if errorlevel 1 set "ALL_CHECKS_PASSED=false"

rem 2. Verificar Waitress
call :check_waitress_server
if errorlevel 1 set "ALL_CHECKS_PASSED=false"

rem 3. Verificar IIS
call :check_iis_site
if errorlevel 1 set "ALL_CHECKS_PASSED=false"

rem 4. Verificar conectividad de base de datos
call :check_database_connection
if errorlevel 1 set "ALL_CHECKS_PASSED=false"

rem 5. Verificar recursos del sistema
call :check_system_resources
if errorlevel 1 set "ALL_CHECKS_PASSED=false"

rem 6. Verificar logs por errores
call :check_error_logs
if errorlevel 1 set "ALL_CHECKS_PASSED=false"

echo.
if "%ALL_CHECKS_PASSED%"=="true" (
    echo ✓ ESTADO: SALUDABLE - Todos los componentes funcionan correctamente
    echo [%TIMESTAMP%] ESTADO: SALUDABLE >> "%MONITORING_LOG%"
) else (
    echo ✗ ESTADO: PROBLEMAS DETECTADOS - Revise los detalles arriba
    echo [%TIMESTAMP%] ESTADO: PROBLEMAS DETECTADOS >> "%MONITORING_LOG%"
    call :send_alert "DINQR: Problemas detectados en el sistema"
)

echo ===============================================================================
exit /b 0

:check_windows_service
echo   Verificando servicio de Windows '%SERVICE_NAME%'...
sc query "%SERVICE_NAME%" >nul 2>&1
if errorlevel 1 (
    echo   ✗ Servicio '%SERVICE_NAME%' no esta instalado
    echo [%TIMESTAMP%] ERROR: Servicio no instalado >> "%MONITORING_LOG%"
    exit /b 1
)

sc query "%SERVICE_NAME%" | find "STATE" | find "RUNNING" >nul
if errorlevel 1 (
    echo   ✗ Servicio '%SERVICE_NAME%' no esta ejecutandose
    echo [%TIMESTAMP%] ERROR: Servicio no ejecutandose >> "%MONITORING_LOG%"
    
    rem Intentar reiniciar el servicio
    echo   Intentando reiniciar el servicio...
    sc start "%SERVICE_NAME%" >nul 2>&1
    timeout /t 10 >nul
    
    sc query "%SERVICE_NAME%" | find "STATE" | find "RUNNING" >nul
    if errorlevel 1 (
        echo   ✗ No se pudo reiniciar el servicio
        echo [%TIMESTAMP%] ERROR: Reinicio de servicio fallido >> "%MONITORING_LOG%"
        exit /b 1
    ) else (
        echo   ✓ Servicio reiniciado exitosamente
        echo [%TIMESTAMP%] INFO: Servicio reiniciado >> "%MONITORING_LOG%"
    )
) else (
    echo   ✓ Servicio ejecutandose correctamente
    echo [%TIMESTAMP%] OK: Servicio ejecutandose >> "%MONITORING_LOG%"
)
exit /b 0

:check_waitress_server
echo   Verificando servidor Waitress (puerto %WAITRESS_PORT%)...

rem Verificar conectividad básica
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:%WAITRESS_PORT%/api/v1/health' -Method GET -TimeoutSec 10; if ($response.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }" >nul 2>&1

if errorlevel 1 (
    echo   ✗ Waitress no responde en puerto %WAITRESS_PORT%
    echo [%TIMESTAMP%] ERROR: Waitress no responde >> "%MONITORING_LOG%"
    exit /b 1
) else (
    echo   ✓ Waitress responde correctamente
    echo [%TIMESTAMP%] OK: Waitress responde >> "%MONITORING_LOG%"
)

rem Verificar tiempo de respuesta
for /f %%i in ('powershell -Command "$start = Get-Date; try { Invoke-WebRequest -Uri 'http://localhost:%WAITRESS_PORT%/api/v1/health' -Method GET -TimeoutSec 10 > $null; $end = Get-Date; [int](($end - $start).TotalMilliseconds) } catch { 9999 }"') do set "RESPONSE_TIME=%%i"

if %RESPONSE_TIME% gtr %MAX_RESPONSE_TIME% (
    echo   ⚠ Tiempo de respuesta alto: %RESPONSE_TIME%ms (limite: %MAX_RESPONSE_TIME%ms)
    echo [%TIMESTAMP%] WARNING: Tiempo respuesta alto %RESPONSE_TIME%ms >> "%MONITORING_LOG%"
) else (
    echo   ✓ Tiempo de respuesta: %RESPONSE_TIME%ms
    echo [%TIMESTAMP%] OK: Tiempo respuesta %RESPONSE_TIME%ms >> "%MONITORING_LOG%"
)

exit /b 0

:check_iis_site
echo   Verificando sitio IIS '%SITE_NAME%'...

rem Verificar que el sitio existe
%windir%\system32\inetsrv\appcmd.exe list site "%SITE_NAME%" >nul 2>&1
if errorlevel 1 (
    echo   ✗ Sitio IIS '%SITE_NAME%' no existe
    echo [%TIMESTAMP%] ERROR: Sitio IIS no existe >> "%MONITORING_LOG%"
    exit /b 1
)

rem Verificar que el sitio está iniciado
%windir%\system32\inetsrv\appcmd.exe list site "%SITE_NAME%" | find "state:Started" >nul
if errorlevel 1 (
    echo   ✗ Sitio IIS '%SITE_NAME%' no esta iniciado
    echo [%TIMESTAMP%] ERROR: Sitio IIS no iniciado >> "%MONITORING_LOG%"
    
    rem Intentar iniciar el sitio
    echo   Intentando iniciar el sitio...
    %windir%\system32\inetsrv\appcmd.exe start site "%SITE_NAME%" >nul 2>&1
    timeout /t 5 >nul
    
    %windir%\system32\inetsrv\appcmd.exe list site "%SITE_NAME%" | find "state:Started" >nul
    if errorlevel 1 (
        echo   ✗ No se pudo iniciar el sitio IIS
        echo [%TIMESTAMP%] ERROR: Inicio sitio IIS fallido >> "%MONITORING_LOG%"
        exit /b 1
    ) else (
        echo   ✓ Sitio IIS iniciado exitosamente
        echo [%TIMESTAMP%] INFO: Sitio IIS iniciado >> "%MONITORING_LOG%"
    )
) else (
    echo   ✓ Sitio IIS ejecutandose correctamente
    echo [%TIMESTAMP%] OK: Sitio IIS ejecutandose >> "%MONITORING_LOG%"
)

rem Verificar respuesta HTTP del sitio
curl -s -I http://localhost/ | find "200" >nul 2>&1
if errorlevel 1 (
    echo   ✗ Sitio IIS no responde via HTTP
    echo [%TIMESTAMP%] ERROR: Sitio IIS no responde HTTP >> "%MONITORING_LOG%"
    exit /b 1
) else (
    echo   ✓ Sitio IIS responde via HTTP
    echo [%TIMESTAMP%] OK: Sitio IIS responde HTTP >> "%MONITORING_LOG%"
)

exit /b 0

:check_database_connection
echo   Verificando conexión a base de datos...

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
except Exception as e:
    print(f'DB_ERROR: {str(e)}')
    sys.exit(1)
" >nul 2>&1

if errorlevel 1 (
    echo   ✗ Error de conexión a base de datos
    echo [%TIMESTAMP%] ERROR: Conexion BD fallida >> "%MONITORING_LOG%"
    exit /b 1
) else (
    echo   ✓ Conexión a base de datos exitosa
    echo [%TIMESTAMP%] OK: Conexion BD exitosa >> "%MONITORING_LOG%"
)

exit /b 0

:check_system_resources
echo   Verificando recursos del sistema...

rem Verificar uso de CPU
for /f "skip=1" %%p in ('wmic cpu get loadpercentage /value') do (
    for /f "tokens=2 delims==" %%i in ("%%p") do set "CPU_USAGE=%%i"
)

if defined CPU_USAGE (
    if %CPU_USAGE% gtr 90 (
        echo   ⚠ Uso de CPU alto: %CPU_USAGE%%
        echo [%TIMESTAMP%] WARNING: CPU alto %CPU_USAGE%% >> "%MONITORING_LOG%"
    ) else (
        echo   ✓ Uso de CPU: %CPU_USAGE%%
        echo [%TIMESTAMP%] OK: CPU %CPU_USAGE%% >> "%MONITORING_LOG%"
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
    if !MEM_USAGE! gtr 90 (
        echo   ⚠ Uso de memoria alto: !MEM_USAGE!%%
        echo [%TIMESTAMP%] WARNING: Memoria alta !MEM_USAGE!%% >> "%MONITORING_LOG%"
    ) else (
        echo   ✓ Uso de memoria: !MEM_USAGE!%%
        echo [%TIMESTAMP%] OK: Memoria !MEM_USAGE!%% >> "%MONITORING_LOG%"
    )
)

rem Verificar espacio en disco
for /f "tokens=3" %%i in ('dir /-c %SystemDrive%\ ^| find "bytes free"') do set "FREE_SPACE=%%i"
if defined FREE_SPACE (
    rem Simplificada verificación de espacio (asume que menos de 1GB es crítico)
    if %FREE_SPACE% lss 1073741824 (
        echo   ⚠ Espacio en disco bajo: %FREE_SPACE% bytes
        echo [%TIMESTAMP%] WARNING: Espacio disco bajo >> "%MONITORING_LOG%"
    ) else (
        echo   ✓ Espacio en disco: %FREE_SPACE% bytes
        echo [%TIMESTAMP%] OK: Espacio disco suficiente >> "%MONITORING_LOG%"
    )
)

exit /b 0

:check_error_logs
echo   Verificando logs por errores recientes...

set "ERROR_FOUND=false"

rem Verificar log de aplicación
if exist "%BACKEND_DIR%\logs\app.log" (
    powershell -Command "Get-Content '%BACKEND_DIR%\logs\app.log' -Tail 100 | Select-String -Pattern 'ERROR|CRITICAL|FATAL' -Quiet" >nul 2>&1
    if not errorlevel 1 (
        echo   ⚠ Errores encontrados en log de aplicación
        echo [%TIMESTAMP%] WARNING: Errores en app.log >> "%MONITORING_LOG%"
        set "ERROR_FOUND=true"
    )
)

rem Verificar log del servidor
if exist "%BACKEND_DIR%\logs\server.log" (
    powershell -Command "Get-Content '%BACKEND_DIR%\logs\server.log' -Tail 50 | Select-String -Pattern 'ERROR|CRITICAL|FATAL' -Quiet" >nul 2>&1
    if not errorlevel 1 (
        echo   ⚠ Errores encontrados en log del servidor
        echo [%TIMESTAMP%] WARNING: Errores en server.log >> "%MONITORING_LOG%"
        set "ERROR_FOUND=true"
    )
)

if "%ERROR_FOUND%"=="false" (
    echo   ✓ No se encontraron errores recientes en logs
    echo [%TIMESTAMP%] OK: Sin errores en logs >> "%MONITORING_LOG%"
)

exit /b 0

:send_alert
if not "%ENABLE_EMAIL_ALERTS%"=="true" goto :skip_email_alert
if "%EMAIL_RECIPIENT%"=="" goto :skip_email_alert

set "ALERT_SUBJECT=%~1"
set "ALERT_BODY=Se detectaron problemas en el sistema DINQR. Revise el log de monitoreo para mas detalles: %MONITORING_LOG%"

echo [%TIMESTAMP%] ALERTA: %ALERT_SUBJECT% >> "%ALERT_LOG%"

rem Aquí se puede integrar con un sistema de envío de emails
rem Por ejemplo, usando PowerShell con Send-MailMessage
powershell -Command "
try {
    Send-MailMessage -To '%EMAIL_RECIPIENT%' -Subject '%ALERT_SUBJECT%' -Body '%ALERT_BODY%' -SmtpServer 'localhost' -From 'dinqr@localhost'
    Write-Host 'Alerta enviada por email'
} catch {
    Write-Host 'Error enviando alerta por email: ' $_.Exception.Message
}
" >nul 2>&1

:skip_email_alert
exit /b 0

:generate_detailed_report
echo.
echo GENERANDO REPORTE DETALLADO DE SISTEMA...
echo ===============================================================================

set "REPORT_FILE=%SCRIPT_DIR%\reporte_sistema_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.txt"

echo DINQR - Reporte de Estado del Sistema > "%REPORT_FILE%"
echo ============================================== >> "%REPORT_FILE%"
echo Fecha/Hora: %date% %time% >> "%REPORT_FILE%"
echo. >> "%REPORT_FILE%"

echo 1. INFORMACION DEL SISTEMA >> "%REPORT_FILE%"
echo ------------------------------ >> "%REPORT_FILE%"
systeminfo | find "OS Name" >> "%REPORT_FILE%"
systeminfo | find "OS Version" >> "%REPORT_FILE%"
systeminfo | find "System Type" >> "%REPORT_FILE%"
systeminfo | find "Total Physical Memory" >> "%REPORT_FILE%"
echo. >> "%REPORT_FILE%"

echo 2. ESTADO DE SERVICIOS >> "%REPORT_FILE%"
echo ----------------------- >> "%REPORT_FILE%"
sc query "%SERVICE_NAME%" >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

echo 3. ESTADO DE IIS >> "%REPORT_FILE%"
echo ----------------- >> "%REPORT_FILE%"
%windir%\system32\inetsrv\appcmd.exe list site "%SITE_NAME%" >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

echo 4. PUERTOS DE RED >> "%REPORT_FILE%"
echo ------------------ >> "%REPORT_FILE%"
netstat -an | find ":%WAITRESS_PORT%" >> "%REPORT_FILE%"
netstat -an | find ":80" | find "LISTENING" >> "%REPORT_FILE%"
netstat -an | find ":443" | find "LISTENING" >> "%REPORT_FILE%"
echo. >> "%REPORT_FILE%"

echo 5. PROCESOS RELACIONADOS >> "%REPORT_FILE%"
echo -------------------------- >> "%REPORT_FILE%"
tasklist | find /i "python" >> "%REPORT_FILE%"
tasklist | find /i "w3wp" >> "%REPORT_FILE%"
echo. >> "%REPORT_FILE%"

echo 6. LOGS RECIENTES >> "%REPORT_FILE%"
echo ------------------ >> "%REPORT_FILE%"
if exist "%BACKEND_DIR%\logs\app.log" (
    echo Ultimas 20 lineas del log de aplicacion: >> "%REPORT_FILE%"
    powershell "Get-Content '%BACKEND_DIR%\logs\app.log' -Tail 20" >> "%REPORT_FILE%"
    echo. >> "%REPORT_FILE%"
)

echo 7. CONFIGURACION ACTUAL >> "%REPORT_FILE%"
echo ------------------------- >> "%REPORT_FILE%"
if exist "%BACKEND_DIR%\.env" (
    echo Configuracion desde .env: >> "%REPORT_FILE%"
    type "%BACKEND_DIR%\.env" | find /v "PASSWORD" | find /v "SECRET" >> "%REPORT_FILE%"
    echo. >> "%REPORT_FILE%"
)

echo.
echo ✓ Reporte generado: %REPORT_FILE%
echo   El reporte contiene información detallada del estado del sistema.
echo.

exit /b 0

:end
echo.
echo Monitoreo completado. Para más opciones use:
echo   %~nx0 -watch   (monitoreo continuo)
echo   %~nx0 -report  (reporte detallado)
echo.
exit /b 0
