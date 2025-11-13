@echo off
title DINQR - Instalador de Servicio de Windows
color 0B

echo ========================================
echo DINQR Backend - Instalador de Servicio
echo ========================================
echo.

:: Verificar permisos de administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Se requieren permisos de administrador
    echo.
    echo Por favor, ejecute este script como administrador:
    echo 1. Click derecho en el archivo
    echo 2. Seleccione "Ejecutar como administrador"
    echo.
    pause
    exit /b 1
)

:: Verificar que el ejecutable existe
if not exist "generadorqr.exe" (
    echo ERROR: No se encontro generadorqr.exe en este directorio
    echo.
    echo Asegurese de que este script este en el mismo directorio que generadorqr.exe
    pause
    exit /b 1
)

echo Verificando archivo .env...
if not exist ".env" (
    echo ADVERTENCIA: No se encontro el archivo .env
    echo.
    if exist ".env.template" (
        echo Copiando .env.template como .env...
        copy ".env.template" ".env" >nul
        echo ✅ Archivo .env creado
        echo.
        echo IMPORTANTE: Edite el archivo .env con sus configuraciones antes de continuar
        echo Presione cualquier tecla cuando haya configurado .env
        pause
    ) else (
        echo Se usaran valores por defecto
        echo.
    )
)

echo Instalando el servicio DINQR Backend...
echo.

:: Instalar el servicio
generadorqr.exe --service install

if %errorLevel% equ 0 (
    echo.
    echo ✅ Servicio instalado correctamente
    echo.
    echo ¿Desea iniciar el servicio ahora? (S/N^)
    set /p response=
    if /i "%response%"=="S" (
        echo Iniciando servicio...
        generadorqr.exe --service start
        if %errorLevel% equ 0 (
            echo ✅ Servicio iniciado correctamente
            echo.
            echo El servicio DINQR Backend esta ahora ejecutandose
            echo URL: http://127.0.0.1:5000
            echo API Docs: http://127.0.0.1:5000/apidocs/
        ) else (
            echo ❌ Error al iniciar el servicio
            echo Revise los logs en la carpeta logs/
        )
    )
) else (
    echo ❌ Error al instalar el servicio
)

echo.
echo Administracion del servicio:
echo   Iniciar:    generadorqr.exe --service start
echo   Detener:    generadorqr.exe --service stop
echo   Estado:     generadorqr.exe --service status
echo   Remover:    generadorqr.exe --service remove
echo.
echo   O use el Administrador de Servicios de Windows
echo   Busque: "DINQR Backend Service"

pause
