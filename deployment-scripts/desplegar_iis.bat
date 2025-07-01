@echo off
echo ====================================
echo   DESPLEGANDO DINQR EN IIS
echo ====================================

:: Verificar permisos de administrador
net session >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Este script debe ejecutarse como Administrador
    echo [INFO] Click derecho en el archivo y selecciona "Ejecutar como administrador"
    pause
    exit /b 1
)

:: Configurar colores para Windows
color 0C

:: Obtener directorio actual
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..
set BACKEND_DIR=%PROJECT_ROOT%\backend
set FRONTEND_DIR=%PROJECT_ROOT%\frontend
set IIS_ROOT=C:\inetpub\wwwroot
set SITE_DIR=%IIS_ROOT%\dinqr

echo [INFO] Iniciando despliegue en IIS...
echo [INFO] Directorio del proyecto: %PROJECT_ROOT%
echo [INFO] Directorio IIS: %SITE_DIR%

echo.
echo ====================================
echo   FASE 1: VERIFICACIONES PREVIAS
echo ====================================

echo [PASO 1] Verificando IIS...
%windir%\system32\inetsrv\appcmd.exe list site >nul 2>&1
if errorlevel 1 (
    echo [ERROR] IIS no está instalado o no está funcionando
    echo [INFO] Instala IIS desde "Programas y características" ^> "Activar o desactivar características de Windows"
    pause
    exit /b 1
)

echo [OK] IIS está disponible

echo.
echo [PASO 2] Verificando compilaciones...
if not exist "%BACKEND_DIR%\wsgi.py" (
    echo [ERROR] Backend no compilado. Ejecuta primero: compilar_backend.bat
    pause
    exit /b 1
)

if not exist "%FRONTEND_DIR%\dist\index.html" (
    echo [ERROR] Frontend no compilado. Ejecuta primero: compilar_frontend.bat
    pause
    exit /b 1
)

echo [OK] Compilaciones verificadas

echo.
echo [PASO 3] Verificando Python para IIS...
where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no está en el PATH del sistema
    pause
    exit /b 1
)

echo [OK] Python disponible para IIS

echo.
echo ====================================
echo   FASE 2: CONFIGURACION DE IIS
echo ====================================

echo [PASO 1] Configurando características de IIS...
echo [INFO] Habilitando CGI y FastCGI...

:: Habilitar CGI
dism /online /enable-feature /featurename:IIS-CGI /all >nul 2>&1
if errorlevel 1 (
    echo [WARNING] No se pudo habilitar CGI automáticamente
)

:: Habilitar características adicionales necesarias
dism /online /enable-feature /featurename:IIS-HttpRedirect /all >nul 2>&1
dism /online /enable-feature /featurename:IIS-HttpLogging /all >nul 2>&1
dism /online /enable-feature /featurename:IIS-RequestFiltering /all >nul 2>&1

echo [OK] Características de IIS configuradas

echo.
echo [PASO 2] Creando estructura de directorios...
if exist "%SITE_DIR%" (
    echo [INFO] Eliminando instalación anterior...
    rmdir /s /q "%SITE_DIR%"
)

mkdir "%SITE_DIR%"
mkdir "%SITE_DIR%\api"
mkdir "%SITE_DIR%\logs"
mkdir "%SITE_DIR%\uploads"

echo [OK] Estructura de directorios creada

echo.
echo [PASO 3] Copiando archivos del frontend...
echo [INFO] Copiando archivos compilados del frontend...
xcopy /E /I /Y "%FRONTEND_DIR%\dist\*" "%SITE_DIR%\"
if errorlevel 1 (
    echo [ERROR] Error al copiar archivos del frontend
    pause
    exit /b 1
)

echo [OK] Frontend desplegado

echo.
echo [PASO 4] Configurando backend...
echo [INFO] Copiando archivos del backend...
xcopy /E /I /Y "%BACKEND_DIR%\*" "%SITE_DIR%\api\"
if errorlevel 1 (
    echo [ERROR] Error al copiar archivos del backend
    pause
    exit /b 1
)

:: Excluir archivos innecesarios del backend en producción
if exist "%SITE_DIR%\api\venv" rmdir /s /q "%SITE_DIR%\api\venv"
if exist "%SITE_DIR%\api\__pycache__" rmdir /s /q "%SITE_DIR%\api\__pycache__"

echo [OK] Backend copiado

echo.
echo ====================================
echo   FASE 3: CONFIGURACION DE PYTHON
echo ====================================

echo [PASO 1] Configurando entorno virtual para producción...
cd /d "%SITE_DIR%\api"

python -m venv venv_production
if errorlevel 1 (
    echo [ERROR] No se pudo crear entorno virtual de producción
    pause
    exit /b 1
)

call venv_production\Scripts\activate.bat
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Error al instalar dependencias en producción
    pause
    exit /b 1
)

call venv_production\Scripts\deactivate.bat

echo [OK] Entorno virtual de producción configurado

echo.
echo [PASO 2] Configurando archivo web.config para API...
echo [INFO] Creando web.config para FastCGI...

echo ^<?xml version="1.0" encoding="UTF-8"?^> > "%SITE_DIR%\api\web.config"
echo ^<configuration^> >> "%SITE_DIR%\api\web.config"
echo   ^<system.webServer^> >> "%SITE_DIR%\api\web.config"
echo     ^<handlers^> >> "%SITE_DIR%\api\web.config"
echo       ^<add name="Python FastCGI" path="*" verb="*" modules="FastCgiModule" >> "%SITE_DIR%\api\web.config"
echo            scriptProcessor="%SITE_DIR%\api\venv_production\Scripts\python.exe|%SITE_DIR%\api\wfastcgi.py" >> "%SITE_DIR%\api\web.config"
echo            resourceType="Unspecified" requireAccess="Script" /^> >> "%SITE_DIR%\api\web.config"
echo     ^</handlers^> >> "%SITE_DIR%\api\web.config"
echo     ^<fastCgi^> >> "%SITE_DIR%\api\web.config"
echo       ^<application fullPath="%SITE_DIR%\api\venv_production\Scripts\python.exe" >> "%SITE_DIR%\api\web.config"
echo                    arguments="%SITE_DIR%\api\wfastcgi.py" >> "%SITE_DIR%\api\web.config"
echo                    maxInstances="4" idleTimeout="1800" activityTimeout="30" >> "%SITE_DIR%\api\web.config"
echo                    requestTimeout="90" instanceMaxRequests="10000" >> "%SITE_DIR%\api\web.config"
echo                    protocol="NamedPipe" flushNamedPipe="False" /^> >> "%SITE_DIR%\api\web.config"
echo     ^</fastCgi^> >> "%SITE_DIR%\api\web.config"
echo   ^</system.webServer^> >> "%SITE_DIR%\api\web.config"
echo   ^<appSettings^> >> "%SITE_DIR%\api\web.config"
echo     ^<add key="WSGI_HANDLER" value="wsgi.application" /^> >> "%SITE_DIR%\api\web.config"
echo     ^<add key="PYTHONPATH" value="%SITE_DIR%\api" /^> >> "%SITE_DIR%\api\web.config"
echo     ^<add key="WSGI_LOG" value="%SITE_DIR%\logs\wfastcgi.log" /^> >> "%SITE_DIR%\api\web.config"
echo   ^</appSettings^> >> "%SITE_DIR%\api\web.config"
echo ^</configuration^> >> "%SITE_DIR%\api\web.config"

echo [OK] web.config para API creado

echo.
echo [PASO 3] Instalando wfastcgi...
call "%SITE_DIR%\api\venv_production\Scripts\activate.bat"
pip install wfastcgi
if errorlevel 1 (
    echo [ERROR] Error al instalar wfastcgi
    pause
    exit /b 1
)

:: Habilitar wfastcgi
wfastcgi-enable
call "%SITE_DIR%\api\venv_production\Scripts\deactivate.bat"

echo [OK] wfastcgi configurado

echo.
echo ====================================
echo   FASE 4: CONFIGURACION DEL SITIO
echo ====================================

echo [PASO 1] Eliminando sitio anterior si existe...
%windir%\system32\inetsrv\appcmd.exe delete site "DINQR" >nul 2>&1

echo [PASO 2] Creando sitio web en IIS...
%windir%\system32\inetsrv\appcmd.exe add site /name:"DINQR" /physicalPath:"%SITE_DIR%" /bindings:http/*:8080:
if errorlevel 1 (
    echo [ERROR] Error al crear sitio en IIS
    pause
    exit /b 1
)

echo [OK] Sitio DINQR creado en puerto 8080

echo.
echo [PASO 3] Configurando aplicación virtual para API...
%windir%\system32\inetsrv\appcmd.exe add app /site.name:"DINQR" /path:/api /physicalPath:"%SITE_DIR%\api"
if errorlevel 1 (
    echo [ERROR] Error al crear aplicación virtual para API
    pause
    exit /b 1
)

echo [OK] Aplicación virtual /api configurada

echo.
echo [PASO 4] Configurando permisos...
echo [INFO] Configurando permisos para IIS_IUSRS...
icacls "%SITE_DIR%" /grant "IIS_IUSRS:(OI)(CI)F" /T >nul 2>&1
icacls "%SITE_DIR%" /grant "IUSR:(OI)(CI)F" /T >nul 2>&1

echo [OK] Permisos configurados

echo.
echo ====================================
echo   FASE 5: CONFIGURACION FINAL
echo ====================================

echo [PASO 1] Configurando variables de entorno del sitio...
%windir%\system32\inetsrv\appcmd.exe set config "DINQR/api" -section:system.webServer/fastCgi /+"[fullPath='%SITE_DIR%\api\venv_production\Scripts\python.exe'].environmentVariables.[name='FLASK_ENV',value='production']" /commit:apphost >nul 2>&1

echo [OK] Variables de entorno configuradas

echo.
echo [PASO 2] Reiniciando IIS...
iisreset >nul 2>&1
if errorlevel 1 (
    echo [WARNING] No se pudo reiniciar IIS automáticamente
    echo [INFO] Reinicia IIS manualmente si es necesario
) else (
    echo [OK] IIS reiniciado
)

echo.
echo [PASO 3] Creando scripts de administración...

:: Script para reiniciar el sitio
echo @echo off > "%SCRIPT_DIR%reiniciar_sitio.bat"
echo echo Reiniciando sitio DINQR... >> "%SCRIPT_DIR%reiniciar_sitio.bat"
echo %windir%\system32\inetsrv\appcmd.exe stop site "DINQR" >> "%SCRIPT_DIR%reiniciar_sitio.bat"
echo timeout /t 2 >> "%SCRIPT_DIR%reiniciar_sitio.bat"
echo %windir%\system32\inetsrv\appcmd.exe start site "DINQR" >> "%SCRIPT_DIR%reiniciar_sitio.bat"
echo echo Sitio reiniciado >> "%SCRIPT_DIR%reiniciar_sitio.bat"

:: Script para ver logs
echo @echo off > "%SCRIPT_DIR%ver_logs.bat"
echo echo Logs de DINQR: >> "%SCRIPT_DIR%ver_logs.bat"
echo echo =================== >> "%SCRIPT_DIR%ver_logs.bat"
echo if exist "%SITE_DIR%\logs\wfastcgi.log" type "%SITE_DIR%\logs\wfastcgi.log" >> "%SCRIPT_DIR%ver_logs.bat"
echo if exist "%SITE_DIR%\api\logs\app.log" type "%SITE_DIR%\api\logs\app.log" >> "%SCRIPT_DIR%ver_logs.bat"
echo pause >> "%SCRIPT_DIR%ver_logs.bat"

echo [OK] Scripts de administración creados

echo.
echo [PASO 4] Verificando despliegue...
echo [INFO] Verificando archivos desplegados...

if not exist "%SITE_DIR%\index.html" (
    echo [ERROR] No se encontró index.html en el sitio
    pause
    exit /b 1
)

if not exist "%SITE_DIR%\api\wsgi.py" (
    echo [ERROR] No se encontró wsgi.py en la API
    pause
    exit /b 1
)

echo [OK] Archivos verificados

echo.
echo ====================================
echo   DESPLIEGUE COMPLETADO
echo ====================================
echo.
echo [RESUMEN DEL DESPLIEGUE]
echo ✓ Sitio web: DINQR
echo ✓ Puerto: 8080
echo ✓ Directorio: %SITE_DIR%
echo ✓ API: /api
echo ✓ Permisos: Configurados
echo ✓ FastCGI: Habilitado
echo.
echo [URLS DE ACCESO]
echo - Frontend: http://localhost:8080
echo - API: http://localhost:8080/api
echo - Documentación: http://localhost:8080/api/apidocs
echo.
echo [ARCHIVOS DE ADMINISTRACION]
echo - Reiniciar sitio: reiniciar_sitio.bat
echo - Ver logs: ver_logs.bat
echo - Logs IIS: %SITE_DIR%\logs\
echo.
echo [PROXIMOS PASOS]
echo 1. Configurar base de datos: migrar_base_datos.bat
echo 2. Verificar acceso: http://localhost:8080
echo 3. Configurar firewall si es necesario
echo 4. Configurar SSL para producción
echo.

:: Crear archivo de información del despliegue
set DEPLOY_INFO=%SCRIPT_DIR%deployment-info.txt
echo DINQR - Información del Despliegue > %DEPLOY_INFO%
echo ===================================== >> %DEPLOY_INFO%
echo. >> %DEPLOY_INFO%
echo Fecha: %DATE% >> %DEPLOY_INFO%
echo Hora: %TIME% >> %DEPLOY_INFO%
echo. >> %DEPLOY_INFO%
echo CONFIGURACION: >> %DEPLOY_INFO%
echo Sitio: DINQR >> %DEPLOY_INFO%
echo Puerto: 8080 >> %DEPLOY_INFO%
echo Directorio: %SITE_DIR% >> %DEPLOY_INFO%
echo Python: %SITE_DIR%\api\venv_production\Scripts\python.exe >> %DEPLOY_INFO%
echo. >> %DEPLOY_INFO%
echo URLS: >> %DEPLOY_INFO%
echo Frontend: http://localhost:8080 >> %DEPLOY_INFO%
echo API: http://localhost:8080/api >> %DEPLOY_INFO%
echo Docs: http://localhost:8080/api/apidocs >> %DEPLOY_INFO%

echo [INFO] Información del despliegue guardada en: %DEPLOY_INFO%
echo.

:: Mantener ventana abierta
echo Presiona cualquier tecla para continuar...
pause >nul
