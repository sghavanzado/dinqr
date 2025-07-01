@echo off
echo ====================================
echo   COMPILANDO BACKEND DINQR
echo ====================================

:: Configurar colores para Windows
color 0A

:: Obtener directorio actual
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..
set BACKEND_DIR=%PROJECT_ROOT%\backend

echo [INFO] Directorio del proyecto: %PROJECT_ROOT%
echo [INFO] Directorio del backend: %BACKEND_DIR%

:: Verificar que existe el directorio backend
if not exist "%BACKEND_DIR%" (
    echo [ERROR] No se encuentra el directorio backend en: %BACKEND_DIR%
    pause
    exit /b 1
)

:: Cambiar al directorio backend
cd /d "%BACKEND_DIR%"

echo.
echo [PASO 1] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no está instalado o no está en el PATH
    echo [INFO] Instala Python desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python encontrado
python --version

echo.
echo [PASO 2] Verificando entorno virtual...
if not exist "venv\" (
    echo [INFO] Creando entorno virtual...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
    echo [OK] Entorno virtual creado
) else (
    echo [OK] Entorno virtual ya existe
)

echo.
echo [PASO 3] Activando entorno virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] No se pudo activar el entorno virtual
    pause
    exit /b 1
)

echo [OK] Entorno virtual activado

echo.
echo [PASO 4] Actualizando pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo [WARNING] No se pudo actualizar pip, continuando...
)

echo.
echo [PASO 5] Instalando dependencias...
echo [INFO] Instalando desde requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Error al instalar dependencias
    pause
    exit /b 1
)

echo [OK] Dependencias instaladas correctamente

echo.
echo [PASO 6] Verificando instalación...
echo [INFO] Verificando Flask...
python -c "import flask; print(f'Flask {flask.__version__} instalado correctamente')"
if errorlevel 1 (
    echo [ERROR] Flask no está instalado correctamente
    pause
    exit /b 1
)

echo [INFO] Verificando SQLAlchemy...
python -c "import sqlalchemy; print(f'SQLAlchemy {sqlalchemy.__version__} instalado correctamente')"
if errorlevel 1 (
    echo [ERROR] SQLAlchemy no está instalado correctamente
    pause
    exit /b 1
)

echo.
echo [PASO 7] Configurando variables de entorno...
if not exist ".env" (
    echo [INFO] Creando archivo .env desde plantilla...
    if exist ".env.example" (
        copy ".env.example" ".env"
        echo [OK] Archivo .env creado desde plantilla
        echo [WARNING] Recuerda configurar las variables en .env
    ) else (
        echo [WARNING] No existe .env.example, creando .env básico...
        echo # Configuración para DINQR > .env
        echo DATABASE_URL=postgresql://postgres:postgr3s@localhost:5432/localdb >> .env
        echo FLASK_ENV=production >> .env
        echo HOST=0.0.0.0 >> .env
        echo PORT=5000 >> .env
        echo DEBUG=false >> .env
        echo CORS_ORIGINS=http://localhost:3000,http://localhost:8080 >> .env
        echo [OK] Archivo .env básico creado
    )
) else (
    echo [OK] Archivo .env ya existe
)

echo.
echo [PASO 8] Validando estructura del proyecto...
set REQUIRED_FILES=app.py config.py extensions.py requirements.txt
for %%f in (%REQUIRED_FILES%) do (
    if not exist "%%f" (
        echo [ERROR] Archivo requerido no encontrado: %%f
        pause
        exit /b 1
    )
    echo [OK] Encontrado: %%f
)

echo.
echo [PASO 9] Creando directorios necesarios...
if not exist "logs" mkdir logs
if not exist "uploads" mkdir uploads
if not exist "uploads\logos" mkdir uploads\logos
if not exist "static" mkdir static
if not exist "static\qr_codes" mkdir static\qr_codes
echo [OK] Directorios creados

echo.
echo [PASO 10] Verificando configuración...
echo [INFO] Verificando configuración de la aplicación...
python -c "from config import Config; print('Configuración cargada correctamente')"
if errorlevel 1 (
    echo [ERROR] Error en la configuración
    pause
    exit /b 1
)

echo.
echo [PASO 11] Generando archivo de inicio para IIS...
echo import sys > wsgi.py
echo import os >> wsgi.py
echo. >> wsgi.py
echo # Agregar el directorio del proyecto al path >> wsgi.py
echo sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))) >> wsgi.py
echo. >> wsgi.py
echo from app import create_app >> wsgi.py
echo. >> wsgi.py
echo application = create_app() >> wsgi.py
echo. >> wsgi.py
echo if __name__ == "__main__": >> wsgi.py
echo     application.run() >> wsgi.py

echo [OK] Archivo wsgi.py generado para IIS

echo.
echo [PASO 12] Compilando archivos Python (opcional)...
python -m compileall . -q
echo [OK] Archivos Python compilados

echo.
echo ====================================
echo   BACKEND COMPILADO EXITOSAMENTE
echo ====================================
echo.
echo [RESUMEN]
echo - Entorno virtual: %BACKEND_DIR%\venv
echo - Dependencias: Instaladas desde requirements.txt
echo - Configuración: .env creado/verificado
echo - Logs: %BACKEND_DIR%\logs
echo - WSGI: %BACKEND_DIR%\wsgi.py
echo.
echo [SIGUIENTE PASO]
echo Ejecutar: migrar_base_datos.bat
echo.

:: Mantener ventana abierta
echo Presiona cualquier tecla para continuar...
pause >nul

:: Desactivar entorno virtual
call venv\Scripts\deactivate.bat
