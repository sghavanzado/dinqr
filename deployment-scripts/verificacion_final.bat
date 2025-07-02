@echo off
echo ================================================
echo   VERIFICACION COMPLETA POST-INSTALACION
echo ================================================
echo.
echo Este script verifica que DINQR este correctamente
echo instalado y funcionando en Windows Server.
echo.

:: Configurar colores
color 0A

set "SCRIPT_DIR=%~dp0"
set "BASE_DIR=%SCRIPT_DIR%.."
set "LOGFILE=%SCRIPT_DIR%\logs\verificacion_final_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.log"

:: Crear directorio de logs
if not exist "%SCRIPT_DIR%\logs" mkdir "%SCRIPT_DIR%\logs"

echo [INFO] Iniciando verificacion completa...
echo [INFO] Log: %LOGFILE%
echo.

:: Verificar permisos de administrador
net session >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Este script funciona mejor como Administrador
    echo [INFO] Continuando con verificaciones basicas...
    echo.
)

echo ================================================
echo   FASE 1: VERIFICACION DE PREREQUISITOS
echo ================================================
echo.

echo [PASO 1] Verificando sistema operativo...
ver | findstr /i "Windows" >nul
if errorlevel 1 (
    echo [ERROR] Sistema no es Windows >> "%LOGFILE%"
    echo [ERROR] Sistema no es Windows
    goto :FAILED
) else (
    echo [OK] Sistema Windows detectado
    ver >> "%LOGFILE%"
)

echo.
echo [PASO 2] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no encontrado >> "%LOGFILE%"
    echo [ERROR] Python no esta instalado
    goto :FAILED
) else (
    echo [OK] Python instalado
    python --version
    python --version >> "%LOGFILE%"
)

echo.
echo [PASO 3] Verificando Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js no encontrado >> "%LOGFILE%"
    echo [ERROR] Node.js no esta instalado
    goto :FAILED
) else (
    echo [OK] Node.js instalado
    node --version
    node --version >> "%LOGFILE%"
)

echo.
echo [PASO 4] Verificando PostgreSQL...
where psql >nul 2>&1
if errorlevel 1 (
    echo [WARNING] PostgreSQL CLI no encontrado en PATH
    echo [INFO] Verificando servicio...
    sc query postgresql-x64-13 >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Servicio PostgreSQL no encontrado >> "%LOGFILE%"
        echo [ERROR] PostgreSQL no esta corriendo
        goto :FAILED
    ) else (
        echo [OK] Servicio PostgreSQL corriendo
    )
) else (
    echo [OK] PostgreSQL CLI disponible
    psql --version
    psql --version >> "%LOGFILE%"
)

echo.
echo ================================================
echo   FASE 2: VERIFICACION DE IIS
echo ================================================
echo.

echo [PASO 1] Verificando IIS...
%windir%\system32\inetsrv\appcmd.exe list site >nul 2>&1
if errorlevel 1 (
    echo [ERROR] IIS no esta instalado o configurado >> "%LOGFILE%"
    echo [ERROR] IIS no esta funcionando
    goto :FAILED
) else (
    echo [OK] IIS esta funcionando
    echo [INFO] Sitios configurados:
    %windir%\system32\inetsrv\appcmd.exe list site
)

echo.
echo [PASO 2] Verificando sitio DINQR...
%windir%\system32\inetsrv\appcmd.exe list site "DINQR" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Sitio DINQR no configurado aun
) else (
    echo [OK] Sitio DINQR configurado
    %windir%\system32\inetsrv\appcmd.exe list site "DINQR"
)

echo.
echo ================================================
echo   FASE 3: VERIFICACION DE ARCHIVOS
echo ================================================
echo.

echo [PASO 1] Verificando estructura de carpetas...
if not exist "%BASE_DIR%\backend" (
    echo [ERROR] Carpeta backend no encontrada >> "%LOGFILE%"
    echo [ERROR] Carpeta backend faltante
    goto :FAILED
) else (
    echo [OK] Carpeta backend encontrada
)

if not exist "%BASE_DIR%\frontend" (
    echo [ERROR] Carpeta frontend no encontrada >> "%LOGFILE%"
    echo [ERROR] Carpeta frontend faltante
    goto :FAILED
) else (
    echo [OK] Carpeta frontend encontrada
)

echo.
echo [PASO 2] Verificando archivos de aplicacion...
if not exist "%BASE_DIR%\backend\app.py" (
    echo [ERROR] app.py no encontrado >> "%LOGFILE%"
    echo [ERROR] Archivo principal backend faltante
    goto :FAILED
) else (
    echo [OK] app.py encontrado
)

if not exist "%BASE_DIR%\frontend\dist\index.html" (
    echo [WARNING] Frontend no compilado (dist/index.html faltante)
    echo [INFO] Ejecutar: compilar_frontend.bat
) else (
    echo [OK] Frontend compilado encontrado
)

echo.
echo ================================================
echo   FASE 4: VERIFICACION DE DEPENDENCIAS
echo ================================================
echo.

echo [PASO 1] Verificando dependencias Python...
cd /d "%BASE_DIR%\backend"
pip list >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip no funciona >> "%LOGFILE%"
    echo [ERROR] pip no esta funcionando
    goto :FAILED
) else (
    echo [OK] pip funcionando
    echo [INFO] Verificando Flask...
    pip show flask >nul 2>&1
    if errorlevel 1 (
        echo [WARNING] Flask no instalado
        echo [INFO] Ejecutar: pip install -r requirements.txt
    ) else (
        echo [OK] Flask instalado
    )
)

echo.
echo [PASO 2] Verificando dependencias Node.js...
cd /d "%BASE_DIR%\frontend"
if exist "node_modules" (
    echo [OK] node_modules encontrado
) else (
    echo [WARNING] node_modules faltante
    echo [INFO] Ejecutar: npm install
)

echo.
echo ================================================
echo   FASE 5: VERIFICACION DE CONECTIVIDAD
echo ================================================
echo.

echo [PASO 1] Verificando puertos...
netstat -an | findstr ":80 " >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Puerto 80 no en uso
) else (
    echo [OK] Puerto 80 en uso
)

netstat -an | findstr ":443 " >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Puerto 443 no en uso
) else (
    echo [OK] Puerto 443 (HTTPS) en uso
)

echo.
echo [PASO 2] Verificando conectividad local...
ping 127.0.0.1 -n 1 >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Loopback no funciona >> "%LOGFILE%"
    echo [ERROR] Conectividad local fallida
    goto :FAILED
) else (
    echo [OK] Conectividad local funcionando
)

echo.
echo ================================================
echo   FASE 6: PRUEBAS DE FUNCIONAMIENTO
echo ================================================
echo.

echo [PASO 1] Intentando iniciar backend...
cd /d "%BASE_DIR%\backend"
python -c "import app; print('Backend importa correctamente')" 2>nul
if errorlevel 1 (
    echo [WARNING] Backend tiene problemas de importacion
    echo [INFO] Revisar dependencias y configuracion
) else (
    echo [OK] Backend se puede importar correctamente
)

echo.
echo [PASO 2] Verificando configuracion de entorno...
if defined DATABASE_URL (
    echo [OK] DATABASE_URL configurado
) else (
    echo [WARNING] DATABASE_URL no configurado
    echo [INFO] Ejecutar: configurar_ambiente.bat
)

echo.
echo ================================================
echo   RESUMEN DE VERIFICACION
echo ================================================
echo.

goto :SUCCESS

:FAILED
echo.
echo ================================================
echo   VERIFICACION FALLIDA
echo ================================================
echo.
echo [ERROR] Se encontraron problemas criticos
echo [INFO] Revisar el log: %LOGFILE%
echo [INFO] Ejecutar scripts de reparacion:
echo   - instalar_dependencias.bat
echo   - configurar_ambiente.bat
echo   - compilar_todo.bat
echo.
exit /b 1

:SUCCESS
echo [OK] Verificacion completada exitosamente
echo [INFO] DINQR parece estar correctamente instalado
echo.
echo [PROXIMOS PASOS]
echo 1. Si frontend no esta compilado: compilar_frontend.bat
echo 2. Si faltan configuraciones: configurar_ambiente.bat
echo 3. Para desplegar en IIS: desplegar_iis.bat
echo 4. Para monitoreo continuo: monitoreo_salud.bat
echo.
echo [INFO] Log completo guardado en: %LOGFILE%
echo.
echo Presiona cualquier tecla para continuar...
pause >nul
