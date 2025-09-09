@echo off
echo Probando el ejecutable generadorqr.exe...
echo.

cd /d "%~dp0"

echo Verificando que el archivo existe...
if not exist "dist\generadorqr.exe" (
    echo ERROR: No se encontro el archivo generadorqr.exe
    pause
    exit /b 1
)

echo Archivo encontrado. Tamano: 
dir "dist\generadorqr.exe" | find "generadorqr.exe"
echo.

echo Ejecutando generadorqr.exe...
echo Presiona Ctrl+C para detener el servidor cuando aparezca el mensaje de inicio
echo.

timeout /t 3
dist\generadorqr.exe

pause
