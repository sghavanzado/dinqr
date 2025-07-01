@echo off
echo ====================================
echo   REINICIAR SERVICIOS DINQR
echo ====================================

:: Verificar permisos de administrador
net session >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Este script debe ejecutarse como Administrador
    echo [INFO] Click derecho en el archivo y selecciona "Ejecutar como administrador"
    pause
    exit /b 1
)

:: Configurar variables
set SCRIPT_DIR=%~dp0
set LOG_DIR=%SCRIPT_DIR%deployment-logs
set LOG_FILE=%LOG_DIR%\reinicio_servicios_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.log

:: Crear directorio de logs si no existe
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

echo [INFO] Reiniciando servicios de DINQR...
echo [INFO] Log: %LOG_FILE%

echo [%date% %time%] INICIO: Reinicio de servicios DINQR >> "%LOG_FILE%"

echo.
echo ====================================
echo   PASO 1: DETENER SERVICIOS
echo ====================================

echo [INFO] Deteniendo sitio DINQR...
%windir%\system32\inetsrv\appcmd.exe stop site "DINQR" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] No se pudo detener el sitio DINQR (puede que no esté iniciado)
    echo [%date% %time%] WARNING: No se pudo detener sitio DINQR >> "%LOG_FILE%"
) else (
    echo [OK] Sitio DINQR detenido
    echo [%date% %time%] OK: Sitio DINQR detenido >> "%LOG_FILE%"
)

echo [INFO] Deteniendo pool de aplicaciones...
%windir%\system32\inetsrv\appcmd.exe stop apppool "DinqrAppPool" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] No se pudo detener el pool DinqrAppPool (puede que no esté iniciado)
    echo [%date% %time%] WARNING: No se pudo detener pool DinqrAppPool >> "%LOG_FILE%"
) else (
    echo [OK] Pool DinqrAppPool detenido
    echo [%date% %time%] OK: Pool DinqrAppPool detenido >> "%LOG_FILE%"
)

echo [INFO] Esperando 5 segundos para asegurar parada completa...
timeout /t 5 /nobreak >nul

echo.
echo ====================================
echo   PASO 2: LIMPIAR CACHE Y TEMPORALES
echo ====================================

echo [INFO] Limpiando cache de IIS...
%windir%\system32\inetsrv\appcmd.exe recycle apppool "DinqrAppPool" >nul 2>&1

echo [INFO] Limpiando archivos temporales de ASP.NET...
if exist "%WINDIR%\Microsoft.NET\Framework64\v4.0.30319\Temporary ASP.NET Files" (
    for /d %%i in ("%WINDIR%\Microsoft.NET\Framework64\v4.0.30319\Temporary ASP.NET Files\*") do (
        rd /s /q "%%i" 2>nul
    )
    echo [OK] Cache de ASP.NET limpiado
)

echo [INFO] Limpiando cache de FastCGI...
%windir%\system32\inetsrv\appcmd.exe clear config -section:system.webServer/fastCgi >nul 2>&1

echo.
echo ====================================
echo   PASO 3: REINICIAR SERVICIOS
echo ====================================

echo [INFO] Reiniciando servicio IIS...
iisreset /restart >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Error al reiniciar IIS
    echo [%date% %time%] ERROR: Error al reiniciar IIS >> "%LOG_FILE%"
    goto :error
) else (
    echo [OK] IIS reiniciado exitosamente
    echo [%date% %time%] OK: IIS reiniciado >> "%LOG_FILE%"
)

echo [INFO] Esperando que IIS se estabilice...
timeout /t 10 /nobreak >nul

echo [INFO] Iniciando pool de aplicaciones...
%windir%\system32\inetsrv\appcmd.exe start apppool "DinqrAppPool" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Error al iniciar pool DinqrAppPool
    echo [%date% %time%] ERROR: Error al iniciar pool DinqrAppPool >> "%LOG_FILE%"
    goto :error
) else (
    echo [OK] Pool DinqrAppPool iniciado
    echo [%date% %time%] OK: Pool DinqrAppPool iniciado >> "%LOG_FILE%"
)

echo [INFO] Iniciando sitio DINQR...
%windir%\system32\inetsrv\appcmd.exe start site "DINQR" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Error al iniciar sitio DINQR
    echo [%date% %time%] ERROR: Error al iniciar sitio DINQR >> "%LOG_FILE%"
    goto :error
) else (
    echo [OK] Sitio DINQR iniciado
    echo [%date% %time%] OK: Sitio DINQR iniciado >> "%LOG_FILE%"
)

echo.
echo ====================================
echo   PASO 4: VERIFICACIÓN POST-REINICIO
echo ====================================

echo [INFO] Esperando que los servicios se estabilicen...
timeout /t 15 /nobreak >nul

echo [INFO] Verificando estado de servicios...

:: Verificar IIS
sc query "W3SVC" | find "RUNNING" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Servicio IIS no está ejecutándose después del reinicio
    echo [%date% %time%] ERROR: IIS no ejecutándose post-reinicio >> "%LOG_FILE%"
    goto :error
) else (
    echo [OK] Servicio IIS ejecutándose correctamente
)

:: Verificar sitio
%windir%\system32\inetsrv\appcmd.exe list site "DINQR" | find "Started" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Sitio DINQR no está activo después del reinicio
    echo [%date% %time%] ERROR: Sitio DINQR no activo post-reinicio >> "%LOG_FILE%"
    goto :error
) else (
    echo [OK] Sitio DINQR activo correctamente
)

:: Verificar pool
%windir%\system32\inetsrv\appcmd.exe list apppool "DinqrAppPool" | find "Started" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Pool DinqrAppPool no está activo después del reinicio
    echo [%date% %time%] ERROR: Pool DinqrAppPool no activo post-reinicio >> "%LOG_FILE%"
    goto :error
) else (
    echo [OK] Pool DinqrAppPool activo correctamente
)

echo.
echo ====================================
echo   PASO 5: PRUEBA DE CONECTIVIDAD
echo ====================================

echo [INFO] Probando conectividad del sitio web...
timeout /t 5 /nobreak >nul

powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8080' -TimeoutSec 30; if($response.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Sitio web no responde inmediatamente - puede necesitar más tiempo
    echo [%date% %time%] WARNING: Sitio web no responde inmediatamente >> "%LOG_FILE%"
    
    echo [INFO] Esperando 30 segundos adicionales...
    timeout /t 30 /nobreak >nul
    
    powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8080' -TimeoutSec 10; if($response.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }" >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Sitio web no responde después del reinicio
        echo [%date% %time%] ERROR: Sitio web no responde post-reinicio >> "%LOG_FILE%"
        echo [INFO] Revisa los logs de IIS y la aplicación para más detalles
        goto :error
    ) else (
        echo [OK] Sitio web responde correctamente (tras espera adicional)
        echo [%date% %time%] OK: Sitio web responde (con demora) >> "%LOG_FILE%"
    )
) else (
    echo [OK] Sitio web responde correctamente
    echo [%date% %time%] OK: Sitio web responde inmediatamente >> "%LOG_FILE%"
)

echo.
echo ====================================
echo   REINICIO COMPLETADO
echo ====================================

echo [SUCCESS] ¡Servicios de DINQR reiniciados exitosamente!
echo [%date% %time%] SUCCESS: Reinicio completado exitosamente >> "%LOG_FILE%"

echo.
echo [INFO] Estado final:
echo [INFO] ✅ Servicio IIS: Ejecutándose
echo [INFO] ✅ Sitio DINQR: Activo
echo [INFO] ✅ Pool DinqrAppPool: Activo
echo [INFO] ✅ Conectividad web: Funcionando

echo.
echo [INFO] URLs de acceso:
echo [INFO] - Frontend: http://localhost:8080
echo [INFO] - API: http://localhost:8080/api
echo [INFO] - Documentación: http://localhost:8080/api/apidocs

echo.
echo [INFO] Para monitoreo continuo: monitoreo_salud.bat
echo [INFO] Para logs en tiempo real: logs_aplicacion.bat

goto :end

:error
echo [ERROR] El reinicio de servicios falló
echo [ERROR] Revisa el log para más detalles: %LOG_FILE%
echo [%date% %time%] ERROR: Reinicio falló >> "%LOG_FILE%"

echo.
echo [INFO] Pasos de resolución de problemas:
echo [INFO] 1. Verificar logs de IIS: %%WINDIR%%\System32\LogFiles\W3SVC1\
echo [INFO] 2. Verificar logs de aplicación: backend\logs\
echo [INFO] 3. Verificar Event Viewer de Windows
echo [INFO] 4. Intentar reinicio manual: iisreset /restart
echo [INFO] 5. Verificar configuración web.config
echo [INFO] 6. Verificar permisos de archivos

echo.
echo [INFO] Para diagnóstico: monitoreo_salud.bat

pause
exit /b 1

:end
echo.
echo [SUCCESS] Reinicio completado satisfactoriamente
pause
