@echo off
title DINQR Backend - Generador QR
color 0A

echo ================================
echo DINQR Backend - Generador QR
echo ================================
echo.

:: Verificar que el ejecutable existe
if not exist "generadorqr.exe" (
    echo ERROR: No se encontro generadorqr.exe en este directorio
    echo.
    echo Asegurese de que este script este en el mismo directorio que generadorqr.exe
    pause
    exit /b 1
)

:: Verificar que existe el archivo .env
if not exist ".env" (
    echo ADVERTENCIA: No se encontro el archivo .env
    echo.
    if exist ".env.template" (
        echo Se encontro .env.template. ¿Desea copiarlo como .env? (S/N^)
        set /p response=
        if /i "%response%"=="S" (
            copy ".env.template" ".env"
            echo Archivo .env creado. IMPORTANTE: Edite .env con sus configuraciones antes de continuar.
            echo.
            pause
        ) else (
            echo Continuando sin archivo .env (se usaran valores por defecto^)
            echo.
        )
    ) else (
        echo No se encontro .env.template. Continuando con valores por defecto.
        echo.
    )
)

:: Crear directorios necesarios
if not exist "logs" mkdir logs
if not exist "static" mkdir static
if not exist "uploads" mkdir uploads
if not exist "data" mkdir data

echo Directorios verificados: logs, static, uploads, data
echo.

echo Iniciando el servidor DINQR Backend...
echo.
echo El servidor se iniciara en: http://127.0.0.1:5000
echo Documentacion API disponible en: http://127.0.0.1:5000/apidocs/
echo.
echo Presione Ctrl+C para detener el servidor
echo ================================
echo.

:: Ejecutar el servidor
generadorqr.exe

echo.
echo El servidor se ha detenido.
pause
