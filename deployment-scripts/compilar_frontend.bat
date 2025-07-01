@echo off
echo ====================================
echo   COMPILANDO FRONTEND DINQR
echo ====================================

:: Configurar colores para Windows
color 0B

:: Obtener directorio actual
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..
set FRONTEND_DIR=%PROJECT_ROOT%\frontend

echo [INFO] Directorio del proyecto: %PROJECT_ROOT%
echo [INFO] Directorio del frontend: %FRONTEND_DIR%

:: Verificar que existe el directorio frontend
if not exist "%FRONTEND_DIR%" (
    echo [ERROR] No se encuentra el directorio frontend en: %FRONTEND_DIR%
    pause
    exit /b 1
)

:: Cambiar al directorio frontend
cd /d "%FRONTEND_DIR%"

echo.
echo [PASO 1] Verificando Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js no está instalado o no está en el PATH
    echo [INFO] Instala Node.js desde: https://nodejs.org/
    pause
    exit /b 1
)

echo [OK] Node.js encontrado
node --version

echo.
echo [PASO 2] Verificando npm...
npm --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] npm no está disponible
    pause
    exit /b 1
)

echo [OK] npm encontrado
npm --version

echo.
echo [PASO 3] Verificando estructura del proyecto...
set REQUIRED_FILES=package.json src\main.tsx src\App.tsx
for %%f in (%REQUIRED_FILES%) do (
    if not exist "%%f" (
        echo [ERROR] Archivo requerido no encontrado: %%f
        pause
        exit /b 1
    )
    echo [OK] Encontrado: %%f
)

echo.
echo [PASO 4] Limpiando instalaciones previas...
if exist "node_modules" (
    echo [INFO] Eliminando node_modules anterior...
    rmdir /s /q node_modules
)

if exist "dist" (
    echo [INFO] Eliminando build anterior...
    rmdir /s /q dist
)

echo [OK] Limpieza completada

echo.
echo [PASO 5] Configurando npm cache...
npm cache clean --force
if errorlevel 1 (
    echo [WARNING] No se pudo limpiar la cache de npm, continuando...
)

echo.
echo [PASO 6] Instalando dependencias...
echo [INFO] Instalando dependencias desde package.json...
npm install
if errorlevel 1 (
    echo [ERROR] Error al instalar dependencias de npm
    echo [INFO] Intentando con npm ci...
    npm ci
    if errorlevel 1 (
        echo [ERROR] Error crítico al instalar dependencias
        pause
        exit /b 1
    )
)

echo [OK] Dependencias instaladas correctamente

echo.
echo [PASO 7] Verificando dependencias críticas...
echo [INFO] Verificando React...
npm list react --depth=0
if errorlevel 1 (
    echo [ERROR] React no está instalado correctamente
    pause
    exit /b 1
)

echo [INFO] Verificando TypeScript...
npm list typescript --depth=0
if errorlevel 1 (
    echo [WARNING] TypeScript no encontrado en dependencias locales
)

echo [INFO] Verificando Vite...
npm list vite --depth=0
if errorlevel 1 (
    echo [ERROR] Vite no está instalado correctamente
    pause
    exit /b 1
)

echo.
echo [PASO 8] Configurando variables de entorno para build...
:: Crear archivo .env.production si no existe
if not exist ".env.production" (
    echo [INFO] Creando .env.production...
    echo VITE_API_URL=/api > .env.production
    echo VITE_APP_TITLE=DINQR - Sistema de Códigos QR >> .env.production
    echo VITE_APP_VERSION=1.0.0 >> .env.production
    echo [OK] Archivo .env.production creado
) else (
    echo [OK] Archivo .env.production ya existe
)

echo.
echo [PASO 9] Ejecutando linting (opcional)...
npm run lint >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Linting falló o no está configurado, continuando...
) else (
    echo [OK] Linting completado
)

echo.
echo [PASO 10] Compilando para producción...
echo [INFO] Ejecutando build de producción con Vite...
npm run build
if errorlevel 1 (
    echo [ERROR] Error durante la compilación del frontend
    echo [INFO] Verifica los errores de TypeScript/React arriba
    pause
    exit /b 1
)

echo [OK] Build de producción completado

echo.
echo [PASO 11] Verificando archivos generados...
if not exist "dist" (
    echo [ERROR] No se generó el directorio dist
    pause
    exit /b 1
)

if not exist "dist\index.html" (
    echo [ERROR] No se generó index.html
    pause
    exit /b 1
)

echo [OK] Archivos de build verificados

echo.
echo [PASO 12] Analizando tamaño del build...
echo [INFO] Contenido del directorio dist:
dir dist /s
echo.

:: Calcular tamaño total del build
for /f "tokens=3" %%a in ('dir dist /s /-c ^| find "bytes"') do set BUILD_SIZE=%%a
echo [INFO] Tamaño total del build: %BUILD_SIZE% bytes

echo.
echo [PASO 13] Optimizando archivos estáticos...
:: Crear archivo web.config para IIS si no existe
if not exist "dist\web.config" (
    echo [INFO] Creando web.config para IIS...
    echo ^<?xml version="1.0" encoding="UTF-8"?^> > dist\web.config
    echo ^<configuration^> >> dist\web.config
    echo     ^<system.webServer^> >> dist\web.config
    echo         ^<rewrite^> >> dist\web.config
    echo             ^<rules^> >> dist\web.config
    echo                 ^<rule name="ReactRouter" stopProcessing="true"^> >> dist\web.config
    echo                     ^<match url=".*" /^> >> dist\web.config
    echo                     ^<conditions logicalGrouping="MatchAll"^> >> dist\web.config
    echo                         ^<add input="{REQUEST_FILENAME}" matchType="IsFile" negate="true" /^> >> dist\web.config
    echo                         ^<add input="{REQUEST_FILENAME}" matchType="IsDirectory" negate="true" /^> >> dist\web.config
    echo                         ^<add input="{REQUEST_URI}" pattern="^/api" negate="true" /^> >> dist\web.config
    echo                     ^</conditions^> >> dist\web.config
    echo                     ^<action type="Rewrite" url="/" /^> >> dist\web.config
    echo                 ^</rule^> >> dist\web.config
    echo                 ^<rule name="Flask API" stopProcessing="true"^> >> dist\web.config
    echo                     ^<match url="^api/(.*)" /^> >> dist\web.config
    echo                     ^<action type="Rewrite" url="http://localhost:5000/{R:1}" /^> >> dist\web.config
    echo                 ^</rule^> >> dist\web.config
    echo             ^</rules^> >> dist\web.config
    echo         ^</rewrite^> >> dist\web.config
    echo         ^<staticContent^> >> dist\web.config
    echo             ^<mimeMap fileExtension=".json" mimeType="application/json" /^> >> dist\web.config
    echo             ^<mimeMap fileExtension=".woff" mimeType="application/font-woff" /^> >> dist\web.config
    echo             ^<mimeMap fileExtension=".woff2" mimeType="application/font-woff2" /^> >> dist\web.config
    echo         ^</staticContent^> >> dist\web.config
    echo     ^</system.webServer^> >> dist\web.config
    echo ^</configuration^> >> dist\web.config
    echo [OK] web.config creado para IIS
)

echo.
echo [PASO 14] Creando archivo de información del build...
echo Build Information > dist\build-info.txt
echo Generated: %DATE% %TIME% >> dist\build-info.txt
echo Node.js Version: >> dist\build-info.txt
node --version >> dist\build-info.txt
echo npm Version: >> dist\build-info.txt
npm --version >> dist\build-info.txt
echo Build Size: %BUILD_SIZE% bytes >> dist\build-info.txt

echo.
echo ====================================
echo   FRONTEND COMPILADO EXITOSAMENTE
echo ====================================
echo.
echo [RESUMEN]
echo - Build generado en: %FRONTEND_DIR%\dist
echo - Configuración IIS: web.config incluido
echo - Tamaño del build: %BUILD_SIZE% bytes
echo - Archivos estáticos: Optimizados
echo.
echo [ARCHIVOS PRINCIPALES]
echo - index.html: Punto de entrada
echo - assets/: CSS y JS compilados
echo - web.config: Configuración para IIS
echo.
echo [SIGUIENTE PASO]
echo Ejecutar: desplegar_iis.bat
echo.

:: Mantener ventana abierta
echo Presiona cualquier tecla para continuar...
pause >nul
