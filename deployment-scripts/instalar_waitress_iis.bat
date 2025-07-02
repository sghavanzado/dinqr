@echo off
rem ===============================================================================
rem DINQR - Despliegue completo con Waitress + IIS
rem ===============================================================================
rem Este script configura automaticamente DINQR para funcionar con:
rem - Waitress como servidor WSGI
rem - IIS como reverse proxy
rem - Servicio de Windows para ejecucion automatica
rem - Configuracion de SSL/HTTPS
rem - Logs y monitoreo
rem
rem Requisitos previos:
rem - Windows Server 2016+ o Windows 10+ Pro
rem - Python 3.8+ instalado
rem - IIS con ARR (Application Request Routing) instalado
rem - Privilegios de administrador
rem
rem Autor: DINQR Deployment Team
rem Fecha: %date%
rem ===============================================================================

setlocal EnableDelayedExpansion

set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."
set "BACKEND_DIR=%PROJECT_ROOT%\backend"
set "FRONTEND_DIR=%PROJECT_ROOT%\frontend"
set "SERVICE_NAME=DINQRBackend"
set "SITE_NAME=DINQR"
set "APP_POOL_NAME=DINQRAppPool"
set "INSTALL_LOG=%SCRIPT_DIR%\instalacion_waitress.log"

rem Configuracion por defecto
set "DEFAULT_PORT=5000"
set "DEFAULT_DOMAIN=dinqr.local"
set "DEFAULT_SSL_PORT=443"
set "BACKEND_URL=http://localhost:%DEFAULT_PORT%"

echo ===============================================================================
echo DINQR - INSTALACION CON WAITRESS + IIS
echo ===============================================================================
echo.
echo Este script configurara DINQR con la siguiente arquitectura:
echo   Cliente ^<--^> IIS (443/80) ^<--^> Waitress (%DEFAULT_PORT%) ^<--^> Flask App
echo.
echo Presione cualquier tecla para continuar o Ctrl+C para cancelar...
pause >nul

rem Crear archivo de log
echo [%date% %time%] Iniciando instalacion DINQR con Waitress + IIS > "%INSTALL_LOG%"

rem Verificar prerequisitos
call :check_prerequisites
if errorlevel 1 goto :error

rem Configurar parametros
call :configure_parameters

rem Instalar dependencias de Python
call :install_python_dependencies
if errorlevel 1 goto :error

rem Configurar el servicio de Windows
call :setup_windows_service
if errorlevel 1 goto :error

rem Configurar IIS
call :setup_iis
if errorlevel 1 goto :error

rem Configurar SSL (opcional)
call :setup_ssl

rem Iniciar servicios
call :start_services
if errorlevel 1 goto :error

rem Verificar instalacion
call :verify_installation

echo.
echo ===============================================================================
echo INSTALACION COMPLETADA EXITOSAMENTE
echo ===============================================================================
echo.
echo Configuracion de DINQR:
echo   Servicio Windows: %SERVICE_NAME%
echo   Puerto Waitress: %WAITRESS_PORT%
echo   Sitio IIS: %SITE_NAME%
echo   Dominio: %DOMAIN_NAME%
echo   SSL: %SSL_ENABLED%
echo.
echo URLs de acceso:
echo   HTTP:  http://%DOMAIN_NAME%
echo   HTTPS: https://%DOMAIN_NAME% (si SSL esta habilitado)
echo   API:   http://%DOMAIN_NAME%/api/v1/
echo.
echo Proximos pasos:
echo 1. Configurar el DNS para apuntar %DOMAIN_NAME% a este servidor
echo 2. Configurar el firewall para permitir puertos 80 y 443
echo 3. Configurar un certificado SSL valido (si no se hizo)
echo 4. Revisar logs en: %BACKEND_DIR%\logs\
echo.
echo Para gestionar el servicio use: servicio_dinqr.bat [start^|stop^|restart^|status]
echo.
goto :end

rem ===============================================================================
rem FUNCIONES
rem ===============================================================================

:check_prerequisites
echo [%date% %time%] Verificando prerequisitos... >> "%INSTALL_LOG%"
echo Verificando prerequisitos del sistema...

rem Verificar privilegios de administrador
net session >nul 2>&1
if errorlevel 1 (
    echo ERROR: Este script debe ejecutarse como administrador.
    echo Por favor, ejecute cmd como administrador y vuelva a intentar.
    echo [%date% %time%] ERROR: Sin privilegios de administrador >> "%INSTALL_LOG%"
    exit /b 1
)
echo   ✓ Privilegios de administrador

rem Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH.
    echo Por favor, instale Python 3.8+ desde https://python.org
    echo [%date% %time%] ERROR: Python no encontrado >> "%INSTALL_LOG%"
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set "PYTHON_VERSION=%%i"
echo   ✓ Python %PYTHON_VERSION%

rem Verificar IIS
%windir%\system32\inetsrv\appcmd.exe list sites >nul 2>&1
if errorlevel 1 (
    echo ERROR: IIS no esta instalado o no esta disponible.
    echo Por favor, instale IIS con las siguientes caracteristicas:
    echo   - IIS Management Console
    echo   - Application Request Routing (ARR)
    echo   - URL Rewrite Module
    echo [%date% %time%] ERROR: IIS no disponible >> "%INSTALL_LOG%"
    exit /b 1
)
echo   ✓ IIS disponible

rem Verificar ARR (Application Request Routing)
%windir%\system32\inetsrv\appcmd.exe list modules | find /i "ApplicationRequestRouting" >nul
if errorlevel 1 (
    echo WARNING: Application Request Routing (ARR) podria no estar instalado.
    echo Se recomienda instalar ARR para mejor funcionalidad de reverse proxy.
    echo [%date% %time%] WARNING: ARR posiblemente no instalado >> "%INSTALL_LOG%"
)

rem Verificar directorios del proyecto
if not exist "%BACKEND_DIR%" (
    echo ERROR: Directorio del backend no encontrado: %BACKEND_DIR%
    echo [%date% %time%] ERROR: Backend directory no encontrado >> "%INSTALL_LOG%"
    exit /b 1
)
echo   ✓ Directorio del backend

if not exist "%FRONTEND_DIR%" (
    echo ERROR: Directorio del frontend no encontrado: %FRONTEND_DIR%
    echo [%date% %time%] ERROR: Frontend directory no encontrado >> "%INSTALL_LOG%"
    exit /b 1
)
echo   ✓ Directorio del frontend

echo [%date% %time%] Prerequisitos verificados exitosamente >> "%INSTALL_LOG%"
exit /b 0

:configure_parameters
echo.
echo Configurando parametros de instalacion...

rem Puerto para Waitress
set /p "WAITRESS_PORT=Puerto para Waitress [%DEFAULT_PORT%]: "
if "%WAITRESS_PORT%"=="" set "WAITRESS_PORT=%DEFAULT_PORT%"

rem Dominio
set /p "DOMAIN_NAME=Nombre de dominio [%DEFAULT_DOMAIN%]: "
if "%DOMAIN_NAME%"=="" set "DOMAIN_NAME=%DEFAULT_DOMAIN%"

rem SSL
set /p "SSL_CHOICE=Configurar SSL/HTTPS? (s/n) [n]: "
if /i "%SSL_CHOICE%"=="s" (
    set "SSL_ENABLED=Si"
    set /p "SSL_CERT_PATH=Ruta del certificado SSL (.pfx): "
    set /p "SSL_CERT_PASSWORD=Password del certificado: "
) else (
    set "SSL_ENABLED=No"
)

rem Actualizar configuracion en .env
echo Actualizando archivo de configuracion...
cd /d "%BACKEND_DIR%"

rem Crear backup del .env actual
if exist ".env" copy ".env" ".env.backup.%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%" >nul

rem Actualizar configuraciones clave
call :update_env_setting "WAITRESS_HOST" "0.0.0.0"
call :update_env_setting "WAITRESS_PORT" "%WAITRESS_PORT%"
call :update_env_setting "FLASK_ENV" "production"
call :update_env_setting "DEBUG" "False"

echo [%date% %time%] Parametros configurados - Puerto: %WAITRESS_PORT%, Dominio: %DOMAIN_NAME%, SSL: %SSL_ENABLED% >> "%INSTALL_LOG%"
exit /b 0

:install_python_dependencies
echo.
echo Instalando dependencias de Python...
cd /d "%BACKEND_DIR%"

rem Actualizar pip
echo   Actualizando pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo ERROR: Fallo la actualizacion de pip
    echo [%date% %time%] ERROR: Pip upgrade fallido >> "%INSTALL_LOG%"
    exit /b 1
)

rem Instalar dependencias
echo   Instalando dependencias del proyecto...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Fallo la instalacion de dependencias
    echo [%date% %time%] ERROR: Instalacion de dependencias fallida >> "%INSTALL_LOG%"
    exit /b 1
)

rem Verificar instalacion de Waitress
python -c "import waitress; print('Waitress version:', waitress.__version__)" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Waitress no se instalo correctamente
    echo [%date% %time%] ERROR: Waitress no instalado >> "%INSTALL_LOG%"
    exit /b 1
)

rem Verificar instalacion de pywin32
python -c "import win32service; print('pywin32 instalado correctamente')" >nul 2>&1
if errorlevel 1 (
    echo ERROR: pywin32 no se instalo correctamente
    echo [%date% %time%] ERROR: pywin32 no instalado >> "%INSTALL_LOG%"
    exit /b 1
)

echo   ✓ Dependencias instaladas correctamente
echo [%date% %time%] Dependencias Python instaladas >> "%INSTALL_LOG%"
exit /b 0

:setup_windows_service
echo.
echo Configurando servicio de Windows...
cd /d "%BACKEND_DIR%"

rem Detener servicio si existe
sc query "%SERVICE_NAME%" >nul 2>&1
if not errorlevel 1 (
    echo   Deteniendo servicio existente...
    python windows_service.py stop >nul 2>&1
    timeout /t 3 >nul
)

rem Instalar/reinstalar servicio
echo   Instalando servicio de Windows...
python windows_service.py install
if errorlevel 1 (
    echo ERROR: Fallo la instalacion del servicio de Windows
    echo [%date% %time%] ERROR: Instalacion servicio Windows fallida >> "%INSTALL_LOG%"
    exit /b 1
)

rem Configurar inicio automatico
echo   Configurando inicio automatico...
sc config "%SERVICE_NAME%" start= auto >nul 2>&1
if errorlevel 1 (
    echo WARNING: No se pudo configurar el inicio automatico del servicio
    echo [%date% %time%] WARNING: Inicio automatico no configurado >> "%INSTALL_LOG%"
)

echo   ✓ Servicio de Windows configurado
echo [%date% %time%] Servicio Windows configurado >> "%INSTALL_LOG%"
exit /b 0

:setup_iis
echo.
echo Configurando IIS...

rem Crear Application Pool
echo   Creando Application Pool...
%windir%\system32\inetsrv\appcmd.exe add apppool /name:"%APP_POOL_NAME%" /managedRuntimeVersion:"" /processModel.identityType:ApplicationPoolIdentity >nul 2>&1
if errorlevel 1 (
    echo   Application Pool ya existe, reconfigurando...
    %windir%\system32\inetsrv\appcmd.exe set apppool "%APP_POOL_NAME%" /managedRuntimeVersion:"" /processModel.identityType:ApplicationPoolIdentity >nul 2>&1
)

rem Detener sitio por defecto si existe
%windir%\system32\inetsrv\appcmd.exe stop site "Default Web Site" >nul 2>&1

rem Crear/actualizar sitio web
echo   Configurando sitio web...
%windir%\system32\inetsrv\appcmd.exe list site "%SITE_NAME%" >nul 2>&1
if errorlevel 1 (
    %windir%\system32\inetsrv\appcmd.exe add site /name:"%SITE_NAME%" /physicalPath:"%FRONTEND_DIR%\dist" /bindings:http/*:80:%DOMAIN_NAME%
) else (
    %windir%\system32\inetsrv\appcmd.exe set site "%SITE_NAME%" /physicalPath:"%FRONTEND_DIR%\dist"
)

if errorlevel 1 (
    echo ERROR: Fallo la configuracion del sitio web en IIS
    echo [%date% %time%] ERROR: Configuracion sitio IIS fallida >> "%INSTALL_LOG%"
    exit /b 1
)

rem Asignar Application Pool al sitio
%windir%\system32\inetsrv\appcmd.exe set app "%SITE_NAME%/" /applicationPool:"%APP_POOL_NAME%" >nul 2>&1

rem Copiar web.config al directorio web
echo   Copiando configuracion web.config...
if exist "%BACKEND_DIR%\web.config" (
    copy "%BACKEND_DIR%\web.config" "%FRONTEND_DIR%\dist\web.config" >nul 2>&1
    if errorlevel 1 (
        echo WARNING: No se pudo copiar web.config
        echo [%date% %time%] WARNING: web.config no copiado >> "%INSTALL_LOG%"
    )
) else (
    echo WARNING: web.config no encontrado en el backend
    echo [%date% %time%] WARNING: web.config no encontrado >> "%INSTALL_LOG%"
)

rem Configurar permisos para logs
echo   Configurando permisos para logs...
if not exist "%BACKEND_DIR%\logs" mkdir "%BACKEND_DIR%\logs"
icacls "%BACKEND_DIR%\logs" /grant "IIS_IUSRS:(OI)(CI)F" /T >nul 2>&1

echo   ✓ IIS configurado correctamente
echo [%date% %time%] IIS configurado >> "%INSTALL_LOG%"
exit /b 0

:setup_ssl
if not "%SSL_ENABLED%"=="Si" goto :skip_ssl

echo.
echo Configurando SSL...

if "%SSL_CERT_PATH%"=="" (
    echo   Generando certificado autofirmado para desarrollo...
    powershell -Command "New-SelfSignedCertificate -DnsName '%DOMAIN_NAME%' -CertStoreLocation Cert:\LocalMachine\My -KeyLength 2048 -KeyAlgorithm RSA -HashAlgorithm SHA256 -KeyUsage KeyEncipherment,DigitalSignature -Type SSLServerAuthentication" >nul 2>&1
    if not errorlevel 1 (
        echo   ✓ Certificado autofirmado creado
        echo [%date% %time%] Certificado autofirmado creado >> "%INSTALL_LOG%"
    ) else (
        echo   WARNING: No se pudo crear certificado autofirmado
        echo [%date% %time%] WARNING: Certificado autofirmado fallido >> "%INSTALL_LOG%"
    )
) else (
    echo   Importando certificado SSL...
    certlm.msc /s "%SSL_CERT_PATH%" >nul 2>&1
    if not errorlevel 1 (
        echo   ✓ Certificado SSL importado
        echo [%date% %time%] Certificado SSL importado >> "%INSTALL_LOG%"
    ) else (
        echo   WARNING: No se pudo importar el certificado SSL
        echo [%date% %time%] WARNING: Importacion SSL fallida >> "%INSTALL_LOG%"
    )
)

rem Configurar binding HTTPS en IIS
echo   Configurando HTTPS binding...
%windir%\system32\inetsrv\appcmd.exe set site "%SITE_NAME%" /+bindings.[protocol='https',bindingInformation='*:443:%DOMAIN_NAME%'] >nul 2>&1

:skip_ssl
exit /b 0

:start_services
echo.
echo Iniciando servicios...

rem Iniciar servicio de Windows DINQR
echo   Iniciando servicio DINQR...
cd /d "%BACKEND_DIR%"
python windows_service.py start
if errorlevel 1 (
    echo ERROR: Fallo el inicio del servicio DINQR
    echo [%date% %time%] ERROR: Inicio servicio DINQR fallido >> "%INSTALL_LOG%"
    exit /b 1
)

rem Esperar a que el servicio inicie
echo   Esperando que el servicio inicie completamente...
timeout /t 10 >nul

rem Verificar que el servicio este corriendo
sc query "%SERVICE_NAME%" | find "RUNNING" >nul
if errorlevel 1 (
    echo ERROR: El servicio DINQR no esta ejecutandose
    echo [%date% %time%] ERROR: Servicio DINQR no corriendo >> "%INSTALL_LOG%"
    exit /b 1
)

rem Iniciar sitio web en IIS
echo   Iniciando sitio web en IIS...
%windir%\system32\inetsrv\appcmd.exe start site "%SITE_NAME%" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Fallo el inicio del sitio web en IIS
    echo [%date% %time%] ERROR: Inicio sitio IIS fallido >> "%INSTALL_LOG%"
    exit /b 1
)

echo   ✓ Servicios iniciados correctamente
echo [%date% %time%] Servicios iniciados >> "%INSTALL_LOG%"
exit /b 0

:verify_installation
echo.
echo Verificando instalacion...

rem Verificar que Waitress responde
echo   Verificando backend (Waitress)...
curl -s http://localhost:%WAITRESS_PORT%/api/v1/health >nul 2>&1
if errorlevel 1 (
    echo   WARNING: Backend no responde en puerto %WAITRESS_PORT%
    echo [%date% %time%] WARNING: Backend no responde >> "%INSTALL_LOG%"
) else (
    echo   ✓ Backend responde correctamente
)

rem Verificar que IIS responde
echo   Verificando frontend (IIS)...
curl -s -I http://localhost/ | find "200" >nul 2>&1
if errorlevel 1 (
    echo   WARNING: Frontend no responde via IIS
    echo [%date% %time%] WARNING: Frontend no responde >> "%INSTALL_LOG%"
) else (
    echo   ✓ Frontend responde correctamente
)

rem Verificar logs
echo   Verificando logs...
if exist "%BACKEND_DIR%\logs\app.log" (
    echo   ✓ Log de aplicacion creado
) else (
    echo   WARNING: Log de aplicacion no encontrado
)

echo [%date% %time%] Verificacion completada >> "%INSTALL_LOG%"
exit /b 0

:update_env_setting
rem Funcion para actualizar una configuracion en .env
rem %1 = clave, %2 = valor
set "key=%~1"
set "value=%~2"
set "temp_file=%temp%\env_temp_%random%.txt"

if exist ".env" (
    findstr /v /b "%key%=" ".env" > "%temp_file%"
    move "%temp_file%" ".env" >nul 2>&1
)

echo %key%=%value% >> ".env"
exit /b 0

:error
echo.
echo ===============================================================================
echo ERROR EN LA INSTALACION
echo ===============================================================================
echo.
echo La instalacion no se completo exitosamente.
echo.
echo Para solucionar problemas:
echo 1. Revise el log de instalacion: %INSTALL_LOG%
echo 2. Verifique que tiene privilegios de administrador
echo 3. Asegurese de que IIS y Python esten instalados correctamente
echo 4. Revise los logs del backend: %BACKEND_DIR%\logs\
echo.
echo Si necesita desinstalar parcialmente:
echo 1. Para remover el servicio: servicio_dinqr.bat remove
echo 2. Para remover el sitio IIS: appcmd delete site "%SITE_NAME%"
echo 3. Para remover el App Pool: appcmd delete apppool "%APP_POOL_NAME%"
echo.
echo [%date% %time%] Instalacion fallida >> "%INSTALL_LOG%"
exit /b 1

:end
echo [%date% %time%] Instalacion completada exitosamente >> "%INSTALL_LOG%"
exit /b 0
