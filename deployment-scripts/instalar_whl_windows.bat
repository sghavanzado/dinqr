@echo off
echo ================================================
echo DINQR - Instalador de Backend (.whl) en Windows Server
echo ================================================
echo.

REM Verificar privilegios de administrador
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ADVERTENCIA: Este script necesita ejecutarse como Administrador
    echo Haga clic derecho en el archivo y seleccione "Ejecutar como administrador"
    pause
    exit /b 1
)

REM Configuración de variables
set APP_NAME=dinqr
set APP_USER=dinqr_service
set APP_DIR=C:\inetpub\%APP_NAME%
set PYTHON_DIR=C:\Python312
set VENV_DIR=%APP_DIR%\venv
set SERVICE_NAME=DINQR_Backend
set LOG_DIR=%APP_DIR%\logs

echo Iniciando instalación de DINQR Backend...
echo.

REM Verificar Python 3.12
if not exist "%PYTHON_DIR%\python.exe" (
    echo ERROR: Python 3.12 no encontrado en %PYTHON_DIR%
    echo Por favor, instale Python 3.12 desde https://www.python.org/
    echo Asegúrese de seleccionar "Add Python to PATH" durante la instalación
    pause
    exit /b 1
)

echo Python 3.12 encontrado: %PYTHON_DIR%
echo.

REM Crear directorios de aplicación
echo Creando estructura de directorios...
if not exist "%APP_DIR%" mkdir "%APP_DIR%"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
if not exist "%APP_DIR%\static" mkdir "%APP_DIR%\static"
if not exist "%APP_DIR%\uploads" mkdir "%APP_DIR%\uploads"
if not exist "%APP_DIR%\data" mkdir "%APP_DIR%\data"

REM Crear usuario de servicio
echo Creando usuario de servicio %APP_USER%...
net user %APP_USER% /delete >nul 2>&1
net user %APP_USER% /add /passwordchg:no /passwordreq:no /fullname:"DINQR Service User" /comment:"Usuario para el servicio DINQR"
if %errorlevel% neq 0 (
    echo ADVERTENCIA: No se pudo crear el usuario de servicio
)

REM Configurar permisos en directorios
echo Configurando permisos de directorio...
icacls "%APP_DIR%" /grant "%APP_USER%:(OI)(CI)M" /T
icacls "%APP_DIR%" /grant "IIS_IUSRS:(OI)(CI)RX" /T
icacls "%APP_DIR%" /grant "IUSR:(OI)(CI)RX" /T

REM Crear entorno virtual
echo Creando entorno virtual Python...
cd /d "%APP_DIR%"
"%PYTHON_DIR%\python.exe" -m venv "%VENV_DIR%"
if %errorlevel% neq 0 (
    echo ERROR: No se pudo crear el entorno virtual
    pause
    exit /b 1
)

REM Activar entorno virtual e instalar dependencias
echo Activando entorno virtual e instalando dependencias...
call "%VENV_DIR%\Scripts\activate.bat"

REM Actualizar pip
python -m pip install --upgrade pip

REM Buscar archivo .whl en el directorio actual
for %%f in (*.whl) do (
    echo Instalando %%f...
    pip install "%%f"
    if %errorlevel% neq 0 (
        echo ERROR: No se pudo instalar %%f
        pause
        exit /b 1
    )
    set WHL_INSTALLED=1
)

if not defined WHL_INSTALLED (
    echo ERROR: No se encontró ningún archivo .whl en el directorio actual
    echo Por favor, coloque el archivo .whl generado en el mismo directorio que este script
    pause
    exit /b 1
)

REM Instalar Waitress
echo Instalando Waitress WSGI Server...
pip install waitress
if %errorlevel% neq 0 (
    echo ERROR: No se pudo instalar Waitress
    pause
    exit /b 1
)

REM Copiar archivos de configuración si existen
if exist ".env" (
    echo Copiando archivo de configuración .env...
    copy ".env" "%APP_DIR%\.env"
)

if exist "config.py" (
    echo Copiando archivo de configuración config.py...
    copy "config.py" "%APP_DIR%\config.py"
)

REM Crear script de inicio para Waitress
echo Creando script de inicio de Waitress...
(
echo @echo off
echo cd /d "%APP_DIR%"
echo call "%VENV_DIR%\Scripts\activate.bat"
echo set FLASK_APP=app.py
echo set FLASK_ENV=production
echo waitress-serve --host=127.0.0.1 --port=5000 --threads=4 --call app:create_app
) > "%APP_DIR%\start_waitress.bat"

REM Crear script de servicio Python
echo Creando script de servicio Windows...
(
echo import sys
echo import os
echo import time
echo import subprocess
echo import win32serviceutil
echo import win32service
echo import win32event
echo import servicemanager
echo.
echo class DINQRService^(win32serviceutil.ServiceFramework^):
echo     _svc_name_ = "%SERVICE_NAME%"
echo     _svc_display_name_ = "DINQR Backend Service"
echo     _svc_description_ = "Servicio backend para aplicación DINQR"
echo.
echo     def __init__^(self, args^):
echo         win32serviceutil.ServiceFramework.__init__^(self, args^)
echo         self.hWaitStop = win32event.CreateEvent^(None, 0, 0, None^)
echo         self.process = None
echo.
echo     def SvcStop^(self^):
echo         self.ReportServiceStatus^(win32service.SERVICE_STOP_PENDING^)
echo         if self.process:
echo             self.process.terminate^(^)
echo         win32event.SetEvent^(self.hWaitStop^)
echo.
echo     def SvcDoRun^(self^):
echo         servicemanager.LogMsg^(
echo             servicemanager.EVENTLOG_INFORMATION_TYPE,
echo             servicemanager.PYS_SERVICE_STARTED,
echo             ^(self._svc_name_, ''^^)
echo         ^)
echo         self.main^(^)
echo.
echo     def main^(self^):
echo         os.chdir^(r'%APP_DIR%'^)
echo         cmd = [
echo             r'%VENV_DIR%\Scripts\python.exe',
echo             '-c',
echo             'from waitress import serve; from app import create_app; serve^(create_app^(^), host="127.0.0.1", port=5000, threads=4^)'
echo         ]
echo         
echo         while True:
echo             try:
echo                 self.process = subprocess.Popen^(cmd^)
echo                 self.process.wait^(^)
echo             except Exception as e:
echo                 servicemanager.LogErrorMsg^(f"Error en servicio DINQR: {e}"^)
echo                 time.sleep^(5^)
echo             
echo             if win32event.WaitForSingleObject^(self.hWaitStop, 0^) == win32event.WAIT_OBJECT_0:
echo                 break
echo.
echo if __name__ == '__main__':
echo     win32serviceutil.HandleCommandLine^(DINQRService^)
) > "%APP_DIR%\dinqr_service.py"

REM Instalar pywin32 para servicios Windows
echo Instalando pywin32 para soporte de servicios Windows...
pip install pywin32

REM Instalar el servicio
echo Instalando servicio Windows...
cd /d "%APP_DIR%"
python dinqr_service.py install

echo.
echo ================================================
echo INSTALACIÓN COMPLETADA EXITOSAMENTE
echo ================================================
echo.
echo Directorio de aplicación: %APP_DIR%
echo Usuario de servicio: %APP_USER%
echo Nombre del servicio: %SERVICE_NAME%
echo.
echo PRÓXIMOS PASOS:
echo 1. Configure las variables de entorno en %APP_DIR%\.env
echo 2. Configure la base de datos PostgreSQL
echo 3. Ejecute las migraciones de base de datos
echo 4. Configure IIS como proxy reverso
echo 5. Inicie el servicio Windows
echo.
echo Para iniciar el servicio manualmente:
echo   sc start %SERVICE_NAME%
echo.
echo Para iniciar Waitress manualmente:
echo   cd "%APP_DIR%"
echo   start_waitress.bat
echo.
echo Revise los logs en: %LOG_DIR%
echo.
pause
