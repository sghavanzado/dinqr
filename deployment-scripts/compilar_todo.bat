@echo off
echo ====================================
echo   COMPILACION COMPLETA DINQR
echo ====================================

:: Configurar colores para Windows
color 0E

:: Obtener directorio actual
set SCRIPT_DIR=%~dp0

echo [INFO] Iniciando compilación completa de DINQR...
echo [INFO] Directorio de scripts: %SCRIPT_DIR%

:: Variables de tiempo para medir duración
set START_TIME=%TIME%

echo.
echo ====================================
echo   FASE 1: COMPILANDO BACKEND
echo ====================================

call "%SCRIPT_DIR%compilar_backend.bat"
if errorlevel 1 (
    echo [ERROR] Falló la compilación del backend
    echo [INFO] Revisa los errores arriba y corrige antes de continuar
    pause
    exit /b 1
)

echo.
echo [OK] Backend compilado exitosamente
echo.

echo ====================================
echo   FASE 2: COMPILANDO FRONTEND
echo ====================================

call "%SCRIPT_DIR%compilar_frontend.bat"
if errorlevel 1 (
    echo [ERROR] Falló la compilación del frontend
    echo [INFO] Revisa los errores arriba y corrige antes de continuar
    pause
    exit /b 1
)

echo.
echo [OK] Frontend compilado exitosamente
echo.

echo ====================================
echo   FASE 3: VERIFICACION FINAL
echo ====================================

echo [PASO 1] Verificando archivos del backend...
set BACKEND_DIR=%SCRIPT_DIR%..\backend
if not exist "%BACKEND_DIR%\wsgi.py" (
    echo [ERROR] No se encontró wsgi.py en el backend
    pause
    exit /b 1
)

if not exist "%BACKEND_DIR%\venv\Scripts\python.exe" (
    echo [ERROR] No se encontró el entorno virtual del backend
    pause
    exit /b 1
)

echo [OK] Backend verificado

echo.
echo [PASO 2] Verificando archivos del frontend...
set FRONTEND_DIR=%SCRIPT_DIR%..\frontend
if not exist "%FRONTEND_DIR%\dist\index.html" (
    echo [ERROR] No se encontró el build del frontend
    pause
    exit /b 1
)

if not exist "%FRONTEND_DIR%\dist\web.config" (
    echo [ERROR] No se encontró web.config del frontend
    pause
    exit /b 1
)

echo [OK] Frontend verificado

echo.
echo [PASO 3] Generando resumen de compilación...
set END_TIME=%TIME%

:: Crear archivo de resumen
set SUMMARY_FILE=%SCRIPT_DIR%build-summary.txt
echo DINQR - Resumen de Compilación > %SUMMARY_FILE%
echo ================================ >> %SUMMARY_FILE%
echo. >> %SUMMARY_FILE%
echo Fecha: %DATE% >> %SUMMARY_FILE%
echo Hora inicio: %START_TIME% >> %SUMMARY_FILE%
echo Hora fin: %END_TIME% >> %SUMMARY_FILE%
echo. >> %SUMMARY_FILE%
echo BACKEND: >> %SUMMARY_FILE%
echo - Entorno virtual: OK >> %SUMMARY_FILE%
echo - Dependencias: Instaladas >> %SUMMARY_FILE%
echo - WSGI: Configurado >> %SUMMARY_FILE%
echo. >> %SUMMARY_FILE%
echo FRONTEND: >> %SUMMARY_FILE%
echo - Build de producción: OK >> %SUMMARY_FILE%
echo - Configuración IIS: OK >> %SUMMARY_FILE%
echo - Assets optimizados: OK >> %SUMMARY_FILE%
echo. >> %SUMMARY_FILE%
echo ESTRUCTURA: >> %SUMMARY_FILE%
dir "%BACKEND_DIR%" /b >> %SUMMARY_FILE%
echo. >> %SUMMARY_FILE%
echo FRONTEND DIST: >> %SUMMARY_FILE%
dir "%FRONTEND_DIR%\dist" /b >> %SUMMARY_FILE%

echo [OK] Resumen generado: %SUMMARY_FILE%

echo.
echo [PASO 4] Verificando tamaños de archivos...
echo [INFO] Tamaño del backend (sin venv):
for /f "tokens=3" %%a in ('dir "%BACKEND_DIR%" /s /-c ^| find "bytes"') do set BACKEND_SIZE=%%a
echo Backend: %BACKEND_SIZE% bytes

echo [INFO] Tamaño del frontend dist:
for /f "tokens=3" %%a in ('dir "%FRONTEND_DIR%\dist" /s /-c ^| find "bytes"') do set FRONTEND_SIZE=%%a
echo Frontend: %FRONTEND_SIZE% bytes

echo.
echo ====================================
echo   COMPILACION COMPLETADA
echo ====================================
echo.
echo [RESUMEN FINAL]
echo ✓ Backend: Compilado y configurado
echo ✓ Frontend: Compilado y optimizado
echo ✓ Estructura: Verificada
echo ✓ Configuración: Lista para IIS
echo.
echo [ARCHIVOS LISTOS PARA DESPLIEGUE]
echo Backend WSGI: %BACKEND_DIR%\wsgi.py
echo Frontend Build: %FRONTEND_DIR%\dist\
echo.
echo [PROXIMOS PASOS]
echo 1. Ejecutar: configurar_postgresql.bat
echo 2. Ejecutar: migrar_base_datos.bat  
echo 3. Ejecutar: desplegar_iis.bat
echo.
echo [TIEMPO TOTAL]
echo Inicio: %START_TIME%
echo Fin: %END_TIME%
echo.

:: Crear script de limpieza rápida
echo @echo off > "%SCRIPT_DIR%limpiar_builds.bat"
echo echo Limpiando builds anteriores... >> "%SCRIPT_DIR%limpiar_builds.bat"
echo if exist "%BACKEND_DIR%\venv" rmdir /s /q "%BACKEND_DIR%\venv" >> "%SCRIPT_DIR%limpiar_builds.bat"
echo if exist "%FRONTEND_DIR%\dist" rmdir /s /q "%FRONTEND_DIR%\dist" >> "%SCRIPT_DIR%limpiar_builds.bat"
echo if exist "%FRONTEND_DIR%\node_modules" rmdir /s /q "%FRONTEND_DIR%\node_modules" >> "%SCRIPT_DIR%limpiar_builds.bat"
echo echo Limpieza completada >> "%SCRIPT_DIR%limpiar_builds.bat"

echo [INFO] Script de limpieza creado: limpiar_builds.bat
echo.

:: Mantener ventana abierta
echo Presiona cualquier tecla para continuar...
pause >nul
