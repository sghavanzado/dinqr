@echo off
echo ====================================
echo   CONFIGURACION IIS CON DISM MANUAL
echo ====================================
echo.
echo Este archivo contiene comandos DISM para configurar IIS
echo cuando PowerShell esta bloqueado por politicas de seguridad.
echo.
echo INSTRUCCIONES:
echo 1. Abrir CMD como Administrador
echo 2. Copiar y pegar cada seccion por separado
echo 3. Esperar a que termine cada comando antes del siguiente
echo 4. Verificar que no haya errores
echo.

:: Verificar permisos de administrador
net session >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Este script debe ejecutarse como Administrador
    echo [INFO] Click derecho en CMD y selecciona "Ejecutar como administrador"
    pause
    exit /b 1
)

echo [INFO] Permisos de administrador confirmados
echo.

echo ====================================
echo   SECCION 1: CARACTERISTICAS BASICAS
echo ====================================
echo.
echo Copiar y pegar estos comandos uno por uno:
echo.

echo REM === Servicios basicos de IIS ===
echo dism /online /enable-feature /featurename:IIS-WebServerRole /all
echo dism /online /enable-feature /featurename:IIS-WebServer /all
echo dism /online /enable-feature /featurename:IIS-CommonHttpFeatures /all
echo.

echo ====================================
echo   SECCION 2: CARACTERISTICAS HTTP
echo ====================================
echo.
echo REM === Documentos y navegacion ===
echo dism /online /enable-feature /featurename:IIS-DefaultDocument /all
echo dism /online /enable-feature /featurename:IIS-DirectoryBrowsing /all
echo dism /online /enable-feature /featurename:IIS-StaticContent /all
echo.
echo REM === Manejo de errores ===
echo dism /online /enable-feature /featurename:IIS-HttpErrors /all
echo dism /online /enable-feature /featurename:IIS-HttpRedirect /all
echo dism /online /enable-feature /featurename:IIS-HttpLogging /all
echo.

echo ====================================
echo   SECCION 3: DESARROLLO DE APLICACIONES
echo ====================================
echo.
echo REM === .NET Framework y ASP.NET ===
echo dism /online /enable-feature /featurename:IIS-NetFxExtensibility45 /all
echo dism /online /enable-feature /featurename:IIS-ASPNET45 /all
echo.
echo REM === CGI e ISAPI (necesario para Python/Flask) ===
echo dism /online /enable-feature /featurename:IIS-CGI /all
echo dism /online /enable-feature /featurename:IIS-ISAPIExtensions /all
echo dism /online /enable-feature /featurename:IIS-ISAPIFilter /all
echo.
echo REM === Caracteristicas adicionales ===
echo dism /online /enable-feature /featurename:IIS-ApplicationDevelopment /all
echo dism /online /enable-feature /featurename:IIS-ApplicationInit /all
echo dism /online /enable-feature /featurename:IIS-WebSockets /all
echo.

echo ====================================
echo   SECCION 4: SEGURIDAD
echo ====================================
echo.
echo REM === Filtrado y seguridad ===
echo dism /online /enable-feature /featurename:IIS-RequestFiltering /all
echo dism /online /enable-feature /featurename:IIS-Security /all
echo.
echo REM === Autenticacion ===
echo dism /online /enable-feature /featurename:IIS-BasicAuthentication /all
echo dism /online /enable-feature /featurename:IIS-WindowsAuthentication /all
echo dism /online /enable-feature /featurename:IIS-DigestAuthentication /all
echo.
echo REM === Autorizacion ===
echo dism /online /enable-feature /featurename:IIS-URLAuthorization /all
echo dism /online /enable-feature /featurename:IIS-IPSecurity /all
echo.

echo ====================================
echo   SECCION 5: RENDIMIENTO
echo ====================================
echo.
echo REM === Compresion ===
echo dism /online /enable-feature /featurename:IIS-HttpCompressionStatic /all
echo dism /online /enable-feature /featurename:IIS-HttpCompressionDynamic /all
echo.

echo ====================================
echo   SECCION 6: LOGGING Y MONITOREO
echo ====================================
echo.
echo REM === Registro y monitoreo ===
echo dism /online /enable-feature /featurename:IIS-CustomLogging /all
echo dism /online /enable-feature /featurename:IIS-LoggingLibraries /all
echo dism /online /enable-feature /featurename:IIS-HttpTracing /all
echo dism /online /enable-feature /featurename:IIS-ODBC /all
echo.

echo ====================================
echo   SECCION 7: ADMINISTRACION
echo ====================================
echo.
echo REM === Consola de administracion ===
echo dism /online /enable-feature /featurename:IIS-ManagementConsole /all
echo.
echo REM === Compatibilidad IIS 6 ===
echo dism /online /enable-feature /featurename:IIS-IIS6ManagementCompatibility /all
echo dism /online /enable-feature /featurename:IIS-Metabase /all
echo dism /online /enable-feature /featurename:IIS-WMICompatibility /all
echo.

echo ====================================
echo   SECCION 8: CONFIGURACION AVANZADA
echo ====================================
echo.
echo REM === Desbloquear configuraciones ===
echo "%windir%\system32\inetsrv\appcmd.exe" unlock config -section:system.webServer/handlers
echo "%windir%\system32\inetsrv\appcmd.exe" unlock config -section:system.webServer/modules
echo "%windir%\system32\inetsrv\appcmd.exe" unlock config -section:system.webServer/httpCompression
echo.

echo ====================================
echo   SECCION 9: VERIFICACION
echo ====================================
echo.
echo REM === Verificar instalacion ===
echo "%windir%\system32\inetsrv\appcmd.exe" list sites
echo iisreset /status
echo.

echo ====================================
echo   COMANDOS AUTOMATICOS (OPCIONAL)
echo ====================================
echo.
echo Si quieres ejecutar todos los comandos automaticamente,
echo presiona cualquier tecla. Si prefieres copiar manualmente,
echo cierra esta ventana ahora.
echo.
pause

echo.
echo [INFO] Ejecutando configuracion automatica...
echo.

REM === Servicios basicos de IIS ===
echo [PASO 1] Configurando servicios basicos...
dism /online /enable-feature /featurename:IIS-WebServerRole /all >nul
dism /online /enable-feature /featurename:IIS-WebServer /all >nul
dism /online /enable-feature /featurename:IIS-CommonHttpFeatures /all >nul

REM === Documentos y navegacion ===
echo [PASO 2] Configurando caracteristicas HTTP...
dism /online /enable-feature /featurename:IIS-DefaultDocument /all >nul
dism /online /enable-feature /featurename:IIS-DirectoryBrowsing /all >nul
dism /online /enable-feature /featurename:IIS-StaticContent /all >nul
dism /online /enable-feature /featurename:IIS-HttpErrors /all >nul
dism /online /enable-feature /featurename:IIS-HttpRedirect /all >nul
dism /online /enable-feature /featurename:IIS-HttpLogging /all >nul

REM === .NET Framework y ASP.NET ===
echo [PASO 3] Configurando desarrollo de aplicaciones...
dism /online /enable-feature /featurename:IIS-NetFxExtensibility45 /all >nul
dism /online /enable-feature /featurename:IIS-ASPNET45 /all >nul

REM === CGI e ISAPI ===
dism /online /enable-feature /featurename:IIS-CGI /all >nul
dism /online /enable-feature /featurename:IIS-ISAPIExtensions /all >nul
dism /online /enable-feature /featurename:IIS-ISAPIFilter /all >nul
dism /online /enable-feature /featurename:IIS-ApplicationDevelopment /all >nul
dism /online /enable-feature /featurename:IIS-ApplicationInit /all >nul
dism /online /enable-feature /featurename:IIS-WebSockets /all >nul

REM === Seguridad ===
echo [PASO 4] Configurando seguridad...
dism /online /enable-feature /featurename:IIS-RequestFiltering /all >nul
dism /online /enable-feature /featurename:IIS-Security /all >nul
dism /online /enable-feature /featurename:IIS-BasicAuthentication /all >nul
dism /online /enable-feature /featurename:IIS-WindowsAuthentication /all >nul
dism /online /enable-feature /featurename:IIS-DigestAuthentication /all >nul
dism /online /enable-feature /featurename:IIS-URLAuthorization /all >nul
dism /online /enable-feature /featurename:IIS-IPSecurity /all >nul

REM === Rendimiento ===
echo [PASO 5] Configurando rendimiento...
dism /online /enable-feature /featurename:IIS-HttpCompressionStatic /all >nul
dism /online /enable-feature /featurename:IIS-HttpCompressionDynamic /all >nul

REM === Logging ===
echo [PASO 6] Configurando logging...
dism /online /enable-feature /featurename:IIS-CustomLogging /all >nul
dism /online /enable-feature /featurename:IIS-LoggingLibraries /all >nul
dism /online /enable-feature /featurename:IIS-HttpTracing /all >nul
dism /online /enable-feature /featurename:IIS-ODBC /all >nul

REM === Administracion ===
echo [PASO 7] Configurando herramientas de administracion...
dism /online /enable-feature /featurename:IIS-ManagementConsole /all >nul
dism /online /enable-feature /featurename:IIS-IIS6ManagementCompatibility /all >nul
dism /online /enable-feature /featurename:IIS-Metabase /all >nul
dism /online /enable-feature /featurename:IIS-WMICompatibility /all >nul

REM === Configuracion avanzada ===
echo [PASO 8] Aplicando configuracion avanzada...
"%windir%\system32\inetsrv\appcmd.exe" unlock config -section:system.webServer/handlers >nul 2>&1
"%windir%\system32\inetsrv\appcmd.exe" unlock config -section:system.webServer/modules >nul 2>&1
"%windir%\system32\inetsrv\appcmd.exe" unlock config -section:system.webServer/httpCompression >nul 2>&1

echo [PASO 9] Verificando instalacion...
"%windir%\system32\inetsrv\appcmd.exe" list sites >nul 2>&1
if errorlevel 1 (
    echo [ERROR] IIS no esta funcionando correctamente
    echo [INFO] Puede ser necesario reiniciar el sistema
) else (
    echo [OK] IIS configurado exitosamente
)

echo.
echo ====================================
echo   CONFIGURACION COMPLETADA
echo ====================================
echo.
echo [OK] IIS ha sido configurado para DINQR
echo.
echo PROXIMOS PASOS:
echo 1. Descargar Application Request Routing (ARR)
echo    URL: https://www.iis.net/downloads/microsoft/application-request-routing
echo 2. Abrir IIS Manager para crear sitio web DINQR
echo 3. Configurar proxy reverso para la API
echo.
echo Presiona cualquier tecla para cerrar...
pause >nul
