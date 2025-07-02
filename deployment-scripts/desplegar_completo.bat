@echo off
echo ================================================
echo DINQR - Despliegue Completo en Windows Server
echo ================================================
echo.
echo Este script realizará la instalación y configuración completa de DINQR
echo en Windows Server usando IIS como proxy reverso y Waitress como servidor WSGI.
echo.

REM Verificar privilegios de administrador
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Este script necesita ejecutarse como Administrador
    echo Haga clic derecho en el archivo y seleccione "Ejecutar como administrador"
    pause
    exit /b 1
)

echo PASO 1: Verificando prerrequisitos...
echo.

REM Verificar Python 3.12
set PYTHON_DIR=C:\Python312
if not exist "%PYTHON_DIR%\python.exe" (
    echo ERROR: Python 3.12 no encontrado en %PYTHON_DIR%
    echo.
    echo Por favor, descargue e instale Python 3.12 desde:
    echo https://www.python.org/downloads/windows/
    echo.
    echo IMPORTANTE: Durante la instalación de Python:
    echo - Marque "Add Python to PATH"
    echo - Marque "Install for all users"
    echo - Instale en C:\Python312
    echo.
    pause
    exit /b 1
)

echo ✓ Python 3.12 encontrado

REM Verificar IIS
where /q appcmd >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: IIS no está instalado
    echo.
    echo Ejecutando instalación automática de IIS...
    call configurar_iis.ps1
    if %errorlevel% neq 0 (
        echo ERROR: Falló la instalación de IIS
        echo Por favor, instale IIS manualmente y ejecute este script nuevamente
        pause
        exit /b 1
    )
)

echo ✓ IIS está instalado

REM Verificar URL Rewrite
reg query "HKLM\SOFTWARE\Microsoft\IIS Extensions\URL Rewrite" >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: IIS URL Rewrite Module no está instalado
    echo.
    echo Por favor, descargue e instale desde:
    echo https://www.iis.net/downloads/microsoft/url-rewrite
    echo.
    pause
    exit /b 1
)

echo ✓ URL Rewrite Module instalado

REM Verificar Application Request Routing
reg query "HKLM\SOFTWARE\Microsoft\IIS Extensions\Application Request Routing" >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: IIS Application Request Routing no está instalado
    echo.
    echo Por favor, descargue e instale desde:
    echo https://www.iis.net/downloads/microsoft/application-request-routing
    echo.
    pause
    exit /b 1
)

echo ✓ Application Request Routing instalado

REM Verificar PostgreSQL
where /q psql >nul 2>&1
if %errorlevel% neq 0 (
    echo ADVERTENCIA: PostgreSQL no se encuentra en el PATH
    echo Si no tiene PostgreSQL instalado, descárguelo desde:
    echo https://www.postgresql.org/download/windows/
)

echo.
echo PASO 2: Instalando backend DINQR...
echo.

REM Ejecutar instalación del backend
call instalar_whl_windows.bat
if %errorlevel% neq 0 (
    echo ERROR: Falló la instalación del backend
    pause
    exit /b 1
)

echo.
echo PASO 3: Configurando IIS...
echo.

REM Configurar IIS
call configurar_iis_proxy.bat
if %errorlevel% neq 0 (
    echo ERROR: Falló la configuración de IIS
    pause
    exit /b 1
)

echo.
echo PASO 4: Configurando base de datos...
echo.

set APP_DIR=C:\inetpub\dinqr

REM Copiar configuración de ejemplo
if not exist "%APP_DIR%\.env" (
    if exist "env-production-template" (
        echo Copiando plantilla de configuración...
        copy "env-production-template" "%APP_DIR%\.env"
        echo.
        echo IMPORTANTE: Edite el archivo %APP_DIR%\.env y configure:
        echo - DATABASE_URL con sus credenciales de PostgreSQL
        echo - SECRET_KEY con una clave única y segura
        echo - JWT_SECRET_KEY con una clave JWT única
        echo - Otras configuraciones según su entorno
        echo.
    )
)

echo PASO 5: Iniciando servicios...
echo.

REM Iniciar servicio DINQR
echo Iniciando servicio DINQR Backend...
sc start DINQR_Backend
if %errorlevel% neq 0 (
    echo ADVERTENCIA: No se pudo iniciar el servicio automáticamente
    echo Puede iniciarlo manualmente después de configurar .env
)

REM Verificar que IIS esté ejecutándose
echo Verificando estado de IIS...
sc query w3svc | find "RUNNING" >nul
if %errorlevel% neq 0 (
    echo Iniciando IIS...
    net start w3svc
)

echo.
echo ================================================
echo DESPLIEGUE COMPLETADO
echo ================================================
echo.
echo ESTADO DE LA INSTALACIÓN:
echo ✓ Backend DINQR instalado en: C:\inetpub\dinqr
echo ✓ Servicio Windows configurado: DINQR_Backend
echo ✓ IIS configurado como proxy reverso
echo ✓ Sitio web disponible en: http://localhost/
echo.
echo TAREAS PENDIENTES:
echo.
echo 1. CONFIGURAR BASE DE DATOS:
echo    - Edite: C:\inetpub\dinqr\.env
echo    - Configure DATABASE_URL con sus credenciales
echo    - Ejecute las migraciones: cd C:\inetpub\dinqr ^&^& python -m flask db upgrade
echo.
echo 2. CONFIGURAR SEGURIDAD:
echo    - Genere SECRET_KEY único: python -c "import secrets; print(secrets.token_hex(32))"
echo    - Genere JWT_SECRET_KEY único
echo    - Configure HTTPS con certificado SSL válido
echo.
echo 3. DESPLEGAR FRONTEND:
echo    - Compile el frontend: npm run build
echo    - Copie dist/* a: C:\inetpub\wwwroot\dinqr\frontend\
echo.
echo 4. VERIFICAR FUNCIONAMIENTO:
echo    - Reinicie el servicio: sc stop DINQR_Backend ^&^& sc start DINQR_Backend
echo    - Acceda a: http://localhost/frontend/
echo    - Verifique API: http://localhost/api/health
echo.
echo 5. CONFIGURACIÓN ADICIONAL:
echo    - Configure firewall para bloquear puerto 5000 desde exterior
echo    - Configure backup automático de base de datos
echo    - Configure monitoreo de logs
echo.
echo ARCHIVOS IMPORTANTES:
echo - Configuración: C:\inetpub\dinqr\.env
echo - Logs: C:\inetpub\dinqr\logs\
echo - Servicio: DINQR_Backend
echo - IIS Site: DINQR
echo.
echo Para soporte adicional, consulte la documentación en:
echo deployment-scripts/README.md
echo.
pause
