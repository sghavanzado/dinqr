@echo off
echo ====================================
echo   VERIFICANDO SISTEMA DINQR
echo ====================================

:: Configurar colores para Windows
color 0B

echo [INFO] Verificando prerrequisitos del sistema para DINQR...

echo.
echo ====================================
echo   VERIFICACION DE SOFTWARE
echo ====================================

:: Variables para tracking de errores
set ERRORS=0
set WARNINGS=0

echo [PASO 1] Verificando sistema operativo...
ver | findstr /i "Windows" >nul
if errorlevel 1 (
    echo [ERROR] Este sistema no es Windows
    set /a ERRORS+=1
) else (
    echo [OK] Sistema Windows detectado
    ver
)

echo.
echo [PASO 2] Verificando permisos de administrador...
net session >nul 2>&1
if errorlevel 1 (
    echo [WARNING] No se ejecuta como administrador
    echo [INFO] Algunas verificaciones pueden fallar
    set /a WARNINGS+=1
) else (
    echo [OK] Ejecutándose como administrador
)

echo.
echo [PASO 3] Verificando Python...
where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no está instalado o no está en el PATH
    echo [SOLUCION] Instalar Python desde: https://www.python.org/downloads/
    set /a ERRORS+=1
) else (
    echo [OK] Python encontrado
    python --version
    
    :: Verificar versión de Python
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo [INFO] Versión: %PYTHON_VERSION%
    
    :: Verificar pip
    pip --version >nul 2>&1
    if errorlevel 1 (
        echo [WARNING] pip no está disponible
        set /a WARNINGS+=1
    ) else (
        echo [OK] pip disponible
        pip --version
    )
)

echo.
echo [PASO 4] Verificando Node.js...
where node >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js no está instalado
    echo [SOLUCION] Instalar Node.js desde: https://nodejs.org/
    set /a ERRORS+=1
) else (
    echo [OK] Node.js encontrado
    node --version
    
    :: Verificar npm
    npm --version >nul 2>&1
    if errorlevel 1 (
        echo [WARNING] npm no está disponible
        set /a WARNINGS+=1
    ) else (
        echo [OK] npm disponible
        npm --version
    )
)

echo.
echo [PASO 5] Verificando Git...
where git >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Git no está instalado
    echo [SOLUCION] Instalar Git desde: https://git-scm.com/download/win
    set /a WARNINGS+=1
) else (
    echo [OK] Git encontrado
    git --version
)

echo.
echo [PASO 6] Verificando PostgreSQL...
where psql >nul 2>&1
if errorlevel 1 (
    echo [ERROR] PostgreSQL no está instalado
    echo [SOLUCION] Instalar PostgreSQL desde: https://www.postgresql.org/download/windows/
    set /a ERRORS+=1
) else (
    echo [OK] PostgreSQL encontrado
    psql --version
    
    :: Verificar servicio
    sc query postgresql-x64-14 >nul 2>&1
    if errorlevel 1 (
        echo [WARNING] Servicio PostgreSQL no encontrado
        set /a WARNINGS+=1
    ) else (
        sc query postgresql-x64-14 | findstr "RUNNING" >nul
        if errorlevel 1 (
            echo [WARNING] Servicio PostgreSQL no está ejecutándose
            set /a WARNINGS+=1
        ) else (
            echo [OK] Servicio PostgreSQL ejecutándose
        )
    )
)

echo.
echo ====================================
echo   VERIFICACION DE IIS
echo ====================================

echo [PASO 1] Verificando IIS...
%windir%\system32\inetsrv\appcmd.exe list site >nul 2>&1
if errorlevel 1 (
    echo [ERROR] IIS no está instalado o no está funcionando
    echo [SOLUCION] Habilitar IIS desde "Características de Windows"
    set /a ERRORS+=1
) else (
    echo [OK] IIS está disponible
    
    :: Verificar Application Pools
    %windir%\system32\inetsrv\appcmd.exe list apppool >nul 2>&1
    if errorlevel 1 (
        echo [WARNING] No se pueden listar Application Pools
        set /a WARNINGS+=1
    ) else (
        echo [OK] Application Pools accesibles
    )
)

echo.
echo [PASO 2] Verificando módulos IIS necesarios...

:: Verificar CGI
%windir%\system32\inetsrv\appcmd.exe list config -section:system.webServer/cgi >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Módulo CGI no parece estar habilitado
    set /a WARNINGS+=1
) else (
    echo [OK] Módulo CGI disponible
)

:: Verificar URL Rewrite
if exist "%ProgramFiles%\IIS\Microsoft URL Rewrite Module 2\rewrite.dll" (
    echo [OK] URL Rewrite Module instalado
) else (
    echo [WARNING] URL Rewrite Module no encontrado
    echo [SOLUCION] Descargar desde: https://www.iis.net/downloads/microsoft/url-rewrite
    set /a WARNINGS+=1
)

echo.
echo ====================================
echo   VERIFICACION DE PUERTOS
echo ====================================

echo [PASO 1] Verificando disponibilidad de puertos...

:: Verificar puerto 5000 (Flask)
netstat -an | findstr ":5000 " >nul
if errorlevel 1 (
    echo [OK] Puerto 5000 disponible para Flask
) else (
    echo [WARNING] Puerto 5000 puede estar en uso
    set /a WARNINGS+=1
)

:: Verificar puerto 8080 (IIS)
netstat -an | findstr ":8080 " >nul
if errorlevel 1 (
    echo [OK] Puerto 8080 disponible para IIS
) else (
    echo [WARNING] Puerto 8080 puede estar en uso
    set /a WARNINGS+=1
)

:: Verificar puerto 5432 (PostgreSQL)
netstat -an | findstr ":5432 " >nul
if errorlevel 1 (
    echo [WARNING] Puerto 5432 no está en uso (PostgreSQL puede no estar ejecutándose)
    set /a WARNINGS+=1
) else (
    echo [OK] Puerto 5432 en uso (PostgreSQL ejecutándose)
)

echo.
echo ====================================
echo   VERIFICACION DE CONECTIVIDAD
echo ====================================

echo [PASO 1] Verificando conectividad local...

:: Ping localhost
ping -n 1 127.0.0.1 >nul 2>&1
if errorlevel 1 (
    echo [ERROR] No se puede hacer ping a localhost
    set /a ERRORS+=1
) else (
    echo [OK] Conectividad localhost funcionando
)

echo.
echo [PASO 2] Verificando conectividad PostgreSQL...
if not %ERRORS% gtr 0 (
    set PGPASSWORD=postgr3s
    psql -U postgres -h localhost -p 5432 -c "SELECT 1;" >nul 2>&1
    if errorlevel 1 (
        echo [WARNING] No se puede conectar a PostgreSQL
        echo [INFO] Puede requerir configuración adicional
        set /a WARNINGS+=1
    ) else (
        echo [OK] Conectividad PostgreSQL funcionando
    )
    set PGPASSWORD=
)

echo.
echo ====================================
echo   VERIFICACION DE ESPACIO EN DISCO
echo ====================================

echo [PASO 1] Verificando espacio disponible...

:: Verificar espacio en C:
for /f "tokens=3" %%a in ('dir C:\ /-c ^| find "bytes free"') do set FREE_SPACE=%%a
echo [INFO] Espacio libre en C:\: %FREE_SPACE% bytes

:: Verificar espacio en directorio de IIS
if exist "C:\inetpub" (
    for /f "tokens=3" %%a in ('dir C:\inetpub /-c ^| find "bytes free"') do set IIS_SPACE=%%a
    echo [OK] Directorio IIS accesible
) else (
    echo [WARNING] Directorio IIS no encontrado
    set /a WARNINGS+=1
)

echo.
echo ====================================
echo   VERIFICACION DE ESTRUCTURA
echo ====================================

set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..

echo [PASO 1] Verificando estructura del proyecto...
if exist "%PROJECT_ROOT%\backend" (
    echo [OK] Directorio backend encontrado
    
    if exist "%PROJECT_ROOT%\backend\app.py" (
        echo [OK] app.py encontrado
    ) else (
        echo [WARNING] app.py no encontrado en backend
        set /a WARNINGS+=1
    )
    
    if exist "%PROJECT_ROOT%\backend\requirements.txt" (
        echo [OK] requirements.txt encontrado
    ) else (
        echo [WARNING] requirements.txt no encontrado
        set /a WARNINGS+=1
    )
) else (
    echo [WARNING] Directorio backend no encontrado
    set /a WARNINGS+=1
)

if exist "%PROJECT_ROOT%\frontend" (
    echo [OK] Directorio frontend encontrado
    
    if exist "%PROJECT_ROOT%\frontend\package.json" (
        echo [OK] package.json encontrado
    ) else (
        echo [WARNING] package.json no encontrado en frontend
        set /a WARNINGS+=1
    )
) else (
    echo [WARNING] Directorio frontend no encontrado
    set /a WARNINGS+=1
)

echo.
echo ====================================
echo   VERIFICACION DE SEGURIDAD
echo ====================================

echo [PASO 1] Verificando firewall...
netsh advfirewall show allprofiles state >nul 2>&1
if errorlevel 1 (
    echo [WARNING] No se puede verificar estado del firewall
    set /a WARNINGS+=1
) else (
    echo [OK] Firewall de Windows disponible
)

echo.
echo [PASO 2] Verificando antivirus...
wmic /namespace:\\root\SecurityCenter2 path AntiVirusProduct get displayName >nul 2>&1
if errorlevel 1 (
    echo [INFO] No se puede detectar antivirus automáticamente
) else (
    echo [OK] Antivirus detectado
    wmic /namespace:\\root\SecurityCenter2 path AntiVirusProduct get displayName /format:list | findstr "DisplayName"
)

echo.
echo ====================================
echo   VERIFICACION DE RENDIMIENTO
echo ====================================

echo [PASO 1] Verificando recursos del sistema...

:: Verificar memoria RAM
for /f "skip=1 tokens=4" %%a in ('wmic computersystem get TotalPhysicalMemory') do (
    if not "%%a"=="" (
        set /a RAM_GB=%%a/1073741824
        echo [INFO] RAM total: !RAM_GB! GB
        if !RAM_GB! lss 4 (
            echo [WARNING] RAM baja para desarrollo web
            set /a WARNINGS+=1
        ) else (
            echo [OK] RAM suficiente
        )
        goto :ram_done
    )
)
:ram_done

:: Verificar procesadores
for /f "skip=1 tokens=1" %%a in ('wmic cpu get NumberOfCores') do (
    if not "%%a"=="" (
        echo [INFO] Núcleos de CPU: %%a
        if %%a lss 2 (
            echo [WARNING] CPU de un solo núcleo puede ser lenta
            set /a WARNINGS+=1
        ) else (
            echo [OK] CPU multinúcleo
        )
        goto :cpu_done
    )
)
:cpu_done

echo.
echo ====================================
echo   RESUMEN DE VERIFICACION
echo ====================================

echo.
echo [ESTADO GENERAL]
if %ERRORS% equ 0 (
    if %WARNINGS% equ 0 (
        echo ✓ SISTEMA LISTO PARA DINQR
        echo [INFO] Todos los prerrequisitos están satisfechos
        color 0A
    ) else (
        echo ⚠ SISTEMA PARCIALMENTE LISTO
        echo [INFO] Hay %WARNINGS% advertencias que revisar
        color 0E
    )
) else (
    echo ✗ SISTEMA NO LISTO
    echo [ERROR] Hay %ERRORS% errores críticos que corregir
    color 0C
)

echo.
echo [ESTADISTICAS]
echo - Errores críticos: %ERRORS%
echo - Advertencias: %WARNINGS%
echo - Verificaciones completadas: 20+

echo.
echo [RECOMENDACIONES]
if %ERRORS% gtr 0 (
    echo 1. Corregir errores críticos primero
    echo 2. Ejecutar: instalar_dependencias.bat
)
if %WARNINGS% gtr 0 (
    echo 3. Revisar advertencias antes de continuar
    echo 4. Configurar servicios y puertos
)
if %ERRORS% equ 0 (
    echo 5. Continuar con: configurar_postgresql.bat
    echo 6. Luego ejecutar: compilar_todo.bat
)

echo.
echo [SIGUIENTE PASO]
if %ERRORS% gtr 0 (
    echo Ejecutar: instalar_dependencias.bat
) else (
    echo Ejecutar: configurar_ambiente.bat
)

echo.
echo ====================================
echo   INFORMACION DEL SISTEMA
echo ====================================

echo [SISTEMA]
systeminfo | findstr /C:"OS Name" /C:"OS Version" /C:"System Type"

echo.
echo [VERSIONES DETECTADAS]
if not %ERRORS% gtr 0 (
    echo Python: 
    python --version 2>&1 | findstr "Python"
    echo Node.js: 
    node --version 2>&1
    echo PostgreSQL: 
    psql --version 2>&1 | findstr "psql"
)

echo.
echo [UBICACIONES IMPORTANTES]
echo - Proyecto: %PROJECT_ROOT%
echo - IIS: C:\inetpub\wwwroot
echo - Logs: %SCRIPT_DIR%logs\
echo - Scripts: %SCRIPT_DIR%

:: Crear archivo de reporte
set REPORT_FILE=%SCRIPT_DIR%system_check_%date:~-4,4%%date:~-10,2%%date:~-7,2%.txt
echo DINQR - Reporte de Verificación del Sistema > %REPORT_FILE%
echo ============================================= >> %REPORT_FILE%
echo. >> %REPORT_FILE%
echo Fecha: %DATE% %TIME% >> %REPORT_FILE%
echo Errores: %ERRORS% >> %REPORT_FILE%
echo Advertencias: %WARNINGS% >> %REPORT_FILE%
echo. >> %REPORT_FILE%
systeminfo >> %REPORT_FILE% 2>&1

echo.
echo [INFO] Reporte guardado en: %REPORT_FILE%
echo.

:: Mantener ventana abierta
echo Presiona cualquier tecla para continuar...
pause >nul
