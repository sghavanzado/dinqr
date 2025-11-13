@echo off
title DINQR - Instalación de Servicio con NSSM
color 0C

echo ===============================================
echo DINQR Backend - Instalación de Servicio (NSSM)
echo ===============================================
echo.
echo Este script instala DINQR como servicio usando NSSM
echo (Non-Sucking Service Manager) como alternativa.
echo.

:: Verificar permisos de administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Se requieren permisos de administrador
    echo.
    echo Por favor, ejecute este script como administrador
    pause
    exit /b 1
)

:: Verificar que el ejecutable existe
if not exist "generadorqr.exe" (
    echo ERROR: No se encontro generadorqr.exe en este directorio
    pause
    exit /b 1
)

:: Obtener la ruta completa del directorio actual
set "CURRENT_DIR=%~dp0"
set "EXE_PATH=%CURRENT_DIR%generadorqr.exe"

echo Directorio de trabajo: %CURRENT_DIR%
echo Ejecutable: %EXE_PATH%
echo.

:: Verificar si NSSM está disponible
where nssm >nul 2>&1
if %errorLevel% neq 0 (
    echo NSSM no está instalado o no está en el PATH
    echo.
    echo Opciones:
    echo 1. Descargar NSSM desde: https://nssm.cc/download
    echo 2. Extraer nssm.exe al directorio actual
    echo 3. O agregarlo al PATH del sistema
    echo.
    echo ¿Desea continuar con la instalación nativa de Windows? (S/N^)
    set /p useNative=
    if /i "%useNative%"=="S" (
        echo Intentando instalación nativa...
        generadorqr.exe --service install
        if %errorLevel% equ 0 (
            echo ✅ Servicio instalado correctamente con método nativo
        ) else (
            echo ❌ Error en instalación nativa
        )
    ) else (
        echo Instalación cancelada
    )
    pause
    exit /b 1
)

echo NSSM encontrado. Procediendo con la instalación...
echo.

:: Verificar si el servicio ya existe
nssm status DINQRBackend >nul 2>&1
if %errorLevel% equ 0 (
    echo El servicio DINQRBackend ya existe
    echo ¿Desea removerlo y reinstalarlo? (S/N^)
    set /p reinstall=
    if /i "%reinstall%"=="S" (
        echo Removiendo servicio existente...
        nssm stop DINQRBackend
        nssm remove DINQRBackend confirm
    ) else (
        echo Instalación cancelada
        pause
        exit /b 0
    )
)

echo Instalando servicio DINQR Backend con NSSM...

:: Instalar el servicio
nssm install DINQRBackend "%EXE_PATH%"

if %errorLevel% neq 0 (
    echo ❌ Error al instalar el servicio
    pause
    exit /b 1
)

:: Configurar el servicio
echo Configurando servicio...

:: Establecer directorio de trabajo
nssm set DINQRBackend AppDirectory "%CURRENT_DIR%"

:: Configurar descripción
nssm set DINQRBackend Description "DINQR Flask Backend Service - Generador de Códigos QR"

:: Configurar inicio automático
nssm set DINQRBackend Start SERVICE_AUTO_START

:: Configurar logs
nssm set DINQRBackend AppStdout "%CURRENT_DIR%logs\nssm_stdout.log"
nssm set DINQRBackend AppStderr "%CURRENT_DIR%logs\nssm_stderr.log"

:: Configurar rotación de logs
nssm set DINQRBackend AppRotateFiles 1
nssm set DINQRBackend AppRotateOnline 1
nssm set DINQRBackend AppRotateBytes 1048576

:: Configurar reinicio automático
nssm set DINQRBackend AppExit Default Restart
nssm set DINQRBackend AppRestartDelay 5000

echo ✅ Servicio configurado correctamente
echo.

:: Preguntar si iniciar el servicio
echo ¿Desea iniciar el servicio ahora? (S/N^)
set /p startNow=
if /i "%startNow%"=="S" (
    echo Iniciando servicio...
    nssm start DINQRBackend
    
    if %errorLevel% equ 0 (
        echo ✅ Servicio iniciado correctamente
        echo.
        echo Verificando estado...
        timeout /t 3 >nul
        nssm status DINQRBackend
        
        echo.
        echo 🌐 Servicio disponible en: http://127.0.0.1:5000
        echo 📚 API Docs: http://127.0.0.1:5000/apidocs/
        echo ❤️  Health Check: http://127.0.0.1:5000/health
    ) else (
        echo ❌ Error al iniciar el servicio
        echo Revise los logs en: logs\nssm_stderr.log
    )
)

echo.
echo ===== COMANDOS DE GESTIÓN =====
echo Estado:      nssm status DINQRBackend
echo Iniciar:     nssm start DINQRBackend
echo Detener:     nssm stop DINQRBackend
echo Reiniciar:   nssm restart DINQRBackend
echo Remover:     nssm remove DINQRBackend confirm
echo Editar:      nssm edit DINQRBackend
echo.
echo También puede usar el Administrador de Servicios de Windows
echo Busque: "DINQRBackend"

pause
