@echo off
echo ====================================
echo   CONFIGURANDO AMBIENTE DINQR
echo ====================================

:: Configurar colores para Windows
color 0E

:: Obtener directorio actual
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..
set BACKEND_DIR=%PROJECT_ROOT%\backend

echo [INFO] Configurando variables de entorno para DINQR...
echo [INFO] Proyecto: %PROJECT_ROOT%

echo.
echo ====================================
echo   FASE 1: CONFIGURACION BACKEND
echo ====================================

echo [PASO 1] Creando archivo .env para el backend...
set ENV_FILE=%BACKEND_DIR%\.env

if exist "%ENV_FILE%" (
    echo [INFO] Archivo .env existente encontrado
    echo [PREGUNTA] ¿Deseas sobreescribirlo? (S/N)
    set /p OVERWRITE="Respuesta: "
    if /i not "%OVERWRITE%"=="S" (
        echo [INFO] Manteniendo archivo .env existente
        goto :frontend_config
    )
    echo [INFO] Creando backup del .env existente...
    copy "%ENV_FILE%" "%ENV_FILE%.backup.%date:~-4,4%%date:~-10,2%%date:~-7,2%" >nul 2>&1
)

echo [INFO] Generando nuevo archivo .env...

echo # ===================================== > "%ENV_FILE%"
echo # CONFIGURACION DINQR - BACKEND >> "%ENV_FILE%"
echo # Generado automáticamente por configurar_ambiente.bat >> "%ENV_FILE%"
echo # Fecha: %DATE% %TIME% >> "%ENV_FILE%"
echo # ===================================== >> "%ENV_FILE%"
echo. >> "%ENV_FILE%"

echo # CONFIGURACION GENERAL >> "%ENV_FILE%"
echo FLASK_APP=app.py >> "%ENV_FILE%"
echo FLASK_ENV=production >> "%ENV_FILE%"
echo DEBUG=false >> "%ENV_FILE%"
echo HOST=0.0.0.0 >> "%ENV_FILE%"
echo PORT=5000 >> "%ENV_FILE%"
echo. >> "%ENV_FILE%"

echo # BASE DE DATOS POSTGRESQL (LOCAL) >> "%ENV_FILE%"
echo DATABASE_URL=postgresql://postgres:postgr3s@localhost:5432/localdb >> "%ENV_FILE%"
echo LOCAL_DB_NAME=localdb >> "%ENV_FILE%"
echo LOCAL_DB_USER=postgres >> "%ENV_FILE%"
echo LOCAL_DB_PASSWORD=postgr3s >> "%ENV_FILE%"
echo LOCAL_DB_HOST=localhost >> "%ENV_FILE%"
echo LOCAL_DB_PORT=5432 >> "%ENV_FILE%"
echo. >> "%ENV_FILE%"

echo # BASE DE DATOS SQL SERVER (REMOTA) >> "%ENV_FILE%"
echo # Configurar según tu entorno >> "%ENV_FILE%"
echo DB_SERVER=192.168.253.5 >> "%ENV_FILE%"
echo DB_NAME=empresadb >> "%ENV_FILE%"
echo DB_USERNAME=sa >> "%ENV_FILE%"
echo DB_PASSWORD=Global2020 >> "%ENV_FILE%"
echo. >> "%ENV_FILE%"

echo # CONFIGURACION CORS >> "%ENV_FILE%"
echo CORS_ORIGINS=http://localhost:3000,http://localhost:8080,http://127.0.0.1:8080 >> "%ENV_FILE%"
echo. >> "%ENV_FILE%"

echo # REDIS (OPCIONAL) >> "%ENV_FILE%"
echo REDIS_URL=redis://localhost:6379/0 >> "%ENV_FILE%"
echo. >> "%ENV_FILE%"

echo # LOGGING >> "%ENV_FILE%"
echo LOG_LEVEL=INFO >> "%ENV_FILE%"
echo LOG_FILE=logs/app.log >> "%ENV_FILE%"
echo. >> "%ENV_FILE%"

echo # JWT SEGURIDAD >> "%ENV_FILE%"
echo JWT_SECRET_KEY=%RANDOM%%RANDOM%%RANDOM%%RANDOM% >> "%ENV_FILE%"
echo FLASK_SECRET_KEY=%RANDOM%%RANDOM%%RANDOM%%RANDOM% >> "%ENV_FILE%"
echo. >> "%ENV_FILE%"

echo # CONFIGURACION PRODUCCION >> "%ENV_FILE%"
echo SESSION_COOKIE_SECURE=false >> "%ENV_FILE%"
echo JWT_COOKIE_SECURE=false >> "%ENV_FILE%"
echo ENABLE_HTTPS=false >> "%ENV_FILE%"
echo. >> "%ENV_FILE%"

echo # DIRECTORIOS >> "%ENV_FILE%"
echo UPLOAD_FOLDER=uploads >> "%ENV_FILE%"
echo QR_OUTPUT_FOLDER=static/qr_codes >> "%ENV_FILE%"

echo [OK] Archivo .env creado: %ENV_FILE%

echo.
echo [PASO 2] Configurando variables del sistema Windows...

echo [INFO] Configurando variables de entorno del sistema...

:: Configurar variables principales para el usuario actual
setx DINQR_HOME "%PROJECT_ROOT%" >nul 2>&1
setx DINQR_BACKEND "%BACKEND_DIR%" >nul 2>&1
setx DINQR_ENV "production" >nul 2>&1

echo [OK] Variables de usuario configuradas

echo.
:frontend_config
echo ====================================
echo   FASE 2: CONFIGURACION FRONTEND
echo ====================================

set FRONTEND_DIR=%PROJECT_ROOT%\frontend

echo [PASO 1] Configurando variables para frontend...
set FRONTEND_ENV=%FRONTEND_DIR%\.env.production

echo [INFO] Creando .env.production para frontend...

echo # ===================================== > "%FRONTEND_ENV%"
echo # CONFIGURACION DINQR - FRONTEND >> "%FRONTEND_ENV%"
echo # Generado automáticamente >> "%FRONTEND_ENV%"
echo # ===================================== >> "%FRONTEND_ENV%"
echo. >> "%FRONTEND_ENV%"

echo # API CONFIGURATION >> "%FRONTEND_ENV%"
echo VITE_API_URL=/api >> "%FRONTEND_ENV%"
echo VITE_API_BASE_URL=http://localhost:8080/api >> "%FRONTEND_ENV%"
echo. >> "%FRONTEND_ENV%"

echo # APP CONFIGURATION >> "%FRONTEND_ENV%"
echo VITE_APP_TITLE=DINQR - Sistema de Códigos QR >> "%FRONTEND_ENV%"
echo VITE_APP_VERSION=1.0.0 >> "%FRONTEND_ENV%"
echo VITE_APP_DESCRIPTION=Sistema de generación y gestión de códigos QR >> "%FRONTEND_ENV%"
echo. >> "%FRONTEND_ENV%"

echo # BUILD CONFIGURATION >> "%FRONTEND_ENV%"
echo VITE_BUILD_TARGET=production >> "%FRONTEND_ENV%"
echo VITE_OPTIMIZE=true >> "%FRONTEND_ENV%"

echo [OK] Configuración frontend creada: %FRONTEND_ENV%

echo.
echo [PASO 2] Configurando archivo .env.local para desarrollo...
set FRONTEND_ENV_LOCAL=%FRONTEND_DIR%\.env.local

echo # CONFIGURACION DESARROLLO LOCAL > "%FRONTEND_ENV_LOCAL%"
echo VITE_API_URL=http://localhost:5000 >> "%FRONTEND_ENV_LOCAL%"
echo VITE_API_BASE_URL=http://localhost:5000 >> "%FRONTEND_ENV_LOCAL%"
echo VITE_DEV_MODE=true >> "%FRONTEND_ENV_LOCAL%"

echo [OK] Configuración desarrollo creada: %FRONTEND_ENV_LOCAL%

echo.
echo ====================================
echo   FASE 3: CONFIGURACION IIS
echo ====================================

echo [PASO 1] Creando configuración para IIS...
set IIS_CONFIG_DIR=%SCRIPT_DIR%iis-config
if not exist "%IIS_CONFIG_DIR%" mkdir "%IIS_CONFIG_DIR%"

echo [INFO] Generando web.config para el sitio principal...
set MAIN_WEB_CONFIG=%IIS_CONFIG_DIR%\web.config.main

echo ^<?xml version="1.0" encoding="UTF-8"?^> > "%MAIN_WEB_CONFIG%"
echo ^<configuration^> >> "%MAIN_WEB_CONFIG%"
echo   ^<system.webServer^> >> "%MAIN_WEB_CONFIG%"
echo     ^<rewrite^> >> "%MAIN_WEB_CONFIG%"
echo       ^<rules^> >> "%MAIN_WEB_CONFIG%"
echo         ^<rule name="ReactRouter" stopProcessing="true"^> >> "%MAIN_WEB_CONFIG%"
echo           ^<match url=".*" /^> >> "%MAIN_WEB_CONFIG%"
echo           ^<conditions logicalGrouping="MatchAll"^> >> "%MAIN_WEB_CONFIG%"
echo             ^<add input="{REQUEST_FILENAME}" matchType="IsFile" negate="true" /^> >> "%MAIN_WEB_CONFIG%"
echo             ^<add input="{REQUEST_FILENAME}" matchType="IsDirectory" negate="true" /^> >> "%MAIN_WEB_CONFIG%"
echo             ^<add input="{REQUEST_URI}" pattern="^/api" negate="true" /^> >> "%MAIN_WEB_CONFIG%"
echo           ^</conditions^> >> "%MAIN_WEB_CONFIG%"
echo           ^<action type="Rewrite" url="/" /^> >> "%MAIN_WEB_CONFIG%"
echo         ^</rule^> >> "%MAIN_WEB_CONFIG%"
echo       ^</rules^> >> "%MAIN_WEB_CONFIG%"
echo     ^</rewrite^> >> "%MAIN_WEB_CONFIG%"
echo     ^<staticContent^> >> "%MAIN_WEB_CONFIG%"
echo       ^<mimeMap fileExtension=".json" mimeType="application/json" /^> >> "%MAIN_WEB_CONFIG%"
echo       ^<mimeMap fileExtension=".woff" mimeType="application/font-woff" /^> >> "%MAIN_WEB_CONFIG%"
echo       ^<mimeMap fileExtension=".woff2" mimeType="application/font-woff2" /^> >> "%MAIN_WEB_CONFIG%"
echo     ^</staticContent^> >> "%MAIN_WEB_CONFIG%"
echo   ^</system.webServer^> >> "%MAIN_WEB_CONFIG%"
echo ^</configuration^> >> "%MAIN_WEB_CONFIG%"

echo [OK] web.config principal creado

echo.
echo [PASO 2] Creando configuración para API...
set API_WEB_CONFIG=%IIS_CONFIG_DIR%\web.config.api

echo ^<?xml version="1.0" encoding="UTF-8"?^> > "%API_WEB_CONFIG%"
echo ^<configuration^> >> "%API_WEB_CONFIG%"
echo   ^<system.webServer^> >> "%API_WEB_CONFIG%"
echo     ^<handlers^> >> "%API_WEB_CONFIG%"
echo       ^<add name="Python FastCGI" path="*" verb="*" modules="FastCgiModule" >> "%API_WEB_CONFIG%"
echo            scriptProcessor="C:\inetpub\wwwroot\dinqr\api\venv_production\Scripts\python.exe|C:\inetpub\wwwroot\dinqr\api\wfastcgi.py" >> "%API_WEB_CONFIG%"
echo            resourceType="Unspecified" requireAccess="Script" /^> >> "%API_WEB_CONFIG%"
echo     ^</handlers^> >> "%API_WEB_CONFIG%"
echo   ^</system.webServer^> >> "%API_WEB_CONFIG%"
echo   ^<appSettings^> >> "%API_WEB_CONFIG%"
echo     ^<add key="WSGI_HANDLER" value="wsgi.application" /^> >> "%API_WEB_CONFIG%"
echo     ^<add key="PYTHONPATH" value="C:\inetpub\wwwroot\dinqr\api" /^> >> "%API_WEB_CONFIG%"
echo     ^<add key="FLASK_ENV" value="production" /^> >> "%API_WEB_CONFIG%"
echo   ^</appSettings^> >> "%API_WEB_CONFIG%"
echo ^</configuration^> >> "%API_WEB_CONFIG%"

echo [OK] web.config API creado

echo.
echo ====================================
echo   FASE 4: SCRIPTS DE CONFIGURACION
echo ====================================

echo [PASO 1] Creando script de configuración rápida...
set QUICK_CONFIG=%SCRIPT_DIR%configuracion_rapida.bat

echo @echo off > "%QUICK_CONFIG%"
echo echo Aplicando configuración rápida... >> "%QUICK_CONFIG%"
echo. >> "%QUICK_CONFIG%"
echo REM Configurar variables de entorno >> "%QUICK_CONFIG%"
echo setx DINQR_HOME "%PROJECT_ROOT%" ^>nul 2^>^&1 >> "%QUICK_CONFIG%"
echo setx DINQR_ENV "production" ^>nul 2^>^&1 >> "%QUICK_CONFIG%"
echo. >> "%QUICK_CONFIG%"
echo REM Aplicar configuración a IIS >> "%QUICK_CONFIG%"
echo if exist "C:\inetpub\wwwroot\dinqr" ( >> "%QUICK_CONFIG%"
echo   copy "%MAIN_WEB_CONFIG%" "C:\inetpub\wwwroot\dinqr\web.config" ^>nul 2^>^&1 >> "%QUICK_CONFIG%"
echo   copy "%API_WEB_CONFIG%" "C:\inetpub\wwwroot\dinqr\api\web.config" ^>nul 2^>^&1 >> "%QUICK_CONFIG%"
echo   echo [OK] Configuración aplicada a IIS >> "%QUICK_CONFIG%"
echo ) else ( >> "%QUICK_CONFIG%"
echo   echo [WARNING] Sitio IIS no encontrado >> "%QUICK_CONFIG%"
echo ) >> "%QUICK_CONFIG%"
echo. >> "%QUICK_CONFIG%"
echo echo Configuración rápida completada >> "%QUICK_CONFIG%"
echo pause >> "%QUICK_CONFIG%"

echo [OK] Script de configuración rápida creado

echo.
echo [PASO 2] Creando script de validación de ambiente...
set VALIDATE_ENV=%SCRIPT_DIR%validar_ambiente.bat

echo @echo off > "%VALIDATE_ENV%"
echo echo Validando ambiente DINQR... >> "%VALIDATE_ENV%"
echo echo ========================== >> "%VALIDATE_ENV%"
echo. >> "%VALIDATE_ENV%"
echo echo [BACKEND] >> "%VALIDATE_ENV%"
echo if exist "%BACKEND_DIR%\.env" ( >> "%VALIDATE_ENV%"
echo   echo ✓ .env configurado >> "%VALIDATE_ENV%"
echo ) else ( >> "%VALIDATE_ENV%"
echo   echo ✗ .env no encontrado >> "%VALIDATE_ENV%"
echo ) >> "%VALIDATE_ENV%"
echo. >> "%VALIDATE_ENV%"
echo echo [FRONTEND] >> "%VALIDATE_ENV%"
echo if exist "%FRONTEND_DIR%\.env.production" ( >> "%VALIDATE_ENV%"
echo   echo ✓ .env.production configurado >> "%VALIDATE_ENV%"
echo ) else ( >> "%VALIDATE_ENV%"
echo   echo ✗ .env.production no encontrado >> "%VALIDATE_ENV%"
echo ) >> "%VALIDATE_ENV%"
echo. >> "%VALIDATE_ENV%"
echo echo [VARIABLES DE SISTEMA] >> "%VALIDATE_ENV%"
echo if defined DINQR_HOME ( >> "%VALIDATE_ENV%"
echo   echo ✓ DINQR_HOME: %%DINQR_HOME%% >> "%VALIDATE_ENV%"
echo ) else ( >> "%VALIDATE_ENV%"
echo   echo ✗ DINQR_HOME no configurada >> "%VALIDATE_ENV%"
echo ) >> "%VALIDATE_ENV%"
echo. >> "%VALIDATE_ENV%"
echo echo [BASE DE DATOS] >> "%VALIDATE_ENV%"
echo psql -U postgres -h localhost -p 5432 -d localdb -c "SELECT 1;" ^>nul 2^>^&1 >> "%VALIDATE_ENV%"
echo if errorlevel 1 ( >> "%VALIDATE_ENV%"
echo   echo ✗ PostgreSQL no accesible >> "%VALIDATE_ENV%"
echo ) else ( >> "%VALIDATE_ENV%"
echo   echo ✓ PostgreSQL funcionando >> "%VALIDATE_ENV%"
echo ) >> "%VALIDATE_ENV%"
echo. >> "%VALIDATE_ENV%"
echo pause >> "%VALIDATE_ENV%"

echo [OK] Script de validación creado

echo.
echo ====================================
echo   FASE 5: DOCUMENTACION
echo ====================================

echo [PASO 1] Generando documentación de configuración...
set CONFIG_DOC=%SCRIPT_DIR%configuracion.md

echo # Configuración de Ambiente DINQR > "%CONFIG_DOC%"
echo ================================ >> "%CONFIG_DOC%"
echo. >> "%CONFIG_DOC%"
echo Generado: %DATE% %TIME% >> "%CONFIG_DOC%"
echo. >> "%CONFIG_DOC%"
echo ## Archivos de Configuración >> "%CONFIG_DOC%"
echo. >> "%CONFIG_DOC%"
echo ### Backend >> "%CONFIG_DOC%"
echo - `.env`: %BACKEND_DIR%\.env >> "%CONFIG_DOC%"
echo - Configuración: PostgreSQL local + SQL Server remoto >> "%CONFIG_DOC%"
echo - Puerto: 5000 >> "%CONFIG_DOC%"
echo. >> "%CONFIG_DOC%"
echo ### Frontend >> "%CONFIG_DOC%"
echo - `.env.production`: %FRONTEND_DIR%\.env.production >> "%CONFIG_DOC%"
echo - `.env.local`: %FRONTEND_DIR%\.env.local >> "%CONFIG_DOC%"
echo - API URL: /api (producción), http://localhost:5000 (desarrollo) >> "%CONFIG_DOC%"
echo. >> "%CONFIG_DOC%"
echo ### IIS >> "%CONFIG_DOC%"
echo - web.config principal: %MAIN_WEB_CONFIG% >> "%CONFIG_DOC%"
echo - web.config API: %API_WEB_CONFIG% >> "%CONFIG_DOC%"
echo - Puerto: 8080 >> "%CONFIG_DOC%"
echo. >> "%CONFIG_DOC%"
echo ## Variables de Entorno del Sistema >> "%CONFIG_DOC%"
echo. >> "%CONFIG_DOC%"
echo - `DINQR_HOME`: %PROJECT_ROOT% >> "%CONFIG_DOC%"
echo - `DINQR_BACKEND`: %BACKEND_DIR% >> "%CONFIG_DOC%"
echo - `DINQR_ENV`: production >> "%CONFIG_DOC%"
echo. >> "%CONFIG_DOC%"
echo ## Comandos Útiles >> "%CONFIG_DOC%"
echo. >> "%CONFIG_DOC%"
echo - Validar ambiente: `validar_ambiente.bat` >> "%CONFIG_DOC%"
echo - Configuración rápida: `configuracion_rapida.bat` >> "%CONFIG_DOC%"
echo - Ver variables: `echo %%DINQR_HOME%%` >> "%CONFIG_DOC%"

echo [OK] Documentación generada: %CONFIG_DOC%

echo.
echo ====================================
echo   CONFIGURACION COMPLETADA
echo ====================================
echo.
echo [RESUMEN DE CONFIGURACION]
echo ✓ Backend .env: Configurado
echo ✓ Frontend .env: Configurado  
echo ✓ Variables sistema: Configuradas
echo ✓ web.config IIS: Preparados
echo ✓ Scripts utilidad: Creados
echo ✓ Documentación: Generada
echo.
echo [ARCHIVOS CREADOS]
echo Backend:
echo   %BACKEND_DIR%\.env
echo.
echo Frontend:
echo   %FRONTEND_DIR%\.env.production
echo   %FRONTEND_DIR%\.env.local
echo.
echo IIS:
echo   %MAIN_WEB_CONFIG%
echo   %API_WEB_CONFIG%
echo.
echo Utilidades:
echo   %QUICK_CONFIG%
echo   %VALIDATE_ENV%
echo   %CONFIG_DOC%
echo.
echo [VARIABLES DE ENTORNO]
echo DINQR_HOME: %PROJECT_ROOT%
echo DINQR_BACKEND: %BACKEND_DIR%
echo DINQR_ENV: production
echo.
echo [PROXIMOS PASOS]
echo 1. Validar: validar_ambiente.bat
echo 2. Revisar configuración: notepad %BACKEND_DIR%\.env
echo 3. Compilar proyecto: compilar_todo.bat
echo 4. Desplegar: desplegar_iis.bat
echo.
echo [NOTA IMPORTANTE]
echo Revisa y ajusta las configuraciones según tu entorno específico,
echo especialmente las conexiones de base de datos y URLs.
echo.

:: Mantener ventana abierta
echo Presiona cualquier tecla para continuar...
pause >nul
