@echo off
rem ===============================================================================
rem DINQR - Script de Compilación del Backend para Windows Server
rem ===============================================================================
rem Este script compila el backend de DINQR en un archivo .whl distribuible
rem para facilitar la instalación en servidores Windows de producción.
rem
rem Características:
rem - Compilación a .whl para distribución
rem - Verificación de dependencias
rem - Limpieza automática de archivos temporales
rem - Empaquetado optimizado para Windows Server
rem
rem Uso:
rem   compilar_backend_whl.bat          - Compilar para producción
rem   compilar_backend_whl.bat -dev     - Compilar para desarrollo
rem   compilar_backend_whl.bat -clean   - Solo limpiar archivos temporales
rem
rem Autor: DINQR Deployment Team
rem Fecha: %date%
rem ===============================================================================

setlocal EnableDelayedExpansion

set "SCRIPT_DIR=%~dp0"
set "BACKEND_DIR=%SCRIPT_DIR%..\backend"
set "BUILD_LOG=%SCRIPT_DIR%\compilacion_backend.log"
set "DIST_DIR=%BACKEND_DIR%\dist"
set "BUILD_DIR=%BACKEND_DIR%\build"
set "EGG_INFO_DIR=%BACKEND_DIR%\apiqr.egg-info"

rem Configuración de compilación
set "COMPILE_MODE=production"
set "CLEAN_ONLY=false"

rem Procesar parámetros
if "%1"=="-dev" set "COMPILE_MODE=development"
if "%1"=="--dev" set "COMPILE_MODE=development"
if "%1"=="-clean" set "CLEAN_ONLY=true"
if "%1"=="--clean" set "CLEAN_ONLY=true"

echo ===============================================================================
echo DINQR - COMPILACION DEL BACKEND A .WHL
echo ===============================================================================
echo Fecha/Hora: %date% %time%
echo Modo: %COMPILE_MODE%
echo Directorio backend: %BACKEND_DIR%
echo.

rem Inicializar log
echo [%date% %time%] === INICIO COMPILACION BACKEND === > "%BUILD_LOG%"

if "%CLEAN_ONLY%"=="true" (
    call :clean_build_files
    goto :end
)

rem Verificar prerequisitos
call :check_prerequisites
if errorlevel 1 goto :error

rem Limpiar compilaciones anteriores
call :clean_build_files

rem Actualizar setup.py si es necesario
call :update_setup_py

rem Compilar el backend
call :build_wheel

rem Verificar compilación
call :verify_build

echo.
echo ===============================================================================
echo COMPILACION COMPLETADA EXITOSAMENTE
echo ===============================================================================
echo.
echo Archivos generados:
if exist "%DIST_DIR%" (
    echo   Directorio dist: %DIST_DIR%
    for %%f in ("%DIST_DIR%\*.whl") do (
        echo   ✓ %%~nxf
    )
    for %%f in ("%DIST_DIR%\*.tar.gz") do (
        echo   ✓ %%~nxf
    )
)
echo.
echo Próximos pasos:
echo 1. Copiar archivos .whl al servidor Windows
echo 2. Usar: instalar_desde_whl.bat [archivo.whl]
echo 3. Configurar con: configurar_servidor_produccion.bat
echo.
echo Log detallado: %BUILD_LOG%
echo.
goto :end

rem ===============================================================================
rem FUNCIONES
rem ===============================================================================

:check_prerequisites
echo Verificando prerequisitos...
echo [%date% %time%] Verificando prerequisitos >> "%BUILD_LOG%"

rem Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo [%date% %time%] ERROR: Python no disponible >> "%BUILD_LOG%"
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set "PYTHON_VERSION=%%i"
echo   ✓ Python %PYTHON_VERSION%

rem Verificar que estamos en el directorio correcto
if not exist "%BACKEND_DIR%" (
    echo ERROR: Directorio backend no encontrado: %BACKEND_DIR%
    echo [%date% %time%] ERROR: Directorio backend no encontrado >> "%BUILD_LOG%"
    exit /b 1
)
echo   ✓ Directorio backend encontrado

rem Verificar archivos esenciales
if not exist "%BACKEND_DIR%\app.py" (
    echo ERROR: app.py no encontrado en el backend
    echo [%date% %time%] ERROR: app.py no encontrado >> "%BUILD_LOG%"
    exit /b 1
)
echo   ✓ Archivos principales del backend encontrados

rem Verificar/instalar herramientas de build
echo   Verificando herramientas de compilación...
python -c "import setuptools; print('setuptools OK')" >nul 2>&1
if errorlevel 1 (
    echo   Instalando setuptools...
    python -m pip install setuptools wheel build
    if errorlevel 1 (
        echo ERROR: No se pudo instalar setuptools
        echo [%date% %time%] ERROR: Instalacion setuptools fallida >> "%BUILD_LOG%"
        exit /b 1
    )
)

python -c "import wheel; print('wheel OK')" >nul 2>&1
if errorlevel 1 (
    echo   Instalando wheel...
    python -m pip install wheel
    if errorlevel 1 (
        echo ERROR: No se pudo instalar wheel
        echo [%date% %time%] ERROR: Instalacion wheel fallida >> "%BUILD_LOG%"
        exit /b 1
    )
)

echo   ✓ Herramientas de compilación listas

echo [%date% %time%] Prerequisitos verificados >> "%BUILD_LOG%"
exit /b 0

:clean_build_files
echo Limpiando archivos de compilaciones anteriores...
echo [%date% %time%] Limpiando archivos build >> "%BUILD_LOG%"

cd /d "%BACKEND_DIR%"

if exist "%DIST_DIR%" (
    echo   Eliminando directorio dist...
    rmdir /s /q "%DIST_DIR%" 2>nul
)

if exist "%BUILD_DIR%" (
    echo   Eliminando directorio build...
    rmdir /s /q "%BUILD_DIR%" 2>nul
)

if exist "%EGG_INFO_DIR%" (
    echo   Eliminando directorio egg-info...
    rmdir /s /q "%EGG_INFO_DIR%" 2>nul
)

rem Limpiar archivos .pyc
echo   Eliminando archivos .pyc...
for /r . %%f in (*.pyc) do del "%%f" 2>nul
for /r . %%d in (__pycache__) do rmdir /s /q "%%d" 2>nul

echo   ✓ Limpieza completada
echo [%date% %time%] Limpieza completada >> "%BUILD_LOG%"
exit /b 0

:update_setup_py
echo Verificando/actualizando setup.py...
echo [%date% %time%] Actualizando setup.py >> "%BUILD_LOG%"

cd /d "%BACKEND_DIR%"

rem Verificar si existe setup.py, si no, crearlo
if not exist "setup.py" (
    echo   Creando setup.py...
    call :create_setup_py
) else (
    echo   ✓ setup.py ya existe
)

rem Verificar si existe pyproject.toml y actualizarlo
if exist "pyproject.toml" (
    echo   ✓ pyproject.toml encontrado
) else (
    echo   Creando pyproject.toml...
    call :create_pyproject_toml
)

echo [%date% %time%] setup.py actualizado >> "%BUILD_LOG%"
exit /b 0

:create_setup_py
echo Creando setup.py para DINQR...

cat > setup.py << 'EOF'
"""
Setup script for DINQR Backend
Compilación optimizada para Windows Server con Waitress
"""

from setuptools import setup, find_packages
import os

# Leer README
def read_readme():
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return 'DINQR Backend - Sistema de gestión empresarial'

# Leer requirements
def read_requirements():
    try:
        with open('requirements.txt', 'r', encoding='utf-8') as f:
            return [line.strip() for line in f 
                   if line.strip() and not line.startswith('#') 
                   and not line.startswith('redis==')]  # Excluir Redis
    except:
        return []

setup(
    name='dinqr-backend',
    version='1.0.0',
    description='DINQR Backend - Sistema de gestión empresarial con Waitress',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    author='DINQR Team',
    author_email='admin@dinqr.com',
    url='https://github.com/dinqr/backend',
    
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    
    install_requires=read_requirements(),
    
    extras_require={
        'dev': [
            'pytest>=6.0.0',
            'pytest-cov>=2.0.0',
            'flake8>=3.8.0',
        ],
        'windows': [
            'pywin32>=308',
            'waitress>=3.0.0',
        ]
    },
    
    package_data={
        '': ['*.txt', '*.md', '*.yml', '*.yaml', '*.json', '*.sql'],
        'static': ['*'],
        'templates': ['*'],
    },
    
    entry_points={
        'console_scripts': [
            'dinqr-server=waitress_server:main',
            'dinqr-service=windows_service:main',
        ],
    },
    
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: Microsoft :: Windows',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    
    python_requires='>=3.8',
    
    # Configuración específica para Windows
    platforms=['win32', 'win_amd64'],
)
EOF

echo   ✓ setup.py creado
exit /b 0

:create_pyproject_toml
echo Creando pyproject.toml...

cat > pyproject.toml << 'EOF'
[build-system]
requires = ["setuptools>=45", "wheel", "setuptools_scm[toml]>=6.2"]
build-backend = "setuptools.build_meta"

[project]
name = "dinqr-backend"
version = "1.0.0"
description = "DINQR Backend - Sistema de gestión empresarial con Waitress"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
authors = [
    {name = "DINQR Team", email = "admin@dinqr.com"},
]
keywords = ["flask", "waitress", "windows", "backend", "api"]
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Operating System :: Microsoft :: Windows",
    "Environment :: Web Environment",
    "Framework :: Flask",
    "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
]

dependencies = [
    "Flask>=3.0.0",
    "waitress>=3.0.0",
    "flask-cors>=5.0.0",
    "Flask-JWT-Extended>=4.5.0",
    "Flask-Limiter>=3.12.0",
    "Flask-Login>=0.6.0",
    "Flask-Migrate>=4.0.0",
    "Flask-RESTful>=0.3.10",
    "Flask-SQLAlchemy>=3.1.0",
    "flask-talisman>=1.1.0",
    "SQLAlchemy>=2.0.0",
    "psycopg2-binary>=2.9.0",
    "pyodbc>=5.2.0",
    "python-dotenv>=1.0.0",
    "pywin32>=308; sys_platform == 'win32'",
    "alembic>=1.14.0",
    "marshmallow>=3.26.0",
    "qrcode>=8.1",
    "pillow>=11.1.0",
    "requests>=2.32.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=6.0.0",
    "pytest-cov>=2.0.0",
    "flake8>=3.8.0",
]

[project.scripts]
dinqr-server = "waitress_server:main"
dinqr-service = "windows_service:main"

[tool.setuptools]
packages = ["dinqr"]
include-package-data = true

[tool.setuptools.package-data]
"*" = ["*.txt", "*.md", "*.yml", "*.yaml", "*.json", "*.sql"]
EOF

echo   ✓ pyproject.toml creado
exit /b 0

:build_wheel
echo Compilando backend a .whl...
echo [%date% %time%] Iniciando compilacion wheel >> "%BUILD_LOG%"

cd /d "%BACKEND_DIR%"

echo   Instalando dependencias de desarrollo...
python -m pip install --upgrade pip setuptools wheel build

echo   Construyendo distribución wheel...
python -m build --wheel --sdist 2>>"%BUILD_LOG%"
if errorlevel 1 (
    echo ERROR: Falló la compilación del wheel
    echo [%date% %time%] ERROR: Compilacion wheel fallida >> "%BUILD_LOG%"
    exit /b 1
)

echo   ✓ Compilación wheel completada

rem Verificar que se generaron los archivos
if not exist "%DIST_DIR%" (
    echo ERROR: Directorio dist no fue creado
    echo [%date% %time%] ERROR: Directorio dist no creado >> "%BUILD_LOG%"
    exit /b 1
)

set "WHL_FOUND=false"
for %%f in ("%DIST_DIR%\*.whl") do set "WHL_FOUND=true"

if "%WHL_FOUND%"=="false" (
    echo ERROR: No se generó archivo .whl
    echo [%date% %time%] ERROR: Archivo .whl no generado >> "%BUILD_LOG%"
    exit /b 1
)

echo [%date% %time%] Compilacion wheel exitosa >> "%BUILD_LOG%"
exit /b 0

:verify_build
echo Verificando compilación...
echo [%date% %time%] Verificando compilacion >> "%BUILD_LOG%"

cd /d "%BACKEND_DIR%"

echo   Archivos generados en dist/:
for %%f in ("%DIST_DIR%\*") do (
    echo     %%~nxf (%%~zf bytes)
    echo [%date% %time%] Generado: %%~nxf >> "%BUILD_LOG%"
)

rem Verificar integridad del wheel
for %%f in ("%DIST_DIR%\*.whl") do (
    echo   Verificando integridad de %%~nxf...
    python -m zipfile -l "%%f" >nul 2>&1
    if errorlevel 1 (
        echo   ⚠ WARNING: Posible problema con %%~nxf
        echo [%date% %time%] WARNING: Integridad %%~nxf >> "%BUILD_LOG%"
    ) else (
        echo   ✓ %%~nxf verificado
        echo [%date% %time%] Verificado: %%~nxf >> "%BUILD_LOG%"
    )
)

echo [%date% %time%] Verificacion completada >> "%BUILD_LOG%"
exit /b 0

:error
echo.
echo ===============================================================================
echo ERROR EN LA COMPILACION
echo ===============================================================================
echo.
echo La compilación no se completó exitosamente.
echo.
echo Para solucionar problemas:
echo 1. Revise el log: %BUILD_LOG%
echo 2. Verifique que Python esté instalado correctamente
echo 3. Asegúrese de que todos los archivos del backend estén presentes
echo 4. Ejecute: compilar_backend_whl.bat -clean (para limpiar)
echo.
echo [%date% %time%] Compilacion fallida >> "%BUILD_LOG%"
exit /b 1

:end
echo.
echo Para más opciones use:
echo   %~nx0 -dev    (compilar para desarrollo)
echo   %~nx0 -clean  (limpiar archivos temporales)
echo.
echo Log detallado: %BUILD_LOG%
exit /b 0
