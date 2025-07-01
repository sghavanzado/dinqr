@echo off
echo ====================================
echo   INSTALADOR COMPLETO DE DINQR
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
set LOG_DIR=%SCRIPT_DIR%deployment-logs

:: Crear timestamp sin caracteres problemáticos
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
set "timestamp=%YYYY%%MM%%DD%_%HH%%Min%%Sec%"

set LOG_FILE=%LOG_DIR%\instalacion_completa_%timestamp%.log

:: Crear directorio de logs
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

echo [INFO] Iniciando instalación completa de DINQR...
echo [INFO] Log: %LOG_FILE%

:: Función de logging
echo [%date% %time%] INICIO: Instalación completa de DINQR >> "%LOG_FILE%"

echo.
echo ====================================
echo   PASO 1: VERIFICACIÓN DEL SISTEMA
echo ====================================

echo [INFO] Verificando sistema...
echo [%date% %time%] INFO: Verificando sistema >> "%LOG_FILE%"
call "%SCRIPT_DIR%verificar_sistema.bat"
if errorlevel 1 (
    echo [ERROR] Verificación del sistema falló
    echo [%date% %time%] ERROR: Verificación del sistema falló >> "%LOG_FILE%"
    goto :error
)

echo.
echo ====================================
echo   PASO 2: INSTALACIÓN DE DEPENDENCIAS
echo ====================================

echo [INFO] Instalando dependencias del sistema...
echo [%date% %time%] INFO: Instalando dependencias del sistema >> "%LOG_FILE%"
call "%SCRIPT_DIR%instalar_dependencias.bat"
if errorlevel 1 (
    echo [ERROR] Instalación de dependencias falló
    echo [%date% %time%] ERROR: Instalación de dependencias falló >> "%LOG_FILE%"
    goto :error
)

echo.
echo ====================================
echo   PASO 3: CONFIGURACIÓN DE POSTGRESQL
echo ====================================

echo [INFO] Configurando PostgreSQL...
echo [%date% %time%] INFO: Configurando PostgreSQL >> "%LOG_FILE%"
call "%SCRIPT_DIR%configurar_postgresql.bat"
if errorlevel 1 (
    echo [ERROR] Configuración de PostgreSQL falló
    echo [%date% %time%] ERROR: Configuración de PostgreSQL falló >> "%LOG_FILE%"
    goto :error
)

echo.
echo ====================================
echo   PASO 4: CONFIGURACIÓN DEL AMBIENTE
echo ====================================

echo [INFO] Configurando ambiente...
echo [%date% %time%] INFO: Configurando ambiente >> "%LOG_FILE%"
call "%SCRIPT_DIR%configurar_ambiente.bat"
if errorlevel 1 (
    echo [ERROR] Configuración del ambiente falló
    echo [%date% %time%] ERROR: Configuración del ambiente falló >> "%LOG_FILE%"
    goto :error
)

echo.
echo ====================================
echo   PASO 5: COMPILACIÓN
echo ====================================

echo [INFO] Compilando aplicación...
echo [%date% %time%] INFO: Compilando aplicación >> "%LOG_FILE%"
call "%SCRIPT_DIR%compilar_todo.bat"
if errorlevel 1 (
    echo [ERROR] Compilación falló
    echo [%date% %time%] ERROR: Compilación falló >> "%LOG_FILE%"
    goto :error
)

echo.
echo ====================================
echo   PASO 6: MIGRACIÓN DE BASE DE DATOS
echo ====================================

echo [INFO] Ejecutando migraciones...
echo [%date% %time%] INFO: Ejecutando migraciones >> "%LOG_FILE%"
call "%SCRIPT_DIR%migrar_base_datos.bat"
if errorlevel 1 (
    echo [ERROR] Migración de base de datos falló
    echo [%date% %time%] ERROR: Migración de base de datos falló >> "%LOG_FILE%"
    goto :error
)

echo.
echo ====================================
echo   PASO 7: DESPLIEGUE EN IIS
echo ====================================

echo [INFO] Desplegando en IIS...
echo [%date% %time%] INFO: Desplegando en IIS >> "%LOG_FILE%"
call "%SCRIPT_DIR%desplegar_iis.bat"
if errorlevel 1 (
    echo [ERROR] Despliegue en IIS falló
    echo [%date% %time%] ERROR: Despliegue en IIS falló >> "%LOG_FILE%"
    goto :error
)

echo.
echo ====================================
echo   PASO 8: VERIFICACIÓN FINAL
echo ====================================

echo [INFO] Verificando instalación...
echo [%date% %time%] INFO: Verificando instalación >> "%LOG_FILE%"
call "%SCRIPT_DIR%verificar_sistema.bat"

echo.
echo ====================================
echo   INSTALACIÓN COMPLETADA
echo ====================================

echo [SUCCESS] DINQR ha sido instalado exitosamente!
echo [%date% %time%] SUCCESS: Instalación completada exitosamente >> "%LOG_FILE%"

echo.
echo [INFO] URLs de acceso:
echo [INFO] - Frontend: http://localhost:8080
echo [INFO] - API Backend: http://localhost:8080/api
echo [INFO] - Documentación API: http://localhost:8080/api/apidocs

echo.
echo [INFO] Servicios configurados:
echo [INFO] - Sitio IIS: DINQR
echo [INFO] - Base de datos: PostgreSQL (dinqr_db)
echo [INFO] - Pool de aplicaciones: DinqrAppPool

echo.
echo [INFO] Archivos importantes:
echo [INFO] - Logs de aplicación: %SCRIPT_DIR%..\backend\logs\
echo [INFO] - Logs de despliegue: %LOG_DIR%
echo [INFO] - Configuración: %SCRIPT_DIR%..\backend\.env

echo.
echo [INFO] Para monitorear logs: ejecuta logs_aplicacion.bat
echo [INFO] Para hacer backup: ejecuta backup_aplicacion.bat

goto :end

:error
echo [ERROR] La instalación falló. Revisa el log para más detalles.
echo [ERROR] Log: %LOG_FILE%
echo [%date% %time%] ERROR: Instalación falló >> "%LOG_FILE%"
echo.
echo [INFO] Para resolución de problemas:
echo [INFO] 1. Revisa el log de errores
echo [INFO] 2. Verifica que tienes permisos de administrador
echo [INFO] 3. Asegúrate de que no hay otros servicios usando los puertos
echo [INFO] 4. Verifica conectividad a internet para descargas
pause
exit /b 1

:end
echo.
echo [INFO] ¡La instalación ha sido completada!
echo [INFO] Presiona cualquier tecla para abrir los logs...
pause
start notepad "%LOG_FILE%"
