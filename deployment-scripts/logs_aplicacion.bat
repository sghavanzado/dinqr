@echo off
echo ====================================
echo   LOGS APLICACION DINQR EN TIEMPO REAL
echo ====================================

:: Configurar colores para Windows
color 0F

:: Obtener directorio actual
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..
set BACKEND_DIR=%PROJECT_ROOT%\backend

echo [INFO] Monitoreando logs de DINQR en tiempo real...
echo [INFO] Presiona Ctrl+C para salir

echo.
echo ====================================
echo   SELECCION DE LOGS
echo ====================================

echo.
echo [OPCIONES DISPONIBLES]
echo 1. Logs de aplicación Flask (app.log)
echo 2. Logs de acceso HTTP (access.log)
echo 3. Logs de Gunicorn (gunicorn_error.log)
echo 4. Logs de servidor manager (server_manager.log)
echo 5. Logs de IIS (si está disponible)
echo 6. Logs de PostgreSQL
echo 7. Todos los logs (multipanel)
echo 8. Logs más recientes de todos
echo.

set /p LOG_CHOICE="Selecciona una opción (1-8): "

if "%LOG_CHOICE%"=="1" goto :app_log
if "%LOG_CHOICE%"=="2" goto :access_log
if "%LOG_CHOICE%"=="3" goto :gunicorn_log
if "%LOG_CHOICE%"=="4" goto :server_log
if "%LOG_CHOICE%"=="5" goto :iis_log
if "%LOG_CHOICE%"=="6" goto :postgresql_log
if "%LOG_CHOICE%"=="7" goto :all_logs
if "%LOG_CHOICE%"=="8" goto :recent_logs

echo [ERROR] Opción no válida
pause
exit /b 1

:app_log
echo.
echo ====================================
echo   LOGS DE APLICACION FLASK
echo ====================================
echo.
echo [INFO] Monitoreando: %BACKEND_DIR%\logs\app.log
echo [INFO] Últimas 20 líneas:
echo.

if exist "%BACKEND_DIR%\logs\app.log" (
    :: Mostrar últimas líneas
    powershell -Command "Get-Content '%BACKEND_DIR%\logs\app.log' -Tail 20"
    echo.
    echo [INFO] Monitoreando cambios en tiempo real...
    echo [INFO] Presiona Ctrl+C para salir
    echo.
    
    :: Monitorear cambios en tiempo real
    powershell -Command "Get-Content '%BACKEND_DIR%\logs\app.log' -Wait -Tail 0"
) else (
    echo [ERROR] Archivo de log no encontrado: %BACKEND_DIR%\logs\app.log
    pause
)
goto :end

:access_log
echo.
echo ====================================
echo   LOGS DE ACCESO HTTP
echo ====================================
echo.
echo [INFO] Monitoreando: %BACKEND_DIR%\logs\access.log
echo [INFO] Últimas 20 líneas:
echo.

if exist "%BACKEND_DIR%\logs\access.log" (
    powershell -Command "Get-Content '%BACKEND_DIR%\logs\access.log' -Tail 20"
    echo.
    echo [INFO] Monitoreando cambios en tiempo real...
    powershell -Command "Get-Content '%BACKEND_DIR%\logs\access.log' -Wait -Tail 0"
) else (
    echo [ERROR] Archivo de log no encontrado: %BACKEND_DIR%\logs\access.log
    pause
)
goto :end

:gunicorn_log
echo.
echo ====================================
echo   LOGS DE GUNICORN
echo ====================================
echo.
echo [INFO] Monitoreando: %BACKEND_DIR%\logs\gunicorn_error.log
echo [INFO] Últimas 20 líneas:
echo.

if exist "%BACKEND_DIR%\logs\gunicorn_error.log" (
    powershell -Command "Get-Content '%BACKEND_DIR%\logs\gunicorn_error.log' -Tail 20"
    echo.
    echo [INFO] Monitoreando cambios en tiempo real...
    powershell -Command "Get-Content '%BACKEND_DIR%\logs\gunicorn_error.log' -Wait -Tail 0"
) else (
    echo [ERROR] Archivo de log no encontrado: %BACKEND_DIR%\logs\gunicorn_error.log
    pause
)
goto :end

:server_log
echo.
echo ====================================
echo   LOGS DE SERVER MANAGER
echo ====================================
echo.
echo [INFO] Monitoreando: %BACKEND_DIR%\logs\server_manager.log
echo [INFO] Últimas 20 líneas:
echo.

if exist "%BACKEND_DIR%\logs\server_manager.log" (
    powershell -Command "Get-Content '%BACKEND_DIR%\logs\server_manager.log' -Tail 20"
    echo.
    echo [INFO] Monitoreando cambios en tiempo real...
    powershell -Command "Get-Content '%BACKEND_DIR%\logs\server_manager.log' -Wait -Tail 0"
) else (
    echo [ERROR] Archivo de log no encontrado: %BACKEND_DIR%\logs\server_manager.log
    pause
)
goto :end

:iis_log
echo.
echo ====================================
echo   LOGS DE IIS
echo ====================================
echo.

set IIS_LOG_DIR=C:\inetpub\wwwroot\dinqr\logs
echo [INFO] Verificando logs de IIS en: %IIS_LOG_DIR%

if exist "%IIS_LOG_DIR%" (
    echo [INFO] Archivos de log disponibles:
    dir "%IIS_LOG_DIR%" /b
    echo.
    
    if exist "%IIS_LOG_DIR%\wfastcgi.log" (
        echo [INFO] Monitoreando wfastcgi.log
        echo [INFO] Últimas 20 líneas:
        powershell -Command "Get-Content '%IIS_LOG_DIR%\wfastcgi.log' -Tail 20"
        echo.
        echo [INFO] Monitoreando cambios en tiempo real...
        powershell -Command "Get-Content '%IIS_LOG_DIR%\wfastcgi.log' -Wait -Tail 0"
    ) else (
        echo [WARNING] wfastcgi.log no encontrado
        echo [INFO] Logs disponibles:
        if exist "%IIS_LOG_DIR%\*.log" (
            for %%f in ("%IIS_LOG_DIR%\*.log") do (
                echo - %%~nxf
            )
        )
        pause
    )
) else (
    echo [ERROR] Directorio de logs IIS no encontrado: %IIS_LOG_DIR%
    echo [INFO] Verifica que DINQR esté desplegado en IIS
    pause
)
goto :end

:postgresql_log
echo.
echo ====================================
echo   LOGS DE POSTGRESQL
echo ====================================
echo.

set PG_LOG_DIR=C:\Program Files\PostgreSQL\14\data\log
echo [INFO] Verificando logs de PostgreSQL en: %PG_LOG_DIR%

if exist "%PG_LOG_DIR%" (
    echo [INFO] Archivos de log más recientes:
    dir "%PG_LOG_DIR%\*.log" /od /b | powershell -Command "$input | Select-Object -Last 5"
    echo.
    
    :: Obtener el log más reciente
    for /f %%f in ('dir "%PG_LOG_DIR%\*.log" /od /b ^| powershell -Command "$input | Select-Object -Last 1"') do set LATEST_PG_LOG=%%f
    
    if defined LATEST_PG_LOG (
        echo [INFO] Monitoreando log más reciente: %LATEST_PG_LOG%
        echo [INFO] Últimas 20 líneas:
        powershell -Command "Get-Content '%PG_LOG_DIR%\%LATEST_PG_LOG%' -Tail 20"
        echo.
        echo [INFO] Monitoreando cambios en tiempo real...
        powershell -Command "Get-Content '%PG_LOG_DIR%\%LATEST_PG_LOG%' -Wait -Tail 0"
    ) else (
        echo [ERROR] No se encontraron logs de PostgreSQL
        pause
    )
) else (
    echo [ERROR] Directorio de logs PostgreSQL no encontrado: %PG_LOG_DIR%
    echo [INFO] Verifica la instalación de PostgreSQL
    pause
)
goto :end

:all_logs
echo.
echo ====================================
echo   TODOS LOS LOGS (MULTIPANEL)
echo ====================================
echo.
echo [INFO] Abriendo ventanas separadas para cada log...

:: Abrir ventana para cada tipo de log
if exist "%BACKEND_DIR%\logs\app.log" (
    start "DINQR - App Log" cmd /c "title DINQR App Log && powershell -Command \"Get-Content '%BACKEND_DIR%\logs\app.log' -Wait -Tail 10\""
)

if exist "%BACKEND_DIR%\logs\access.log" (
    start "DINQR - Access Log" cmd /c "title DINQR Access Log && powershell -Command \"Get-Content '%BACKEND_DIR%\logs\access.log' -Wait -Tail 10\""
)

if exist "%BACKEND_DIR%\logs\gunicorn_error.log" (
    start "DINQR - Gunicorn Log" cmd /c "title DINQR Gunicorn Log && powershell -Command \"Get-Content '%BACKEND_DIR%\logs\gunicorn_error.log' -Wait -Tail 10\""
)

if exist "C:\inetpub\wwwroot\dinqr\logs\wfastcgi.log" (
    start "DINQR - IIS Log" cmd /c "title DINQR IIS Log && powershell -Command \"Get-Content 'C:\inetpub\wwwroot\dinqr\logs\wfastcgi.log' -Wait -Tail 10\""
)

echo [OK] Ventanas de logs abiertas
echo [INFO] Cierra las ventanas individualmente cuando termines
pause
goto :end

:recent_logs
echo.
echo ====================================
echo   LOGS MAS RECIENTES DE TODOS
echo ====================================
echo.

echo [INFO] Mostrando últimas entradas de todos los logs...
echo.

:: App Log
if exist "%BACKEND_DIR%\logs\app.log" (
    echo [APP LOG - Últimas 5 líneas]
    echo ----------------------------------------
    powershell -Command "Get-Content '%BACKEND_DIR%\logs\app.log' -Tail 5"
    echo.
)

:: Access Log
if exist "%BACKEND_DIR%\logs\access.log" (
    echo [ACCESS LOG - Últimas 5 líneas]
    echo ----------------------------------------
    powershell -Command "Get-Content '%BACKEND_DIR%\logs\access.log' -Tail 5"
    echo.
)

:: Gunicorn Log
if exist "%BACKEND_DIR%\logs\gunicorn_error.log" (
    echo [GUNICORN LOG - Últimas 5 líneas]
    echo ----------------------------------------
    powershell -Command "Get-Content '%BACKEND_DIR%\logs\gunicorn_error.log' -Tail 5"
    echo.
)

:: Server Manager Log
if exist "%BACKEND_DIR%\logs\server_manager.log" (
    echo [SERVER MANAGER LOG - Últimas 5 líneas]
    echo ----------------------------------------
    powershell -Command "Get-Content '%BACKEND_DIR%\logs\server_manager.log' -Tail 5"
    echo.
)

:: IIS Log
if exist "C:\inetpub\wwwroot\dinqr\logs\wfastcgi.log" (
    echo [IIS LOG - Últimas 5 líneas]
    echo ----------------------------------------
    powershell -Command "Get-Content 'C:\inetpub\wwwroot\dinqr\logs\wfastcgi.log' -Tail 5"
    echo.
)

echo [INFO] Fin del resumen de logs
echo.
echo [OPCIONES]
echo 1. Actualizar resumen
echo 2. Monitorear log específico
echo 3. Salir
echo.

set /p NEXT_ACTION="Selecciona una opción (1-3): "

if "%NEXT_ACTION%"=="1" goto :recent_logs
if "%NEXT_ACTION%"=="2" goto :start
if "%NEXT_ACTION%"=="3" goto :end

goto :end

:start
cls
goto :top

:end
echo.
echo [INFO] Monitoreo de logs finalizado
pause
