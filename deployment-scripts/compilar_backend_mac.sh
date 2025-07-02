#!/bin/bash
set -e

# ============================================================================
# DINQR - Script de Compilación del Backend en macOS
# ============================================================================
# Este script prepara y compila el backend de DINQR en macOS generando 
# un archivo .whl que se puede instalar en Windows Server
#
# Funciones:
# - Limpia compilaciones anteriores
# - Actualiza pyproject.toml para Windows Server
# - Compila el paquete .whl
# - Prepara archivos para despliegue
#
# Uso:
#   ./compilar_backend_mac.sh              # Compilación estándar
#   ./compilar_backend_mac.sh --clean      # Solo limpiar
#   ./compilar_backend_mac.sh --dev        # Compilación para desarrollo
#
# Autor: DINQR Development Team
# Fecha: $(date)
# ============================================================================

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables del proyecto
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/../backend"
BUILD_LOG="$SCRIPT_DIR/compilacion_backend.log"
DIST_DIR="$BACKEND_DIR/dist"
BUILD_DIR="$BACKEND_DIR/build"
EGG_INFO_DIR="$BACKEND_DIR/*.egg-info"

# Configuración
COMPILE_MODE="production"
CLEAN_ONLY=false
VERSION="1.0.0"

# Funciones de utilidad
print_header() {
    echo -e "${BLUE}============================================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}============================================================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Procesar argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        --clean|-c)
            CLEAN_ONLY=true
            shift
            ;;
        --dev|-d)
            COMPILE_MODE="development"
            shift
            ;;
        --version|-v)
            VERSION="$2"
            shift 2
            ;;
        --help|-h)
            echo "Uso: $0 [OPTIONS]"
            echo "Opciones:"
            echo "  --clean, -c     Solo limpiar archivos de compilación"
            echo "  --dev, -d       Compilar en modo desarrollo"
            echo "  --version, -v   Especificar versión (default: $VERSION)"
            echo "  --help, -h      Mostrar esta ayuda"
            exit 0
            ;;
        *)
            print_error "Opción desconocida: $1"
            exit 1
            ;;
    esac
done

# Inicializar log
echo "[$(date)] === INICIO COMPILACION BACKEND ===" > "$BUILD_LOG"

print_header "DINQR - COMPILACION DEL BACKEND PARA WINDOWS SERVER"
echo "Fecha/Hora: $(date)"
echo "Modo: $COMPILE_MODE"
echo "Versión: $VERSION"
echo "Directorio backend: $BACKEND_DIR"
echo ""

if [ "$CLEAN_ONLY" = true ]; then
    clean_build_files
    exit 0
fi

# Función para limpiar archivos de compilación
clean_build_files() {
    print_info "Limpiando archivos de compilaciones anteriores..."
    echo "[$(date)] Limpiando archivos build" >> "$BUILD_LOG"
    
    cd "$BACKEND_DIR"
    
    if [ -d "$DIST_DIR" ]; then
        print_info "Eliminando directorio dist..."
        rm -rf "$DIST_DIR"
    fi
    
    if [ -d "$BUILD_DIR" ]; then
        print_info "Eliminando directorio build..."
        rm -rf "$BUILD_DIR"
    fi
    
    # Eliminar directorios egg-info
    find . -name "*.egg-info" -type d -exec rm -rf {} + 2>/dev/null || true
    
    # Limpiar archivos .pyc y __pycache__
    print_info "Eliminando archivos .pyc y __pycache__..."
    find . -name "*.pyc" -delete 2>/dev/null || true
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    
    print_success "Limpieza completada"
    echo "[$(date)] Limpieza completada" >> "$BUILD_LOG"
}

# Función para verificar prerrequisitos
check_prerequisites() {
    print_info "Verificando prerrequisitos..."
    echo "[$(date)] Verificando prerrequisitos" >> "$BUILD_LOG"
    
    # Verificar Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 no está instalado"
        echo "[$(date)] ERROR: Python 3 no disponible" >> "$BUILD_LOG"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2)
    print_success "Python $PYTHON_VERSION encontrado"
    
    # Verificar que estamos en el directorio correcto
    if [ ! -d "$BACKEND_DIR" ]; then
        print_error "Directorio backend no encontrado: $BACKEND_DIR"
        echo "[$(date)] ERROR: Directorio backend no encontrado" >> "$BUILD_LOG"
        exit 1
    fi
    print_success "Directorio backend encontrado"
    
    # Verificar archivos esenciales
    if [ ! -f "$BACKEND_DIR/app.py" ]; then
        print_error "app.py no encontrado en el backend"
        echo "[$(date)] ERROR: app.py no encontrado" >> "$BUILD_LOG"
        exit 1
    fi
    print_success "Archivos principales del backend encontrados"
    
    # Verificar/instalar herramientas de build
    print_info "Verificando herramientas de compilación..."
    if ! python3 -c "import setuptools" &> /dev/null; then
        print_info "Instalando setuptools..."
        python3 -m pip install setuptools wheel build
        if [ $? -ne 0 ]; then
            print_error "No se pudo instalar setuptools"
            echo "[$(date)] ERROR: Instalacion setuptools fallida" >> "$BUILD_LOG"
            exit 1
        fi
    fi
    
    if ! python3 -c "import wheel" &> /dev/null; then
        print_info "Instalando wheel..."
        python3 -m pip install wheel
        if [ $? -ne 0 ]; then
            print_error "No se pudo instalar wheel"
            echo "[$(date)] ERROR: Instalacion wheel fallida" >> "$BUILD_LOG"
            exit 1
        fi
    fi
    
    print_success "Herramientas de compilación listas"
    echo "[$(date)] Prerequisitos verificados" >> "$BUILD_LOG"
}

# Función para actualizar pyproject.toml
update_pyproject() {
    print_info "Actualizando pyproject.toml para Windows Server..."
    echo "[$(date)] Actualizando pyproject.toml" >> "$BUILD_LOG"
    
    cd "$BACKEND_DIR"
    
    # Crear backup del pyproject.toml original
    if [ -f "pyproject.toml" ]; then
        cp "pyproject.toml" "pyproject.toml.backup"
        print_info "Backup creado: pyproject.toml.backup"
    fi
    
    # Crear nuevo pyproject.toml optimizado para Windows Server
    cat > pyproject.toml << 'EOF'
[build-system]
requires = ["setuptools>=45", "wheel", "setuptools_scm[toml]>=6.2"]
build-backend = "setuptools.build_meta"

[project]
name = "dinqr-backend"
version = "1.0.0"
description = "DINQR Backend - Sistema de gestión empresarial con Waitress para Windows Server"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
authors = [
    {name = "DINQR Team", email = "admin@dinqr.com"},
    {name = "Maikel Cuao", email = "maikelcm@hotmail.com"},
]
keywords = ["flask", "waitress", "windows", "backend", "api", "dinqr"]
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX :: Linux",
    "Operating System :: MacOS",
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
    "alembic>=1.14.0",
    "marshmallow>=3.26.0",
    "qrcode>=8.1",
    "pillow>=11.1.0",
    "requests>=2.32.0",
    "flasgger>=0.9.7",
    "blinker>=1.9.0",
    "click>=8.1.0",
    "itsdangerous>=2.2.0",
    "MarkupSafe>=3.0.0",
    "Werkzeug>=3.1.0",
    "gunicorn>=23.0.0",
    "limits>=4.7.0",
    "PyJWT>=2.10.0",
    "pytz>=2024.2",
    "six>=1.17.0",
    "setuptools>=72.2.0",
    "typing_extensions>=4.12.0",
    "urllib3>=2.3.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=6.0.0",
    "pytest-cov>=2.0.0",
    "flake8>=3.8.0",
]
windows = [
    "pywin32>=308; sys_platform == 'win32'",
]

[project.scripts]
dinqr-server = "waitress_server:main"
dinqr-service = "windows_service:main"

[tool.setuptools]
include-package-data = true

[tool.setuptools.packages.find]
exclude = ["tests*", "docs*", "*.tests*", "*.tests.*", "tests.*"]

[tool.setuptools.package-data]
"*" = ["*.txt", "*.md", "*.yml", "*.yaml", "*.json", "*.sql", "*.html", "*.css", "*.js"]
"static" = ["*"]
"templates" = ["*"]
EOF
    
    print_success "pyproject.toml actualizado para Windows Server"
    echo "[$(date)] pyproject.toml actualizado" >> "$BUILD_LOG"
}

# Función para compilar el wheel
build_wheel() {
    print_info "Compilando backend a .whl..."
    echo "[$(date)] Iniciando compilacion wheel" >> "$BUILD_LOG"
    
    cd "$BACKEND_DIR"
    
    print_info "Instalando dependencias de desarrollo..."
    python3 -m pip install --upgrade pip setuptools wheel build
    
    print_info "Construyendo distribución wheel..."
    python3 -m build --wheel --sdist 2>> "$BUILD_LOG"
    
    if [ $? -ne 0 ]; then
        print_error "Falló la compilación del wheel"
        echo "[$(date)] ERROR: Compilacion wheel fallida" >> "$BUILD_LOG"
        exit 1
    fi
    
    print_success "Compilación wheel completada"
    
    # Verificar que se generaron los archivos
    if [ ! -d "$DIST_DIR" ]; then
        print_error "Directorio dist no fue creado"
        echo "[$(date)] ERROR: Directorio dist no creado" >> "$BUILD_LOG"
        exit 1
    fi
    
    WHL_FILES=$(find "$DIST_DIR" -name "*.whl" | wc -l)
    if [ "$WHL_FILES" -eq 0 ]; then
        print_error "No se generó archivo .whl"
        echo "[$(date)] ERROR: Archivo .whl no generado" >> "$BUILD_LOG"
        exit 1
    fi
    
    echo "[$(date)] Compilacion wheel exitosa" >> "$BUILD_LOG"
}

# Función para verificar la compilación
verify_build() {
    print_info "Verificando compilación..."
    echo "[$(date)] Verificando compilacion" >> "$BUILD_LOG"
    
    cd "$BACKEND_DIR"
    
    print_info "Archivos generados en dist/:"
    for file in "$DIST_DIR"/*; do
        if [ -f "$file" ]; then
            filename=$(basename "$file")
            filesize=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo "unknown")
            echo "    $filename ($filesize bytes)"
            echo "[$(date)] Generado: $filename" >> "$BUILD_LOG"
        fi
    done
    
    # Verificar integridad del wheel
    for whl_file in "$DIST_DIR"/*.whl; do
        if [ -f "$whl_file" ]; then
            filename=$(basename "$whl_file")
            print_info "Verificando integridad de $filename..."
            if python3 -m zipfile -l "$whl_file" > /dev/null 2>&1; then
                print_success "$filename verificado"
                echo "[$(date)] Verificado: $filename" >> "$BUILD_LOG"
            else
                print_warning "Posible problema con $filename"
                echo "[$(date)] WARNING: Integridad $filename" >> "$BUILD_LOG"
            fi
        fi
    done
    
    echo "[$(date)] Verificacion completada" >> "$BUILD_LOG"
}

# Función para crear paquete de despliegue
create_deployment_package() {
    print_info "Creando paquete de despliegue para Windows Server..."
    
    DEPLOYMENT_DIR="$SCRIPT_DIR/windows-deployment"
    
    if [ -d "$DEPLOYMENT_DIR" ]; then
        rm -rf "$DEPLOYMENT_DIR"
    fi
    
    mkdir -p "$DEPLOYMENT_DIR"
    
    # Copiar archivos .whl
    cp "$DIST_DIR"/*.whl "$DEPLOYMENT_DIR/" 2>/dev/null || true
    
    # Copiar scripts de despliegue
    cp "$SCRIPT_DIR"/*.bat "$DEPLOYMENT_DIR/" 2>/dev/null || true
    cp "$SCRIPT_DIR"/*.ps1 "$DEPLOYMENT_DIR/" 2>/dev/null || true
    cp "$SCRIPT_DIR"/env-production-template "$DEPLOYMENT_DIR/" 2>/dev/null || true
    cp "$SCRIPT_DIR"/*.md "$DEPLOYMENT_DIR/" 2>/dev/null || true
    
    # Crear archivo README para el paquete
    cat > "$DEPLOYMENT_DIR/README_DESPLIEGUE.txt" << EOF
DINQR - Paquete de Despliegue para Windows Server
================================================

Este paquete contiene todo lo necesario para instalar DINQR en Windows Server.

CONTENIDO:
- dinqr-backend-1.0.0-py3-none-any.whl (aplicación compilada)
- Scripts de instalación (.bat)
- Plantilla de configuración (env-production-template)
- Documentación completa (.md)

INSTALACIÓN RÁPIDA:
1. Copie todos los archivos a Windows Server
2. Ejecute como administrador: desplegar_completo.bat
3. Siga las instrucciones en pantalla

INSTALACIÓN MANUAL:
1. Instale prerrequisitos (Python 3.12, IIS, PostgreSQL)
2. Ejecute: instalar_whl_windows.bat
3. Configure: configurar_iis_proxy.bat
4. Edite: env-production-template -> .env

DOCUMENTACIÓN:
- GUIA_DESPLIEGUE_WINDOWS.md (guía completa)
- GUIA_WAITRESS_IIS.md (configuración específica)

SOPORTE:
Para problemas, consulte los logs y la documentación incluida.

Generado: $(date)
Versión: 1.0.0
EOF
    
    print_success "Paquete de despliegue creado en: $DEPLOYMENT_DIR"
}

# Función principal
main() {
    # Verificar prerrequisitos
    check_prerequisites
    
    # Limpiar compilaciones anteriores
    clean_build_files
    
    # Actualizar configuración del proyecto
    update_pyproject
    
    # Compilar el backend
    build_wheel
    
    # Verificar compilación
    verify_build
    
    # Crear paquete de despliegue
    create_deployment_package
    
    print_header "COMPILACION COMPLETADA EXITOSAMENTE"
    echo ""
    echo "Archivos generados:"
    if [ -d "$DIST_DIR" ]; then
        echo "  Directorio dist: $DIST_DIR"
        for file in "$DIST_DIR"/*; do
            if [ -f "$file" ]; then
                echo "  ✓ $(basename "$file")"
            fi
        done
    fi
    echo ""
    echo "Paquete de despliegue: $SCRIPT_DIR/windows-deployment/"
    echo ""
    echo "PRÓXIMOS PASOS:"
    echo "1. Copie el contenido de windows-deployment/ a Windows Server"
    echo "2. En Windows Server, ejecute como administrador: desplegar_completo.bat"
    echo "3. Configure las variables de entorno según su ambiente"
    echo ""
    echo "Log detallado: $BUILD_LOG"
    echo ""
}

# Manejar errores
handle_error() {
    print_error "Error en la compilación"
    echo ""
    echo "Para solucionar problemas:"
    echo "1. Revise el log: $BUILD_LOG"
    echo "2. Verifique que Python 3 esté instalado correctamente"
    echo "3. Asegúrese de que todos los archivos del backend estén presentes"
    echo "4. Ejecute: $0 --clean (para limpiar)"
    echo ""
    echo "[$(date)] Compilacion fallida" >> "$BUILD_LOG"
    exit 1
}

# Configurar manejo de errores
trap handle_error ERR

# Ejecutar función principal
main

echo ""
echo "Para más opciones use:"
echo "  $0 --dev     (compilar para desarrollo)"
echo "  $0 --clean   (limpiar archivos temporales)"
echo "  $0 --help    (mostrar ayuda)"
echo ""
echo "Log detallado: $BUILD_LOG"
