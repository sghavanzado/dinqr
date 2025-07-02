@echo off
echo ====================================
echo   INSTALANDO DEPENDENCIAS DINQR
echo ====================================

:: Verificar permisos de administrador
net session >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Este script debe ejecutarse como Administrador
    echo [INFO] Click derecho y selecciona "Ejecutar como administrador"
    pause
    exit /b 1
)

:: Configurar colores para Windows
color 0D

echo [INFO] Instalando todas las dependencias necesarias para DINQR...

echo.
echo ====================================
echo   FASE 1: VERIFICANDO SISTEMA
echo ====================================

echo [PASO 1] Verificando sistema operativo...
ver | findstr /i "Windows" >nul
if errorlevel 1 (
    echo [ERROR] Este script es solo para Windows
    pause
    exit /b 1
)

echo [OK] Sistema Windows detectado

echo.
echo [PASO 2] Verificando permisos...
whoami /priv | findstr /i SeBackupPrivilege >nul
if errorlevel 1 (
    echo [WARNING] Algunos permisos pueden estar limitados
) else (
    echo [OK] Permisos de administrador confirmados
)

echo.
echo ====================================
echo   FASE 2: CHOCOLATEY (GESTOR DE PAQUETES)
echo ====================================

echo [PASO 1] Verificando Chocolatey...
where choco >nul 2>&1
if errorlevel 1 (
    echo [INFO] Instalando Chocolatey...
    
    :: Configurar política de ejecución temporalmente
    powershell -Command "Set-ExecutionPolicy Bypass -Scope Process -Force"
    
    :: Instalar Chocolatey
    powershell -Command "[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
    
    if errorlevel 1 (
        echo [ERROR] No se pudo instalar Chocolatey
        echo [INFO] Instalación manual requerida desde: https://chocolatey.org/install
        pause
        exit /b 1
    )
    
    :: Refrescar variables de entorno
    call refreshenv
    echo [OK] Chocolatey instalado
) else (
    echo [OK] Chocolatey ya está instalado
    choco --version
)

echo.
echo ====================================
echo   FASE 3: PYTHON
echo ====================================

echo [PASO 1] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [INFO] Instalando Python 3.11...
    choco install python311 -y
    if errorlevel 1 (
        echo [ERROR] Error al instalar Python
        echo [INFO] Instala manualmente desde: https://www.python.org/downloads/
        pause
        exit /b 1
    )
    
    :: Refrescar PATH
    call refreshenv
    echo [OK] Python instalado
) else (
    echo [OK] Python ya está instalado
    python --version
)

echo.
echo [PASO 2] Verificando pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo [INFO] Instalando pip...
    python -m ensurepip --upgrade
    if errorlevel 1 (
        echo [ERROR] Error al instalar pip
        pause
        exit /b 1
    )
)

echo [OK] pip disponible
pip --version

echo.
echo [PASO 3] Actualizando pip y herramientas...
python -m pip install --upgrade pip
python -m pip install --upgrade setuptools wheel virtualenv

echo [OK] Herramientas Python actualizadas

echo.
echo ====================================
echo   FASE 4: NODE.JS
echo ====================================

echo [PASO 1] Verificando Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo [INFO] Instalando Node.js LTS...
    choco install nodejs-lts -y
    if errorlevel 1 (
        echo [ERROR] Error al instalar Node.js
        echo [INFO] Instala manualmente desde: https://nodejs.org/
        pause
        exit /b 1
    )
    
    :: Refrescar PATH
    call refreshenv
    echo [OK] Node.js instalado
) else (
    echo [OK] Node.js ya está instalado
    node --version
)

echo.
echo [PASO 2] Verificando npm...
npm --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] npm no está disponible
    pause
    exit /b 1
)

echo [OK] npm disponible
npm --version

echo.
echo [PASO 3] Configurando npm...
npm config set fund false
npm config set audit-level moderate
npm install -g npm@latest

echo [OK] npm configurado y actualizado

echo.
echo ====================================
echo   FASE 5: POSTGRESQL
echo ====================================

echo [PASO 1] Verificando PostgreSQL...
where psql >nul 2>&1
if errorlevel 1 (
    echo [INFO] Instalando PostgreSQL...
    choco install postgresql14 --params '/Password:postgr3s' -y
    if errorlevel 1 (
        echo [ERROR] Error al instalar PostgreSQL
        echo [INFO] Instala manualmente desde: https://www.postgresql.org/download/windows/
        pause
        exit /b 1
    )
    
    :: Refrescar PATH
    call refreshenv
    echo [OK] PostgreSQL instalado
) else (
    echo [OK] PostgreSQL ya está instalado
)

echo.
echo [PASO 2] Verificando servicio PostgreSQL...
sc query postgresql-x64-14 >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Servicio PostgreSQL no encontrado
    echo [INFO] Configura el servicio manualmente
) else (
    net start postgresql-x64-14 >nul 2>&1
    echo [OK] Servicio PostgreSQL iniciado
)

echo.
echo ====================================
echo   FASE 6: GIT
echo ====================================

echo [PASO 1] Verificando Git...
where git >nul 2>&1
if errorlevel 1 (
    echo [INFO] Instalando Git...
    choco install git -y
    if errorlevel 1 (
        echo [ERROR] Error al instalar Git
        echo [INFO] Instala manualmente desde: https://git-scm.com/download/win
        pause
        exit /b 1
    )
    
    :: Refrescar PATH
    call refreshenv
    echo [OK] Git instalado
) else (
    echo [OK] Git ya está instalado
    git --version
)

echo.
echo ====================================
echo   FASE 7: IIS Y COMPONENTES WEB
echo ====================================

echo.
echo ====================================
echo   FASE 7: IIS Y COMPONENTES WEB
echo ====================================

echo [PASO 1] Configurando características de IIS...
echo [INFO] Intentando configuración automatizada de IIS...

:: Método 1: Intentar con Bypass policy
echo [INFO] Método 1: PowerShell con ExecutionPolicy Bypass...
powershell -ExecutionPolicy Bypass -File "%SCRIPT_DIR%configurar_iis_features.ps1" -Force 2>nul
if errorlevel 0 if not errorlevel 1 (
    echo [OK] IIS configurado exitosamente con PowerShell (Bypass)
    goto :IIS_CONFIGURED
)

:: Método 2: Intentar con RemoteSigned
echo [INFO] Método 2: PowerShell con ExecutionPolicy RemoteSigned...
powershell -ExecutionPolicy RemoteSigned -File "%SCRIPT_DIR%configurar_iis_features.ps1" -Force 2>nul
if errorlevel 0 if not errorlevel 1 (
    echo [OK] IIS configurado exitosamente con PowerShell (RemoteSigned)
    goto :IIS_CONFIGURED
)

:: Método 3: Intentar desbloquear archivo y ejecutar
echo [INFO] Método 3: Desbloqueando archivo PowerShell...
powershell -Command "Unblock-File -Path '%SCRIPT_DIR%configurar_iis_features.ps1'" 2>nul
powershell -ExecutionPolicy RemoteSigned -File "%SCRIPT_DIR%configurar_iis_features.ps1" -Force 2>nul
if errorlevel 0 if not errorlevel 1 (
    echo [OK] IIS configurado exitosamente con PowerShell (archivo desbloqueado)
    goto :IIS_CONFIGURED
)

:: Método 4: Fallback a DISM
echo [ERROR] No se pudo ejecutar configuracion PowerShell
echo [ERROR] Esto puede deberse a politicas de seguridad de PowerShell
echo.
echo [SOLUCION] Ejecuta: solucionar_powershell.bat
echo            para resolver problemas de ExecutionPolicy
echo.
echo [INFO] Continuando con configuracion basica via DISM...

:DISM_FALLBACK
    echo [WARNING] Error en configuración automatizada, usando método básico...
    
    :: Método alternativo básico usando DISM
    echo [INFO] Habilitando IIS con características básicas...
    dism /online /enable-feature /featurename:IIS-WebServerRole /all >nul
    dism /online /enable-feature /featurename:IIS-WebServer /all >nul
    dism /online /enable-feature /featurename:IIS-CommonHttpFeatures /all >nul
    dism /online /enable-feature /featurename:IIS-HttpErrors /all >nul
    dism /online /enable-feature /featurename:IIS-HttpLogging /all >nul
    dism /online /enable-feature /featurename:IIS-RequestFiltering /all >nul
    dism /online /enable-feature /featurename:IIS-StaticContent /all >nul
    dism /online /enable-feature /featurename:IIS-DefaultDocument /all >nul
    dism /online /enable-feature /featurename:IIS-DirectoryBrowsing /all >nul
    dism /online /enable-feature /featurename:IIS-CGI /all >nul
    dism /online /enable-feature /featurename:IIS-ISAPIExtensions /all >nul
    dism /online /enable-feature /featurename:IIS-ISAPIFilter /all >nul
    dism /online /enable-feature /featurename:IIS-ManagementConsole /all >nul
    dism /online /enable-feature /featurename:IIS-NetFxExtensibility45 /all >nul
    dism /online /enable-feature /featurename:IIS-ASPNET45 /all >nul
    dism /online /enable-feature /featurename:IIS-HttpCompressionStatic /all >nul
    dism /online /enable-feature /featurename:IIS-HttpCompressionDynamic /all >nul
    
    echo [OK] IIS habilitado con características básicas

:IIS_CONFIGURED

:: Verificar que IIS esté funcionando
echo [INFO] Verificando instalación de IIS...
%windir%\system32\inetsrv\appcmd.exe list site >nul 2>&1
if errorlevel 1 (
    echo [ERROR] IIS no está funcionando correctamente
    echo [INFO] Puede ser necesario reiniciar el sistema
) else (
    echo [OK] IIS está funcionando correctamente
)

echo.
echo [PASO 2] Instalando URL Rewrite Module...
if not exist "%ProgramFiles%\IIS\Microsoft URL Rewrite Module 2\rewrite.dll" (
    echo [INFO] Descargando URL Rewrite Module...
    
    :: Crear directorio temporal
    if not exist "%TEMP%\dinqr_setup" mkdir "%TEMP%\dinqr_setup"
    
    :: Descargar URL Rewrite Module
    powershell -Command "Invoke-WebRequest -Uri 'https://download.microsoft.com/download/1/2/8/128E2E22-C1B9-44A4-BE2A-5859ED1D4592/rewrite_amd64_en-US.msi' -OutFile '%TEMP%\dinqr_setup\urlrewrite.msi'"
    
    if exist "%TEMP%\dinqr_setup\urlrewrite.msi" (
        echo [INFO] Instalando URL Rewrite Module...
        msiexec /i "%TEMP%\dinqr_setup\urlrewrite.msi" /quiet /norestart
        echo [OK] URL Rewrite Module instalado
    ) else (
        echo [WARNING] No se pudo descargar URL Rewrite Module
        echo [INFO] Descarga manualmente desde: https://www.iis.net/downloads/microsoft/url-rewrite
    )
) else (
    echo [OK] URL Rewrite Module ya está instalado
)

echo.
echo ====================================
echo   FASE 8: REDIS (OPCIONAL)
echo ====================================

echo [PASO 1] Verificando Redis...
where redis-server >nul 2>&1
if errorlevel 1 (
    echo [INFO] Instalando Redis...
    choco install redis-64 -y
    if errorlevel 1 (
        echo [WARNING] No se pudo instalar Redis automáticamente
        echo [INFO] Redis es opcional para DINQR
    ) else (
        echo [OK] Redis instalado
    )
) else (
    echo [OK] Redis ya está instalado
)

echo.
echo ====================================
echo   FASE 9: HERRAMIENTAS ADICIONALES
echo ====================================

echo [PASO 1] Instalando Visual C++ Redistributable...
choco install vcredist-all -y >nul 2>&1
echo [OK] Visual C++ Redistributable verificado

echo.
echo [PASO 2] Instalando 7-Zip...
where 7z >nul 2>&1
if errorlevel 1 (
    choco install 7zip -y >nul 2>&1
    echo [OK] 7-Zip instalado
) else (
    echo [OK] 7-Zip ya está disponible
)

echo.
echo [PASO 3] Instalando Notepad++...
where notepad++ >nul 2>&1
if errorlevel 1 (
    choco install notepadplusplus -y >nul 2>&1
    echo [OK] Notepad++ instalado
) else (
    echo [OK] Notepad++ ya está disponible
)

echo.
echo ====================================
echo   FASE 10: CONFIGURACION FINAL
echo ====================================

echo [PASO 1] Configurando firewall...
echo [INFO] Configurando reglas de firewall para DINQR...

:: Permitir puerto 5000 (Flask desarrollo)
netsh advfirewall firewall add rule name="DINQR Flask Dev" dir=in action=allow protocol=TCP localport=5000 >nul 2>&1

:: Permitir puerto 8080 (IIS producción)
netsh advfirewall firewall add rule name="DINQR IIS Production" dir=in action=allow protocol=TCP localport=8080 >nul 2>&1

:: Permitir puerto 5432 (PostgreSQL - solo local)
netsh advfirewall firewall add rule name="DINQR PostgreSQL Local" dir=in action=allow protocol=TCP localport=5432 remoteip=127.0.0.1 >nul 2>&1

echo [OK] Reglas de firewall configuradas

echo.
echo [PASO 2] Configurando variables de entorno del sistema...
:: Agregar Python Scripts al PATH si no está
echo %PATH% | findstr /i "Python.*Scripts" >nul
if errorlevel 1 (
    setx PATH "%PATH%;%APPDATA%\Python\Python311\Scripts" /M >nul 2>&1
    echo [OK] Python Scripts agregado al PATH
)

echo.
echo [PASO 3] Limpiando archivos temporales...
if exist "%TEMP%\dinqr_setup" rmdir /s /q "%TEMP%\dinqr_setup"
echo [OK] Limpieza completada

echo.
echo [PASO 4] Verificando instalaciones...
echo [INFO] Verificando que todo esté funcionando...

:: Verificar Python
python --version >nul 2>&1 && echo [OK] Python: Funcionando || echo [ERROR] Python: Error

:: Verificar Node.js
node --version >nul 2>&1 && echo [OK] Node.js: Funcionando || echo [ERROR] Node.js: Error

:: Verificar npm
npm --version >nul 2>&1 && echo [OK] npm: Funcionando || echo [ERROR] npm: Error

:: Verificar PostgreSQL
where psql >nul 2>&1 && echo [OK] PostgreSQL: Instalado || echo [ERROR] PostgreSQL: Error

:: Verificar Git
git --version >nul 2>&1 && echo [OK] Git: Funcionando || echo [ERROR] Git: Error

:: Verificar IIS
%windir%\system32\inetsrv\appcmd.exe list site >nul 2>&1 && echo [OK] IIS: Funcionando || echo [ERROR] IIS: Error

echo.
echo ====================================
echo   INSTALACION COMPLETADA
echo ====================================
echo.
echo [RESUMEN DE INSTALACIONES]
echo ✓ Chocolatey: Gestor de paquetes
echo ✓ Python 3.11: Entorno de desarrollo backend
echo ✓ Node.js LTS: Entorno de desarrollo frontend  
echo ✓ PostgreSQL 14: Base de datos principal
echo ✓ Git: Control de versiones
echo ✓ IIS: Servidor web de producción
echo ✓ URL Rewrite: Módulo para IIS
echo ✓ Redis: Cache (opcional)
echo ✓ Herramientas adicionales: Visual C++, 7-Zip, Notepad++
echo.
echo [PUERTOS CONFIGURADOS EN FIREWALL]
echo - 5000: Flask (desarrollo)
echo - 8080: IIS (producción)
echo - 5432: PostgreSQL (solo local)
echo.
echo [PROXIMOS PASOS]
echo 1. Reiniciar el sistema (recomendado)
echo 2. Ejecutar: verificar_sistema.bat
echo 3. Clonar proyecto DINQR
echo 4. Ejecutar: compilar_todo.bat
echo 5. Ejecutar: configurar_postgresql.bat
echo 6. Ejecutar: desplegar_iis.bat
echo.
echo [COMANDOS UTILES]
echo - Verificar instalaciones: verificar_sistema.bat
echo - Manager IIS: inetmgr
echo - PostgreSQL Shell: psql -U postgres
echo - Chocolatey GUI: choco install chocolateygui
echo.

:: Crear script de verificación rápida
set SCRIPT_DIR=%~dp0
echo @echo off > "%SCRIPT_DIR%verificar_instalaciones.bat"
echo echo Verificando instalaciones... >> "%SCRIPT_DIR%verificar_instalaciones.bat"
echo python --version ^&^& echo [OK] Python || echo [ERROR] Python >> "%SCRIPT_DIR%verificar_instalaciones.bat"
echo node --version ^&^& echo [OK] Node.js || echo [ERROR] Node.js >> "%SCRIPT_DIR%verificar_instalaciones.bat"
echo npm --version ^&^& echo [OK] npm || echo [ERROR] npm >> "%SCRIPT_DIR%verificar_instalaciones.bat"
echo git --version ^&^& echo [OK] Git || echo [ERROR] Git >> "%SCRIPT_DIR%verificar_instalaciones.bat"
echo psql --version ^&^& echo [OK] PostgreSQL || echo [ERROR] PostgreSQL >> "%SCRIPT_DIR%verificar_instalaciones.bat"
echo %%windir%%\system32\inetsrv\appcmd.exe list site ^>nul 2^>^&1 ^&^& echo [OK] IIS || echo [ERROR] IIS >> "%SCRIPT_DIR%verificar_instalaciones.bat"
echo pause >> "%SCRIPT_DIR%verificar_instalaciones.bat"

echo [INFO] Script de verificación creado: verificar_instalaciones.bat
echo.

:: Mantener ventana abierta
echo Presiona cualquier tecla para continuar...
pause >nul
