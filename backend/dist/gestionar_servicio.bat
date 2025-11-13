@echo off
title DINQR - Gestión de Servicio
color 0E

echo ====================================
echo DINQR Backend - Gestión de Servicio
echo ====================================
echo.

:: Verificar que el ejecutable existe
if not exist "generadorqr.exe" (
    echo ERROR: No se encontro generadorqr.exe en este directorio
    pause
    exit /b 1
)

:menu
echo Seleccione una opción:
echo.
echo 1. Ver estado del servicio
echo 2. Iniciar servicio
echo 3. Detener servicio
echo 4. Reiniciar servicio
echo 5. Remover servicio (requiere admin)
echo 6. Ver logs del servicio
echo 7. Probar conexión (Health Check)
echo 8. Abrir documentación API
echo 9. Salir
echo.
set /p choice="Ingrese su opción (1-9): "

if "%choice%"=="1" goto status
if "%choice%"=="2" goto start
if "%choice%"=="3" goto stop
if "%choice%"=="4" goto restart
if "%choice%"=="5" goto remove
if "%choice%"=="6" goto logs
if "%choice%"=="7" goto health
if "%choice%"=="8" goto docs
if "%choice%"=="9" goto exit

echo Opción inválida. Intente nuevamente.
echo.
goto menu

:status
echo.
echo Verificando estado del servicio...
generadorqr.exe --service status
echo.
pause
goto menu

:start
echo.
echo Iniciando servicio...
generadorqr.exe --service start
echo.
pause
goto menu

:stop
echo.
echo Deteniendo servicio...
generadorqr.exe --service stop
echo.
pause
goto menu

:restart
echo.
echo Reiniciando servicio...
generadorqr.exe --service restart
echo.
pause
goto menu

:remove
echo.
echo ADVERTENCIA: Esto eliminará permanentemente el servicio
echo ¿Está seguro? (S/N^)
set /p confirm=
if /i "%confirm%"=="S" (
    echo Removiendo servicio...
    generadorqr.exe --service remove
)
echo.
pause
goto menu

:logs
echo.
echo Mostrando logs del servicio...
if exist "logs\windows_service.log" (
    echo Últimas 20 líneas del log del servicio:
    echo ========================================
    powershell -Command "Get-Content 'logs\windows_service.log' -Tail 20"
) else (
    echo No se encontró el archivo de log del servicio
)
echo.
if exist "logs\app.log" (
    echo Últimas 10 líneas del log de la aplicación:
    echo ==========================================
    powershell -Command "Get-Content 'logs\app.log' -Tail 10"
) else (
    echo No se encontró el archivo de log de la aplicación
)
echo.
pause
goto menu

:health
echo.
echo Probando conexión al servicio...
echo Realizando Health Check en http://127.0.0.1:5000/health
echo.

:: Usar PowerShell para hacer la petición HTTP
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://127.0.0.1:5000/health' -UseBasicParsing -TimeoutSec 10; Write-Host '✅ Servicio respondiendo correctamente'; Write-Host 'Status Code:' $response.StatusCode; Write-Host 'Respuesta:' $response.Content } catch { Write-Host '❌ Error al conectar con el servicio:' $_.Exception.Message }"

echo.
pause
goto menu

:docs
echo.
echo Abriendo documentación de la API...
start http://127.0.0.1:5000/apidocs/
echo.
echo Si el navegador no se abre automáticamente, visite:
echo http://127.0.0.1:5000/apidocs/
echo.
pause
goto menu

:exit
echo.
echo ¡Hasta luego!
exit /b 0
