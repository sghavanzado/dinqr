@echo off
echo ================================================
echo   SOLUCIONADOR DE PROBLEMAS POWERSHELL
echo ================================================
echo.
echo Este script soluciona problemas comunes con la 
echo ejecucion de scripts PowerShell en Windows.
echo.

:: Verificar permisos de administrador
net session >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Este script debe ejecutarse como Administrador
    echo [INFO] Click derecho y selecciona "Ejecutar como administrador"
    echo.
    echo Presiona cualquier tecla para salir...
    pause >nul
    exit /b 1
)

echo [INFO] Permisos de administrador confirmados
echo.

echo ================================================
echo   METODO 1: CONFIGURACION AUTOMATICA
echo ================================================
echo.
echo [INFO] Intentando configurar ExecutionPolicy automaticamente...

:: Intentar configurar ExecutionPolicy con PowerShell
powershell -Command "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force" 2>nul
if errorlevel 0 if not errorlevel 1 (
    echo [OK] ExecutionPolicy configurado exitosamente
    echo.
    echo [INFO] Probando ejecucion de script...
    powershell -File "%~dp0configurar_iis_features.ps1" -WhatIf 2>nul
    if errorlevel 0 if not errorlevel 1 (
        echo [OK] Los scripts PowerShell ahora pueden ejecutarse
        echo [INFO] Puedes continuar con la instalacion
        goto :SUCCESS
    )
)

echo ================================================
echo   METODO 2: CONFIGURACION INTERACTIVA
echo ================================================
echo.
echo [INFO] Abriendo PowerShell para configuracion manual...
echo.
echo INSTRUCCIONES:
echo 1. En la ventana de PowerShell que se abre, ejecuta:
echo    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
echo.
echo 2. Cuando pregunte, responde: S (Si) o Y (Yes)
echo.
echo 3. Cierra PowerShell y presiona cualquier tecla aqui
echo.

start powershell -NoExit -Command "Write-Host 'Ejecuta: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser' -ForegroundColor Yellow"

echo Presiona cualquier tecla cuando hayas configurado PowerShell...
pause >nul

echo.
echo [INFO] Verificando configuracion...
powershell -Command "Get-ExecutionPolicy -Scope CurrentUser" | findstr /i "RemoteSigned Unrestricted" >nul
if errorlevel 1 (
    echo [WARNING] ExecutionPolicy aun parece estar restringido
    goto :MANUAL_METHODS
) else (
    echo [OK] ExecutionPolicy configurado correctamente
    goto :SUCCESS
)

:MANUAL_METHODS
echo.
echo ================================================
echo   METODO 3: OPCIONES MANUALES
echo ================================================
echo.
echo Si los metodos anteriores no funcionaron, puedes:
echo.
echo OPCION A - Ejecutar scripts con Bypass:
echo   PowerShell -ExecutionPolicy Bypass -File configurar_iis_features.ps1
echo.
echo OPCION B - Desbloquear archivos descargados:
echo   1. Click derecho en configurar_iis_features.ps1
echo   2. Seleccionar "Propiedades"
echo   3. Marcar "Desbloquear" si aparece la opcion
echo   4. Aplicar y cerrar
echo.
echo OPCION C - Usar comandos DISM directamente:
echo   Ver archivo README.md seccion "Resolucion de Problemas"
echo.
goto :END

:SUCCESS
echo.
echo ================================================
echo   CONFIGURACION EXITOSA
echo ================================================
echo.
echo [OK] PowerShell configurado correctamente
echo [INFO] Ahora puedes ejecutar:
echo   - instalar_dependencias.bat
echo   - configurar_iis_features.ps1
echo   - Otros scripts de DINQR
echo.

:END
echo.
echo Presiona cualquier tecla para salir...
pause >nul
