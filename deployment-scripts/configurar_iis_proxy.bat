@echo off
echo ================================================
echo DINQR - Configurador de IIS para Proxy Reverso
echo ================================================
echo.

REM Verificar privilegios de administrador
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Este script necesita ejecutarse como Administrador
    echo Haga clic derecho en el archivo y seleccione "Ejecutar como administrador"
    pause
    exit /b 1
)

REM Variables de configuración
set SITE_NAME=DINQR
set APP_POOL_NAME=DINQR_AppPool
set SITE_PATH=C:\inetpub\wwwroot\dinqr
set BACKEND_URL=http://127.0.0.1:5000
set FRONTEND_PATH=C:\inetpub\wwwroot\dinqr\frontend

echo Configurando IIS para DINQR...
echo.

REM Verificar que IIS esté instalado
where /q appcmd
if %errorlevel% neq 0 (
    echo ERROR: IIS no está instalado o no está en el PATH
    echo Por favor, instale IIS con las características necesarias
    echo Ejecute primero: configurar_iis.ps1
    pause
    exit /b 1
)

REM Verificar que URL Rewrite esté instalado
reg query "HKLM\SOFTWARE\Microsoft\IIS Extensions\URL Rewrite" >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: IIS URL Rewrite Module no está instalado
    echo Descárguelo desde: https://www.iis.net/downloads/microsoft/url-rewrite
    pause
    exit /b 1
)

REM Verificar que Application Request Routing esté instalado
reg query "HKLM\SOFTWARE\Microsoft\IIS Extensions\Application Request Routing" >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: IIS Application Request Routing no está instalado
    echo Descárguelo desde: https://www.iis.net/downloads/microsoft/application-request-routing
    pause
    exit /b 1
)

REM Crear directorios
echo Creando directorios del sitio web...
if not exist "%SITE_PATH%" mkdir "%SITE_PATH%"
if not exist "%FRONTEND_PATH%" mkdir "%FRONTEND_PATH%"

REM Crear Application Pool
echo Creando Application Pool %APP_POOL_NAME%...
%windir%\system32\inetsrv\appcmd delete apppool "%APP_POOL_NAME%" >nul 2>&1
%windir%\system32\inetsrv\appcmd add apppool /name:"%APP_POOL_NAME%" /managedRuntimeVersion:"" /processModel.identityType:ApplicationPoolIdentity

REM Configurar Application Pool
%windir%\system32\inetsrv\appcmd set apppool "%APP_POOL_NAME%" /recycling.periodicRestart.time:00:00:00
%windir%\system32\inetsrv\appcmd set apppool "%APP_POOL_NAME%" /processModel.idleTimeout:00:00:00
%windir%\system32\inetsrv\appcmd set apppool "%APP_POOL_NAME%" /failure.rapidFailProtection:false

REM Eliminar sitio web existente si existe
echo Configurando sitio web %SITE_NAME%...
%windir%\system32\inetsrv\appcmd delete site "%SITE_NAME%" >nul 2>&1

REM Crear sitio web
%windir%\system32\inetsrv\appcmd add site /name:"%SITE_NAME%" /physicalPath:"%SITE_PATH%" /bindings:http/*:80:

REM Asignar Application Pool al sitio
%windir%\system32\inetsrv\appcmd set app "%SITE_NAME%/" /applicationPool:"%APP_POOL_NAME%"

REM Crear aplicación virtual para el frontend
%windir%\system32\inetsrv\appcmd add app /site.name:"%SITE_NAME%" /path:"/frontend" /physicalPath:"%FRONTEND_PATH%"

REM Crear web.config para el sitio principal (proxy reverso para API)
echo Creando configuración de proxy reverso...
(
echo ^<?xml version="1.0" encoding="UTF-8"?^>
echo ^<configuration^>
echo     ^<system.webServer^>
echo         ^<rewrite^>
echo             ^<rules^>
echo                 ^<rule name="API Proxy" stopProcessing="true"^>
echo                     ^<match url="^api/(.*)$" /^>
echo                     ^<action type="Rewrite" url="%BACKEND_URL%/api/{R:1}" /^>
echo                 ^</rule^>
echo                 ^<rule name="Admin Proxy" stopProcessing="true"^>
echo                     ^<match url="^admin/(.*)$" /^>
echo                     ^<action type="Rewrite" url="%BACKEND_URL%/admin/{R:1}" /^>
echo                 ^</rule^>
echo                 ^<rule name="Auth Proxy" stopProcessing="true"^>
echo                     ^<match url="^auth/(.*)$" /^>
echo                     ^<action type="Rewrite" url="%BACKEND_URL%/auth/{R:1}" /^>
echo                 ^</rule^>
echo                 ^<rule name="Uploads Proxy" stopProcessing="true"^>
echo                     ^<match url="^uploads/(.*)$" /^>
echo                     ^<action type="Rewrite" url="%BACKEND_URL%/uploads/{R:1}" /^>
echo                 ^</rule^>
echo                 ^<rule name="Static Proxy" stopProcessing="true"^>
echo                     ^<match url="^static/(.*)$" /^>
echo                     ^<action type="Rewrite" url="%BACKEND_URL%/static/{R:1}" /^>
echo                 ^</rule^>
echo                 ^<rule name="Frontend Redirect" stopProcessing="true"^>
echo                     ^<match url="^$" /^>
echo                     ^<action type="Redirect" url="/frontend/" redirectType="Found" /^>
echo                 ^</rule^>
echo             ^</rules^>
echo         ^</rewrite^>
echo         ^<defaultDocument^>
echo             ^<files^>
echo                 ^<clear /^>
echo                 ^<add value="index.html" /^>
echo             ^</files^>
echo         ^</defaultDocument^>
echo         ^<httpErrors errorMode="Custom" defaultResponseMode="ExecuteURL"^>
echo             ^<remove statusCode="404" subStatusCode="-1" /^>
echo             ^<error statusCode="404" path="/frontend/index.html" responseMode="ExecuteURL" /^>
echo         ^</httpErrors^>
echo     ^</system.webServer^>
echo ^</configuration^>
) > "%SITE_PATH%\web.config"

REM Crear web.config para el frontend (SPA routing)
echo Creando configuración para frontend SPA...
(
echo ^<?xml version="1.0" encoding="UTF-8"?^>
echo ^<configuration^>
echo     ^<system.webServer^>
echo         ^<rewrite^>
echo             ^<rules^>
echo                 ^<rule name="SPA Routes" stopProcessing="true"^>
echo                     ^<match url=".*" /^>
echo                     ^<conditions logicalGrouping="MatchAll"^>
echo                         ^<add input="{REQUEST_FILENAME}" matchType="IsFile" negate="true" /^>
echo                         ^<add input="{REQUEST_FILENAME}" matchType="IsDirectory" negate="true" /^>
echo                     ^</conditions^>
echo                     ^<action type="Rewrite" url="/index.html" /^>
echo                 ^</rule^>
echo             ^</rules^>
echo         ^</rewrite^>
echo         ^<staticContent^>
echo             ^<mimeMap fileExtension=".js" mimeType="application/javascript" /^>
echo             ^<mimeMap fileExtension=".css" mimeType="text/css" /^>
echo             ^<mimeMap fileExtension=".json" mimeType="application/json" /^>
echo             ^<mimeMap fileExtension=".woff" mimeType="font/woff" /^>
echo             ^<mimeMap fileExtension=".woff2" mimeType="font/woff2" /^>
echo         ^</staticContent^>
echo         ^<defaultDocument^>
echo             ^<files^>
echo                 ^<clear /^>
echo                 ^<add value="index.html" /^>
echo             ^</files^>
echo         ^</defaultDocument^>
echo     ^</system.webServer^>
echo ^</configuration^>
) > "%FRONTEND_PATH%\web.config"

REM Configurar permisos
echo Configurando permisos...
icacls "%SITE_PATH%" /grant "IIS_IUSRS:(OI)(CI)RX" /T
icacls "%SITE_PATH%" /grant "IUSR:(OI)(CI)RX" /T

REM Habilitar proxy en Application Request Routing
echo Habilitando proxy en Application Request Routing...
%windir%\system32\inetsrv\appcmd set config -section:system.webServer/proxy /enabled:"True" /commit:apphost

REM Reiniciar IIS
echo Reiniciando IIS...
iisreset

echo.
echo ================================================
echo CONFIGURACIÓN DE IIS COMPLETADA EXITOSAMENTE
echo ================================================
echo.
echo Sitio web: %SITE_NAME%
echo Application Pool: %APP_POOL_NAME%
echo Ruta física: %SITE_PATH%
echo URL del sitio: http://localhost/
echo URL del frontend: http://localhost/frontend/
echo URL de la API: http://localhost/api/
echo.
echo PRÓXIMOS PASOS:
echo 1. Copie los archivos del frontend compilado a: %FRONTEND_PATH%
echo 2. Asegúrese de que el servicio DINQR_Backend esté ejecutándose
echo 3. Pruebe el acceso desde un navegador
echo.
echo COMANDOS ÚTILES:
echo   Ver sitios: appcmd list sites
echo   Ver apps: appcmd list apps
echo   Ver app pools: appcmd list apppools
echo   Reiniciar IIS: iisreset
echo.
pause
