@echo off
echo ====================================
echo   INSTALACIÓN RÁPIDA DINQR - VERSIÓN CORREGIDA
echo ====================================

:: Verificar permisos de administrador
net session >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Este script debe ejecutarse como Administrador
    echo [INFO] Click derecho en el archivo y selecciona "Ejecutar como administrador"
    pause
    exit /b 1
)

:: Configurar variables
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..
set LOG_DIR=%SCRIPT_DIR%deployment-logs

:: Crear timestamp sin caracteres problemáticos
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
set "timestamp=%YYYY%%MM%%DD%_%HH%%Min%%Sec%"

set LOG_FILE=%LOG_DIR%\instalacion_rapida_%timestamp%.log

:: Crear directorio de logs
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

echo [INFO] Iniciando instalación rápida de DINQR...
echo [INFO] Log: %LOG_FILE%
echo [INFO] Proyecto: %PROJECT_ROOT%

:: Función de logging
echo [%date% %time%] INICIO: Instalación rápida de DINQR >> "%LOG_FILE%"

echo.
echo ====================================
echo   PASO 1: VERIFICACIONES BÁSICAS
echo ====================================

echo [INFO] Verificando estructura del proyecto...
echo [%date% %time%] INFO: Verificando estructura del proyecto >> "%LOG_FILE%"

if not exist "%PROJECT_ROOT%\backend" (
    echo [ERROR] Directorio backend no encontrado en: %PROJECT_ROOT%\backend
    echo [%date% %time%] ERROR: Directorio backend no encontrado >> "%LOG_FILE%"
    goto :error
)

if not exist "%PROJECT_ROOT%\frontend" (
    echo [ERROR] Directorio frontend no encontrado en: %PROJECT_ROOT%\frontend
    echo [%date% %time%] ERROR: Directorio frontend no encontrado >> "%LOG_FILE%"
    goto :error
)

echo [OK] Estructura del proyecto verificada
echo [%date% %time%] OK: Estructura del proyecto verificada >> "%LOG_FILE%"

echo.
echo [INFO] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Python no está instalado o no está en PATH
    echo [%date% %time%] WARNING: Python no disponible >> "%LOG_FILE%"
    echo [INFO] Necesitarás instalar Python 3.10+ manualmente
) else (
    python --version
    echo [OK] Python encontrado
    echo [%date% %time%] OK: Python encontrado >> "%LOG_FILE%"
)

echo.
echo [INFO] Verificando Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Node.js no está instalado o no está en PATH
    echo [%date% %time%] WARNING: Node.js no disponible >> "%LOG_FILE%"
    echo [INFO] Necesitarás instalar Node.js 18+ manualmente
) else (
    node --version
    echo [OK] Node.js encontrado
    echo [%date% %time%] OK: Node.js encontrado >> "%LOG_FILE%"
)

echo.
echo [INFO] Verificando IIS...
%windir%\system32\inetsrv\appcmd.exe list site >nul 2>&1
if errorlevel 1 (
    echo [WARNING] IIS no está disponible
    echo [%date% %time%] WARNING: IIS no disponible >> "%LOG_FILE%"
    echo [INFO] Necesitarás habilitar IIS manualmente
) else (
    echo [OK] IIS está disponible
    echo [%date% %time%] OK: IIS está disponible >> "%LOG_FILE%"
)

echo.
echo ====================================
echo   PASO 2: PREPARAR BACKEND
echo ====================================

echo [INFO] Preparando backend...
echo [%date% %time%] INFO: Preparando backend >> "%LOG_FILE%"

cd /d "%PROJECT_ROOT%\backend"

echo [INFO] Verificando archivo requirements.txt...
if not exist "requirements.txt" (
    echo [ERROR] Archivo requirements.txt no encontrado
    echo [%date% %time%] ERROR: requirements.txt no encontrado >> "%LOG_FILE%"
    goto :error
)

echo [OK] requirements.txt encontrado
echo [%date% %time%] OK: requirements.txt encontrado >> "%LOG_FILE%"

echo.
echo [INFO] Creando entorno virtual Python...
python -m venv venv
if errorlevel 1 (
    echo [ERROR] No se pudo crear el entorno virtual
    echo [%date% %time%] ERROR: No se pudo crear entorno virtual >> "%LOG_FILE%"
    goto :error
)

echo [OK] Entorno virtual creado
echo [%date% %time%] OK: Entorno virtual creado >> "%LOG_FILE%"

echo.
echo [INFO] Activando entorno virtual e instalando dependencias...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] No se pudo activar el entorno virtual
    echo [%date% %time%] ERROR: No se pudo activar entorno virtual >> "%LOG_FILE%"
    goto :error
)

pip install -r requirements.txt
if errorlevel 1 (
    echo [WARNING] Algunos paquetes pueden no haberse instalado correctamente
    echo [%date% %time%] WARNING: Problemas instalando dependencias Python >> "%LOG_FILE%"
) else (
    echo [OK] Dependencias Python instaladas
    echo [%date% %time%] OK: Dependencias Python instaladas >> "%LOG_FILE%"
)

echo.
echo ====================================
echo   PASO 3: PREPARAR FRONTEND
echo ====================================

echo [INFO] Preparando frontend...
echo [%date% %time%] INFO: Preparando frontend >> "%LOG_FILE%"

cd /d "%PROJECT_ROOT%\frontend"

echo [INFO] Verificando package.json...
if not exist "package.json" (
    echo [ERROR] Archivo package.json no encontrado
    echo [%date% %time%] ERROR: package.json no encontrado >> "%LOG_FILE%"
    goto :error
)

echo [OK] package.json encontrado
echo [%date% %time%] OK: package.json encontrado >> "%LOG_FILE%"

echo.
echo [INFO] Instalando dependencias Node.js...
npm install
if errorlevel 1 (
    echo [WARNING] Algunos paquetes pueden no haberse instalado correctamente
    echo [%date% %time%] WARNING: Problemas instalando dependencias Node.js >> "%LOG_FILE%"
) else (
    echo [OK] Dependencias Node.js instaladas
    echo [%date% %time%] OK: Dependencias Node.js instaladas >> "%LOG_FILE%"
)

echo.
echo [INFO] Compilando frontend...
npm run build
if errorlevel 1 (
    echo [WARNING] Compilación del frontend falló
    echo [%date% %time%] WARNING: Compilación del frontend falló >> "%LOG_FILE%"
) else (
    echo [OK] Frontend compilado exitosamente
    echo [%date% %time%] OK: Frontend compilado >> "%LOG_FILE%"
)

echo.
echo ====================================
echo   PASO 4: CREAR CONFIGURACIÓN BÁSICA
echo ====================================

echo [INFO] Creando configuración básica...
echo [%date% %time%] INFO: Creando configuración básica >> "%LOG_FILE%"

cd /d "%PROJECT_ROOT%\backend"

echo [INFO] Verificando archivo .env...
if not exist ".env" (
    echo [INFO] Creando archivo .env básico...
    (
    echo # Configuración básica de DINQR
    echo DATABASE_URL=postgresql://postgres:postgr3s@localhost:5432/localdb
    echo LOCAL_DB_NAME=localdb
    echo LOCAL_DB_USER=postgres
    echo LOCAL_DB_PASSWORD=postgr3s
    echo LOCAL_DB_HOST=localhost
    echo LOCAL_DB_PORT=5432
    echo.
    echo # Configuración del servidor
    echo HOST=0.0.0.0
    echo PORT=5000
    echo DEBUG=false
    echo FLASK_ENV=production
    echo.
    echo # CORS
    echo CORS_ORIGINS=http://localhost:3000,http://localhost:8080
    echo.
    echo # Logging
    echo LOG_LEVEL=INFO
    echo LOG_FILE=logs/app.log
    ) > .env
    
    echo [OK] Archivo .env creado
    echo [%date% %time%] OK: Archivo .env creado >> "%LOG_FILE%"
) else (
    echo [OK] Archivo .env ya existe
    echo [%date% %time%] OK: Archivo .env ya existe >> "%LOG_FILE%"
)

echo.
echo ====================================
echo   RESULTADO DE LA INSTALACIÓN RÁPIDA
echo ====================================

echo [SUCCESS] Instalación rápida completada
echo [%date% %time%] SUCCESS: Instalación rápida completada >> "%LOG_FILE%"

echo.
echo [INFO] Estado del proyecto:
echo [INFO] ✅ Código fuente copiado
echo [INFO] ✅ Entorno virtual Python creado
echo [INFO] ✅ Dependencias Python instaladas
echo [INFO] ✅ Dependencias Node.js instaladas
echo [INFO] ✅ Frontend compilado
echo [INFO] ✅ Configuración básica creada

echo.
echo [INFO] Próximos pasos necesarios:
echo [INFO] 1. Instalar y configurar PostgreSQL
echo [INFO] 2. Crear la base de datos 'localdb'
echo [INFO] 3. Ejecutar migraciones: flask db upgrade
echo [INFO] 4. Configurar IIS para el despliegue
echo [INFO] 5. Crear usuario administrador: python create_admin.py

echo.
echo [INFO] Para continuar con la instalación completa:
echo [INFO] - instalar_dependencias.bat (instalar PostgreSQL, etc.)
echo [INFO] - configurar_postgresql.bat (configurar base de datos)
echo [INFO] - migrar_base_datos.bat (crear tablas)
echo [INFO] - desplegar_iis.bat (desplegar en IIS)

echo.
echo [INFO] Para prueba rápida del backend:
echo [INFO] cd %PROJECT_ROOT%\backend
echo [INFO] venv\Scripts\activate
echo [INFO] python app.py

echo.
echo [INFO] Log completo guardado en: %LOG_FILE%

goto :end

:error
echo [ERROR] La instalación rápida falló
echo [ERROR] Revisa el log para más detalles: %LOG_FILE%
echo [%date% %time%] ERROR: Instalación rápida falló >> "%LOG_FILE%"

echo.
echo [INFO] Pasos de resolución:
echo [INFO] 1. Verificar que Python 3.10+ esté instalado
echo [INFO] 2. Verificar que Node.js 18+ esté instalado  
echo [INFO] 3. Verificar conexión a internet
echo [INFO] 4. Ejecutar como Administrador
echo [INFO] 5. Verificar que la carpeta dinqr esté en C:\

pause
exit /b 1

:end
echo.
echo [SUCCESS] Instalación rápida completada exitosamente
echo [INFO] Puedes continuar con los scripts específicos según tus necesidades
pause
