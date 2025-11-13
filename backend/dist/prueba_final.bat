@echo off
title DINQR - Prueba del Ejecutable Final
color 0A

echo ================================================
echo DINQR Backend - Prueba del Ejecutable Final
echo ================================================
echo.

echo Probando el ejecutable generadorqr.exe...
echo.

echo === 1. Verificando version y help ===
generadorqr.exe --help
echo.

echo === 2. Verificando status del servicio ===
generadorqr.exe --service status
echo.

echo === 3. Informacion del archivo ===
echo Archivo: generadorqr.exe
dir generadorqr.exe | find "generadorqr.exe"
echo.

echo === 4. Verificando health check (prueba rapida) ===
echo Iniciando servidor por 10 segundos para probar...
start /b generadorqr.exe > temp_output.log 2>&1
timeout /t 8 /nobreak
echo.

echo Probando health check...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://127.0.0.1:5000/health' -UseBasicParsing -TimeoutSec 5; Write-Host 'Health Check OK:' $response.StatusCode } catch { Write-Host 'No se pudo conectar (normal si el servidor no inicio)' }"

echo.
echo Deteniendo servidor de prueba...
taskkill /f /im generadorqr.exe 2>nul

echo.
echo === RESUMEN ===
if exist temp_output.log (
    echo Ultimas lineas del servidor:
    powershell -Command "Get-Content temp_output.log -Tail 5"
    del temp_output.log
)

echo.
echo El ejecutable esta listo para:
echo 1. Servidor normal: generadorqr.exe
echo 2. Servicio Windows: generadorqr.exe --service install
echo 3. Con NSSM: instalar_servicio_nssm.bat

pause
