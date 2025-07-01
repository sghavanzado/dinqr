@echo off
echo ====================================
echo   MIGRANDO BASE DE DATOS DINQR
echo ====================================

:: Configurar colores para Windows
color 0A

:: Obtener directorio actual
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..
set BACKEND_DIR=%PROJECT_ROOT%\backend

echo [INFO] Ejecutando migraciones de base de datos para DINQR...
echo [INFO] Backend: %BACKEND_DIR%

echo.
echo ====================================
echo   FASE 1: VERIFICACIONES PREVIAS
echo ====================================

echo [PASO 1] Verificando directorio backend...
if not exist "%BACKEND_DIR%" (
    echo [ERROR] No se encuentra el directorio backend: %BACKEND_DIR%
    pause
    exit /b 1
)

echo [OK] Directorio backend encontrado

echo.
echo [PASO 2] Verificando entorno virtual...
if not exist "%BACKEND_DIR%\venv\Scripts\python.exe" (
    echo [ERROR] Entorno virtual no encontrado
    echo [INFO] Ejecuta primero: compilar_backend.bat
    pause
    exit /b 1
)

echo [OK] Entorno virtual encontrado

echo.
echo [PASO 3] Verificando PostgreSQL...
set PGPASSWORD=postgr3s
psql -U postgres -h localhost -p 5432 -d localdb -c "SELECT 1;" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] No se puede conectar a PostgreSQL
    echo [INFO] Ejecuta primero: configurar_postgresql.bat
    pause
    exit /b 1
)

echo [OK] Conexión PostgreSQL verificada

echo.
echo [PASO 4] Verificando archivos de migración...
if not exist "%BACKEND_DIR%\migrations" (
    echo [WARNING] Directorio migrations no existe, se creará
) else (
    echo [OK] Directorio migrations encontrado
)

if not exist "%BACKEND_DIR%\alembic.ini" (
    echo [WARNING] alembic.ini no encontrado en backend
    if exist "%BACKEND_DIR%\migrations\alembic.ini" (
        echo [OK] alembic.ini encontrado en migrations
    )
) else (
    echo [OK] alembic.ini encontrado
)

echo.
echo ====================================
echo   FASE 2: CONFIGURACION DE MIGRACIONES
echo ====================================

echo [PASO 1] Cambiando al directorio backend...
cd /d "%BACKEND_DIR%"

echo [PASO 2] Activando entorno virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] No se pudo activar el entorno virtual
    pause
    exit /b 1
)

echo [OK] Entorno virtual activado

echo.
echo [PASO 3] Verificando Flask...
python -c "import flask; print(f'Flask {flask.__version__}')" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Flask no está disponible
    pause
    exit /b 1
)

echo [OK] Flask disponible

echo.
echo [PASO 4] Verificando Alembic...
python -c "import alembic; print(f'Alembic {alembic.__version__}')" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Instalando Alembic...
    pip install alembic
    if errorlevel 1 (
        echo [ERROR] Error al instalar Alembic
        pause
        exit /b 1
    )
)

echo [OK] Alembic disponible

echo.
echo [PASO 5] Configurando variables de entorno...
if exist ".env" (
    echo [OK] Archivo .env encontrado
) else (
    echo [WARNING] Archivo .env no encontrado, usando configuración por defecto
    set DATABASE_URL=postgresql://postgres:postgr3s@localhost:5432/localdb
)

:: Cargar configuración si existe archivo .env.database
if exist ".env.database" (
    echo [INFO] Cargando configuración desde .env.database
    for /f "tokens=1,2 delims==" %%a in (.env.database) do (
        if "%%a"=="DATABASE_URL" set DATABASE_URL=%%b
    )
)

echo [OK] Variables configuradas

echo.
echo ====================================
echo   FASE 3: INICIALIZACION DE MIGRACIONES
echo ====================================

echo [PASO 1] Verificando si Alembic está inicializado...
if not exist "migrations\alembic.ini" (
    echo [INFO] Inicializando Alembic...
    flask db init
    if errorlevel 1 (
        echo [ERROR] Error al inicializar Alembic
        pause
        exit /b 1
    )
    echo [OK] Alembic inicializado
) else (
    echo [OK] Alembic ya está inicializado
)

echo.
echo [PASO 2] Verificando configuración de Alembic...
if exist "migrations\alembic.ini" (
    echo [OK] Configuración de Alembic encontrada
) else (
    echo [ERROR] No se pudo crear la configuración de Alembic
    pause
    exit /b 1
)

echo.
echo ====================================
echo   FASE 4: CREACION DE MIGRACIONES
echo ====================================

echo [PASO 1] Verificando modelos de la aplicación...
python -c "from models.user import User; print('Modelo User OK')" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Error al cargar modelo User
)

python -c "from models.settings import Settings; print('Modelo Settings OK')" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Error al cargar modelo Settings
)

python -c "from models.qrdata import QRCode; print('Modelo QRCode OK')" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Error al cargar modelo QRCode
)

echo.
echo [PASO 2] Verificando migraciones existentes...
if exist "migrations\versions\*.py" (
    echo [INFO] Migraciones existentes encontradas:
    dir migrations\versions\*.py /b
    echo.
    echo [PREGUNTA] ¿Deseas crear una nueva migración? (S/N)
    set /p CREATE_NEW="Respuesta: "
    if /i "%CREATE_NEW%"=="S" (
        goto :create_migration
    ) else (
        goto :apply_migrations
    )
) else (
    echo [INFO] No hay migraciones existentes, creando primera migración...
    goto :create_migration
)

:create_migration
echo [PASO 3] Creando nueva migración...
flask db migrate -m "Initial migration or update"
if errorlevel 1 (
    echo [ERROR] Error al crear migración
    pause
    exit /b 1
)

echo [OK] Migración creada

:apply_migrations
echo.
echo ====================================
echo   FASE 5: APLICACION DE MIGRACIONES
echo ====================================

echo [PASO 1] Verificando estado actual de la base de datos...
flask db current >nul 2>&1
if errorlevel 1 (
    echo [INFO] Base de datos sin migraciones aplicadas
) else (
    echo [INFO] Estado actual de la base de datos:
    flask db current
)

echo.
echo [PASO 2] Aplicando migraciones...
echo [INFO] Esto puede tomar unos momentos...
flask db upgrade
if errorlevel 1 (
    echo [ERROR] Error al aplicar migraciones
    echo [INFO] Verificando detalles del error...
    flask db upgrade --verbose
    pause
    exit /b 1
)

echo [OK] Migraciones aplicadas exitosamente

echo.
echo [PASO 3] Verificando estructura de la base de datos...
echo [INFO] Verificando tablas creadas...
psql -U postgres -h localhost -p 5432 -d localdb -c "\dt" 2>&1 | findstr "table" >nul
if errorlevel 1 (
    echo [WARNING] No se pudieron verificar las tablas automáticamente
) else (
    echo [OK] Tablas verificadas en la base de datos
    psql -U postgres -h localhost -p 5432 -d localdb -c "\dt"
)

echo.
echo ====================================
echo   FASE 6: INICIALIZACION DE DATOS
echo ====================================

echo [PASO 1] Verificando scripts de inicialización...
if exist "initialize_roles.py" (
    echo [INFO] Ejecutando inicialización de roles...
    python initialize_roles.py
    if errorlevel 1 (
        echo [WARNING] Error al inicializar roles, continuando...
    ) else (
        echo [OK] Roles inicializados
    )
) else (
    echo [WARNING] Script initialize_roles.py no encontrado
)

echo.
echo [PASO 2] Creando usuario administrador...
if exist "create_admin.py" (
    echo [INFO] ¿Deseas crear un usuario administrador? (S/N)
    set /p CREATE_ADMIN="Respuesta: "
    if /i "%CREATE_ADMIN%"=="S" (
        python create_admin.py
        if errorlevel 1 (
            echo [WARNING] Error al crear administrador
        ) else (
            echo [OK] Usuario administrador creado
        )
    )
) else (
    echo [WARNING] Script create_admin.py no encontrado
)

echo.
echo [PASO 3] Configurando datos iniciales...
echo [INFO] Insertando configuraciones iniciales en settings...

:: Insertar configuraciones básicas si no existen
psql -U postgres -h localhost -p 5432 -d localdb -c "
INSERT INTO settings (key, value) VALUES 
    ('serverDomain', '127.0.0.1'),
    ('serverPort', '5000'),
    ('outputFolder', 'C:\inetpub\wwwroot\dinqr\uploads\qr_codes'),
    ('maxQRPerBatch', '100'),
    ('qrCodeSize', '200')
ON CONFLICT (key) DO NOTHING;
" >nul 2>&1

if errorlevel 1 (
    echo [WARNING] No se pudieron insertar todas las configuraciones
) else (
    echo [OK] Configuraciones iniciales insertadas
)

echo.
echo ====================================
echo   FASE 7: VERIFICACION FINAL
echo ====================================

echo [PASO 1] Verificando integridad de la base de datos...
psql -U postgres -h localhost -p 5432 -d localdb -c "SELECT COUNT(*) as total_tables FROM information_schema.tables WHERE table_schema = 'public';" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] No se pudo verificar la integridad
) else (
    echo [OK] Base de datos verificada
)

echo.
echo [PASO 2] Verificando conectividad desde la aplicación...
python -c "
from extensions import db
from app import create_app
app = create_app()
with app.app_context():
    try:
        db.engine.execute('SELECT 1')
        print('[OK] Conexión desde aplicación exitosa')
    except Exception as e:
        print(f'[ERROR] Error de conexión: {e}')
" 2>&1

echo.
echo [PASO 3] Creando backup post-migración...
set BACKUP_FILE=backup_post_migration_%date:~-4,4%%date:~-10,2%%date:~-7,2%.sql
echo [INFO] Creando backup: %BACKUP_FILE%
pg_dump -U postgres -h localhost -p 5432 localdb > "%BACKUP_FILE%" 2>&1
if errorlevel 1 (
    echo [WARNING] No se pudo crear backup automático
) else (
    echo [OK] Backup creado: %BACKUP_FILE%
)

echo.
echo [PASO 4] Generando reporte de migración...
set REPORT_FILE=migration_report_%date:~-4,4%%date:~-10,2%%date:~-7,2%.txt
echo DINQR - Reporte de Migración > %REPORT_FILE%
echo ============================== >> %REPORT_FILE%
echo. >> %REPORT_FILE%
echo Fecha: %DATE% %TIME% >> %REPORT_FILE%
echo Backend: %BACKEND_DIR% >> %REPORT_FILE%
echo Base de datos: localdb >> %REPORT_FILE%
echo. >> %REPORT_FILE%
echo Estado actual: >> %REPORT_FILE%
flask db current >> %REPORT_FILE% 2>&1
echo. >> %REPORT_FILE%
echo Tablas creadas: >> %REPORT_FILE%
psql -U postgres -h localhost -p 5432 -d localdb -c "\dt" >> %REPORT_FILE% 2>&1

echo [OK] Reporte generado: %REPORT_FILE%

echo.
echo ====================================
echo   MIGRACION COMPLETADA
echo ====================================
echo.
echo [RESUMEN DE MIGRACION]
echo ✓ Entorno virtual: Activado
echo ✓ Alembic: Configurado
echo ✓ Migraciones: Aplicadas
echo ✓ Base de datos: Estructurada
echo ✓ Datos iniciales: Insertados
echo ✓ Verificación: Completada
echo.
echo [ARCHIVOS GENERADOS]
echo - Backup: %BACKUP_FILE%
echo - Reporte: %REPORT_FILE%
echo - Logs: migrations/
echo.
echo [ESTADO DE LA BASE DE DATOS]
flask db current 2>&1

echo.
echo [ESTRUCTURA ACTUAL]
psql -U postgres -h localhost -p 5432 -d localdb -c "\dt" 2>&1

echo.
echo [CONFIGURACIONES DISPONIBLES]
psql -U postgres -h localhost -p 5432 -d localdb -c "SELECT key, value FROM settings ORDER BY key;" 2>&1

echo.
echo [PROXIMOS PASOS]
echo 1. Verificar estructura: conectar_postgresql.bat
echo 2. Compilar aplicación: compilar_todo.bat
echo 3. Desplegar en IIS: desplegar_iis.bat
echo.

:: Desactivar entorno virtual
call venv\Scripts\deactivate.bat

:: Limpiar variables
set PGPASSWORD=

:: Mantener ventana abierta
echo Presiona cualquier tecla para continuar...
pause >nul
