@echo off
title DINQR - Verificacion de Permisos
color 0E

echo =============================================
echo DINQR - Verificacion de Permisos de Windows
echo =============================================
echo.

echo Verificando permisos actuales...
echo.

:: Verificar si es administrador
net session >nul 2>&1
if %errorLevel% equ 0 (
    echo ✅ PERMISOS: Ejecutandose como Administrador
    set "IS_ADMIN=true"
) else (
    echo ❌ PERMISOS: NO ejecutandose como Administrador
    set "IS_ADMIN=false"
)

echo.
echo === INFORMACION DEL USUARIO ===
echo Usuario actual: %USERNAME%
echo Dominio/PC: %USERDOMAIN%
echo.

echo === VERIFICACION DE GRUPOS ===
whoami /groups | find "Administradores" >nul
if %errorLevel% equ 0 (
    echo ✅ GRUPOS: Usuario pertenece al grupo Administradores
) else (
    echo ❌ GRUPOS: Usuario NO pertenece al grupo Administradores
)

echo.
echo === PRUEBA DE OPERACION ADMINISTRATIVA ===
echo Intentando acceder al registro de servicios...

reg query "HKLM\SYSTEM\CurrentControlSet\Services" >nul 2>&1
if %errorLevel% equ 0 (
    echo ✅ REGISTRO: Acceso exitoso a registro de servicios
) else (
    echo ❌ REGISTRO: No se puede acceder al registro de servicios
)

echo.
echo === VERIFICACION UAC ===
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v EnableLUA 2>nul | find "0x1" >nul
if %errorLevel% equ 0 (
    echo ⚠️  UAC: Control de Cuentas de Usuario HABILITADO
    echo    Esto puede causar problemas incluso ejecutando como admin
) else (
    echo ✅ UAC: Control de Cuentas de Usuario deshabilitado o no encontrado
)

echo.
echo === RECOMENDACIONES ===

if "%IS_ADMIN%"=="true" (
    echo ✅ Los permisos parecen correctos
    echo.
    echo Probando instalacion del servicio...
    generadorqr.exe --service install
) else (
    echo ❌ PROBLEMA: No tiene permisos de administrador
    echo.
    echo SOLUCIONES:
    echo 1. Cerrar esta ventana
    echo 2. Click derecho en "Simbolo del sistema" o "PowerShell"
    echo 3. Seleccionar "Ejecutar como administrador"
    echo 4. Navegar al directorio: cd /d "%~dp0"
    echo 5. Ejecutar nuevamente: generadorqr.exe --service install
    echo.
    echo O usar alternativa NSSM:
    echo    instalar_servicio_nssm.bat
)

echo.
echo === INFORMACION ADICIONAL ===
echo Directorio actual: %CD%
echo Ejecutable: generadorqr.exe
if exist "generadorqr.exe" (
    echo ✅ Ejecutable encontrado
) else (
    echo ❌ Ejecutable NO encontrado
)

echo.
pause
