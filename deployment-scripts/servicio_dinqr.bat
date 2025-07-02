@echo off
rem ===============================================================================
rem DINQR Windows Service Management Script
rem ===============================================================================
rem This script provides easy management of the DINQR Windows Service
rem 
rem Usage:
rem   servicio_dinqr.bat install   - Install the service
rem   servicio_dinqr.bat start     - Start the service
rem   servicio_dinqr.bat stop      - Stop the service
rem   servicio_dinqr.bat restart   - Restart the service
rem   servicio_dinqr.bat remove    - Remove the service
rem   servicio_dinqr.bat status    - Show service status
rem   servicio_dinqr.bat debug     - Run in debug mode
rem   servicio_dinqr.bat logs      - Show service logs
rem
rem Author: DINQR Deployment Team
rem Date: %date%
rem ===============================================================================

setlocal EnableDelayedExpansion

set "SCRIPT_DIR=%~dp0"
set "BACKEND_DIR=%SCRIPT_DIR%..\backend"
set "SERVICE_NAME=DINQRBackend"
set "PYTHON_SCRIPT=%BACKEND_DIR%\windows_service.py"

rem Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo Por favor, instale Python y asegurese de que este en el PATH del sistema
    goto :error
)

rem Check if backend directory exists
if not exist "%BACKEND_DIR%" (
    echo ERROR: Directorio del backend no encontrado: %BACKEND_DIR%
    goto :error
)

rem Check if windows_service.py exists
if not exist "%PYTHON_SCRIPT%" (
    echo ERROR: Script del servicio no encontrado: %PYTHON_SCRIPT%
    goto :error
)

rem Get the action parameter
set "ACTION=%1"
if "%ACTION%"=="" (
    call :show_usage
    goto :end
)

echo ===============================================================================
echo DINQR - Gestion del Servicio de Windows
echo ===============================================================================
echo Accion solicitada: %ACTION%
echo Directorio del backend: %BACKEND_DIR%
echo Script del servicio: %PYTHON_SCRIPT%
echo Nombre del servicio: %SERVICE_NAME%
echo.

rem Execute the requested action
if /i "%ACTION%"=="install" goto :install
if /i "%ACTION%"=="start" goto :start
if /i "%ACTION%"=="stop" goto :stop
if /i "%ACTION%"=="restart" goto :restart
if /i "%ACTION%"=="remove" goto :remove
if /i "%ACTION%"=="status" goto :status
if /i "%ACTION%"=="debug" goto :debug
if /i "%ACTION%"=="logs" goto :logs
if /i "%ACTION%"=="help" goto :show_usage

echo ERROR: Accion no reconocida: %ACTION%
call :show_usage
goto :error

:install
echo Instalando el servicio DINQR...
cd /d "%BACKEND_DIR%"
python "%PYTHON_SCRIPT%" install
if errorlevel 1 (
    echo ERROR: Fallo la instalacion del servicio
    goto :error
)
echo Servicio instalado exitosamente.
echo.
echo NOTA: Para iniciar el servicio automaticamente al arrancar Windows:
echo   sc config %SERVICE_NAME% start= auto
echo.
goto :end

:start
echo Iniciando el servicio DINQR...
cd /d "%BACKEND_DIR%"
python "%PYTHON_SCRIPT%" start
if errorlevel 1 (
    echo ERROR: Fallo el inicio del servicio
    goto :error
)
echo Servicio iniciado exitosamente.
goto :end

:stop
echo Deteniendo el servicio DINQR...
cd /d "%BACKEND_DIR%"
python "%PYTHON_SCRIPT%" stop
if errorlevel 1 (
    echo ERROR: Fallo la detencion del servicio
    goto :error
)
echo Servicio detenido exitosamente.
goto :end

:restart
echo Reiniciando el servicio DINQR...
call :stop
timeout /t 3 >nul
call :start
goto :end

:remove
echo Removiendo el servicio DINQR...
cd /d "%BACKEND_DIR%"
python "%PYTHON_SCRIPT%" remove
if errorlevel 1 (
    echo ERROR: Fallo la remocion del servicio
    goto :error
)
echo Servicio removido exitosamente.
goto :end

:status
echo Verificando el estado del servicio DINQR...
sc query "%SERVICE_NAME%" 2>nul | find "STATE" | find /v "STOP_PENDING" | find /v "START_PENDING"
if errorlevel 1 (
    echo El servicio %SERVICE_NAME% no esta instalado o no se puede consultar su estado.
) else (
    echo.
    sc query "%SERVICE_NAME%"
)
goto :end

:debug
echo Ejecutando DINQR en modo debug (consola)...
cd /d "%BACKEND_DIR%"
python "%PYTHON_SCRIPT%" debug
goto :end

:logs
echo Mostrando logs del servicio DINQR...
set "LOG_DIR=%BACKEND_DIR%\logs"
if exist "%LOG_DIR%\app.log" (
    echo.
    echo === Ultimas 50 lineas del log de aplicacion ===
    powershell "Get-Content '%LOG_DIR%\app.log' -Tail 50"
) else (
    echo No se encontro el archivo de log: %LOG_DIR%\app.log
)

if exist "%LOG_DIR%\server.log" (
    echo.
    echo === Ultimas 30 lineas del log del servidor ===
    powershell "Get-Content '%LOG_DIR%\server.log' -Tail 30"
) else (
    echo No se encontro el archivo de log del servidor: %LOG_DIR%\server.log
)
goto :end

:show_usage
echo.
echo DINQR - Script de Gestion del Servicio de Windows
echo ==================================================
echo.
echo Uso: %~nx0 [accion]
echo.
echo Acciones disponibles:
echo   install   - Instalar el servicio de Windows
echo   start     - Iniciar el servicio
echo   stop      - Detener el servicio
echo   restart   - Reiniciar el servicio
echo   remove    - Remover el servicio
echo   status    - Mostrar el estado del servicio
echo   debug     - Ejecutar en modo debug (consola)
echo   logs      - Mostrar los logs del servicio
echo   help      - Mostrar esta ayuda
echo.
echo Ejemplos:
echo   %~nx0 install
echo   %~nx0 start
echo   %~nx0 status
echo   %~nx0 logs
echo.
echo NOTA: Para instalar/remover el servicio necesita privilegios de administrador.
echo       Ejecute cmd/PowerShell como administrador.
echo.
goto :end

:error
echo.
echo ===============================================================================
echo ERROR: La operacion no se completo exitosamente.
echo ===============================================================================
echo.
echo Sugerencias para solucionar problemas:
echo 1. Ejecute este script como administrador para operaciones de install/remove
echo 2. Verifique que Python este instalado y en el PATH del sistema
echo 3. Verifique que el directorio del backend exista y sea accesible
echo 4. Revise los logs para mas detalles: %~nx0 logs
echo 5. Ejecute en modo debug para ver errores detallados: %~nx0 debug
echo.
exit /b 1

:end
echo.
echo Operacion completada.
echo Para mas informacion, use: %~nx0 help
echo.
exit /b 0
