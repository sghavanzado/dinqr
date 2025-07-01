@echo off
echo ====================================
echo   MONITOREO DE SALUD - DINQR
echo ====================================

:: Configurar variables
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..
set LOG_DIR=%SCRIPT_DIR%deployment-logs
set HEALTH_LOG=%LOG_DIR%\health_check_%date:~-4,4%%date:~-10,2%%date:~-7,2%.log

:: Crear directorio de logs si no existe
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

echo [INFO] Iniciando verificación de salud del sistema DINQR...
echo [INFO] Log: %HEALTH_LOG%

echo [%date% %time%] INICIO: Verificación de salud >> "%HEALTH_LOG%"

echo.
echo ====================================
echo   VERIFICACIÓN DE SERVICIOS
echo ====================================

:: Verificar IIS
echo [INFO] Verificando servicio IIS...
sc query "W3SVC" | find "RUNNING" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] ❌ Servicio IIS no está ejecutándose
    echo [%date% %time%] ERROR: Servicio IIS no ejecutándose >> "%HEALTH_LOG%"
    set /a error_count+=1
) else (
    echo [OK] ✅ Servicio IIS ejecutándose
    echo [%date% %time%] OK: Servicio IIS ejecutándose >> "%HEALTH_LOG%"
)

:: Verificar PostgreSQL
echo [INFO] Verificando servicio PostgreSQL...
sc query "postgresql*" | find "RUNNING" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] ❌ Servicio PostgreSQL no está ejecutándose
    echo [%date% %time%] ERROR: Servicio PostgreSQL no ejecutándose >> "%HEALTH_LOG%"
    set /a error_count+=1
) else (
    echo [OK] ✅ Servicio PostgreSQL ejecutándose
    echo [%date% %time%] OK: Servicio PostgreSQL ejecutándose >> "%HEALTH_LOG%"
)

echo.
echo ====================================
echo   VERIFICACIÓN DE SITIOS IIS
echo ====================================

:: Verificar sitio DINQR
echo [INFO] Verificando sitio DINQR en IIS...
%windir%\system32\inetsrv\appcmd.exe list site "DINQR" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] ❌ Sitio DINQR no encontrado en IIS
    echo [%date% %time%] ERROR: Sitio DINQR no encontrado >> "%HEALTH_LOG%"
    set /a error_count+=1
) else (
    :: Verificar estado del sitio
    %windir%\system32\inetsrv\appcmd.exe list site "DINQR" | find "Started" >nul 2>&1
    if errorlevel 1 (
        echo [WARNING] ⚠️ Sitio DINQR existe pero no está iniciado
        echo [%date% %time%] WARNING: Sitio DINQR no iniciado >> "%HEALTH_LOG%"
        set /a warning_count+=1
    ) else (
        echo [OK] ✅ Sitio DINQR activo en IIS
        echo [%date% %time%] OK: Sitio DINQR activo >> "%HEALTH_LOG%"
    )
)

:: Verificar pool de aplicaciones
echo [INFO] Verificando pool de aplicaciones...
%windir%\system32\inetsrv\appcmd.exe list apppool "DinqrAppPool" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] ❌ Pool DinqrAppPool no encontrado
    echo [%date% %time%] ERROR: Pool DinqrAppPool no encontrado >> "%HEALTH_LOG%"
    set /a error_count+=1
) else (
    %windir%\system32\inetsrv\appcmd.exe list apppool "DinqrAppPool" | find "Started" >nul 2>&1
    if errorlevel 1 (
        echo [WARNING] ⚠️ Pool DinqrAppPool no está iniciado
        echo [%date% %time%] WARNING: Pool DinqrAppPool no iniciado >> "%HEALTH_LOG%"
        set /a warning_count+=1
    ) else (
        echo [OK] ✅ Pool DinqrAppPool activo
        echo [%date% %time%] OK: Pool DinqrAppPool activo >> "%HEALTH_LOG%"
    )
)

echo.
echo ====================================
echo   VERIFICACIÓN DE CONECTIVIDAD
echo ====================================

:: Verificar conectividad web
echo [INFO] Verificando conectividad del sitio web...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8080' -TimeoutSec 10; if($response.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] ❌ Sitio web no responde en http://localhost:8080
    echo [%date% %time%] ERROR: Sitio web no responde >> "%HEALTH_LOG%"
    set /a error_count+=1
) else (
    echo [OK] ✅ Sitio web responde correctamente
    echo [%date% %time%] OK: Sitio web responde >> "%HEALTH_LOG%"
)

:: Verificar API backend
echo [INFO] Verificando API backend...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8080/api/health' -TimeoutSec 10; if($response.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] ⚠️ API backend no responde en /api/health
    echo [%date% %time%] WARNING: API backend no responde >> "%HEALTH_LOG%"
    set /a warning_count+=1
) else (
    echo [OK] ✅ API backend responde correctamente
    echo [%date% %time%] OK: API backend responde >> "%HEALTH_LOG%"
)

echo.
echo ====================================
echo   VERIFICACIÓN DE BASE DE DATOS
echo ====================================

:: Verificar conexión a base de datos
echo [INFO] Verificando conexión a base de datos...
psql -U dinqr_user -d dinqr_db -c "SELECT 1;" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] ❌ No se puede conectar a la base de datos
    echo [%date% %time%] ERROR: No conexión a base de datos >> "%HEALTH_LOG%"
    set /a error_count+=1
) else (
    echo [OK] ✅ Conexión a base de datos exitosa
    echo [%date% %time%] OK: Conexión a base de datos exitosa >> "%HEALTH_LOG%"
)

echo.
echo ====================================
echo   VERIFICACIÓN DE ARCHIVOS
echo ====================================

:: Verificar archivos críticos
echo [INFO] Verificando archivos críticos...

set CRITICAL_FILES="%PROJECT_ROOT%\backend\app.py" "C:\inetpub\wwwroot\dinqr\web.config" "%PROJECT_ROOT%\backend\.env"

for %%f in (%CRITICAL_FILES%) do (
    if exist %%f (
        echo [OK] ✅ Archivo encontrado: %%f
        echo [%date% %time%] OK: Archivo encontrado: %%f >> "%HEALTH_LOG%"
    ) else (
        echo [ERROR] ❌ Archivo faltante: %%f
        echo [%date% %time%] ERROR: Archivo faltante: %%f >> "%HEALTH_LOG%"
        set /a error_count+=1
    )
)

echo.
echo ====================================
echo   VERIFICACIÓN DE RECURSOS
echo ====================================

:: Verificar uso de CPU y memoria
echo [INFO] Verificando recursos del sistema...

:: CPU
for /f "tokens=2 delims==" %%a in ('wmic cpu get loadpercentage /value ^| find "="') do set cpu_usage=%%a
echo [INFO] Uso de CPU: %cpu_usage%%%
echo [%date% %time%] INFO: Uso de CPU: %cpu_usage%%% >> "%HEALTH_LOG%"

if %cpu_usage% GTR 80 (
    echo [WARNING] ⚠️ Alto uso de CPU (%cpu_usage%%%)
    echo [%date% %time%] WARNING: Alto uso de CPU >> "%HEALTH_LOG%"
    set /a warning_count+=1
)

:: Memoria disponible
for /f "tokens=2 delims==" %%a in ('wmic OS get FreePhysicalMemory /value ^| find "="') do set free_mem=%%a
set /a free_mem_mb=%free_mem%/1024
echo [INFO] Memoria libre: %free_mem_mb% MB
echo [%date% %time%] INFO: Memoria libre: %free_mem_mb% MB >> "%HEALTH_LOG%"

if %free_mem_mb% LSS 500 (
    echo [WARNING] ⚠️ Poca memoria disponible (%free_mem_mb% MB)
    echo [%date% %time%] WARNING: Poca memoria disponible >> "%HEALTH_LOG%"
    set /a warning_count+=1
)

:: Espacio en disco
for /f "tokens=3" %%a in ('dir C:\ ^| find "bytes free"') do set free_space=%%a
echo [INFO] Espacio libre en C:\: %free_space%
echo [%date% %time%] INFO: Espacio libre: %free_space% >> "%HEALTH_LOG%"

echo.
echo ====================================
echo   VERIFICACIÓN DE LOGS
echo ====================================

:: Verificar logs recientes de errores
echo [INFO] Verificando logs de errores recientes...

if exist "%PROJECT_ROOT%\backend\logs\app.log" (
    echo [INFO] Últimas líneas del log de aplicación:
    powershell -Command "Get-Content '%PROJECT_ROOT%\backend\logs\app.log' | Select-Object -Last 5"
    
    :: Buscar errores en las últimas 24 horas
    powershell -Command "$ErrorActionPreference='SilentlyContinue'; $content = Get-Content '%PROJECT_ROOT%\backend\logs\app.log' | Select-Object -Last 100; if($content -match 'ERROR|CRITICAL') { exit 1 } else { exit 0 }" >nul 2>&1
    if not errorlevel 1 (
        echo [OK] ✅ No se encontraron errores críticos en logs recientes
        echo [%date% %time%] OK: No errores críticos en logs >> "%HEALTH_LOG%"
    ) else (
        echo [WARNING] ⚠️ Se encontraron errores en los logs recientes
        echo [%date% %time%] WARNING: Errores encontrados en logs >> "%HEALTH_LOG%"
        set /a warning_count+=1
    )
) else (
    echo [WARNING] ⚠️ Archivo de log de aplicación no encontrado
    echo [%date% %time%] WARNING: Log de aplicación no encontrado >> "%HEALTH_LOG%"
    set /a warning_count+=1
)

echo.
echo ====================================
echo   RESUMEN DE SALUD
echo ====================================

:: Inicializar contadores si no existen
if not defined error_count set error_count=0
if not defined warning_count set warning_count=0

echo [INFO] Verificación completada
echo [%date% %time%] INFO: Verificación completada >> "%HEALTH_LOG%"

echo.
echo [INFO] Errores encontrados: %error_count%
echo [INFO] Advertencias encontradas: %warning_count%

if %error_count% EQU 0 (
    if %warning_count% EQU 0 (
        echo [SUCCESS] 🎉 Sistema DINQR funcionando perfectamente
        echo [%date% %time%] SUCCESS: Sistema funcionando perfectamente >> "%HEALTH_LOG%"
        set health_status=EXCELENTE
    ) else (
        echo [WARNING] ⚠️ Sistema DINQR funcionando con advertencias menores
        echo [%date% %time%] WARNING: Sistema con advertencias menores >> "%HEALTH_LOG%"
        set health_status=BUENO
    )
) else (
    echo [ERROR] ❌ Sistema DINQR con problemas que requieren atención
    echo [%date% %time%] ERROR: Sistema con problemas >> "%HEALTH_LOG%"
    set health_status=PROBLEMAS
)

echo.
echo [INFO] Estado de salud: %health_status%
echo [INFO] Log completo: %HEALTH_LOG%

echo.
echo [INFO] Recomendaciones:
if %error_count% GTR 0 (
    echo [INFO] - Revisar y corregir los errores encontrados
    echo [INFO] - Verificar logs de aplicación para más detalles
    echo [INFO] - Considerar reiniciar servicios problemáticos
)
if %warning_count% GTR 0 (
    echo [INFO] - Monitorear las advertencias reportadas
    echo [INFO] - Considerar optimización de recursos si es necesario
)

echo [INFO] - Ejecutar este script regularmente para monitoreo continuo
echo [INFO] - Para logs en tiempo real: logs_aplicacion.bat
echo [INFO] - Para backup: backup_aplicacion.bat

echo.
pause
