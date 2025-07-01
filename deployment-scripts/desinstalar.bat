@echo off
echo ====================================
echo   DESINSTALADOR DE DINQR
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
set IIS_ROOT=C:\inetpub\wwwroot
set SITE_DIR=%IIS_ROOT%\dinqr
set LOG_DIR=%SCRIPT_DIR%deployment-logs
set LOG_FILE=%LOG_DIR%\desinstalacion_%date:~-4,4%%date:~-10,2%%date:~-7,2%.log

:: Crear directorio de logs si no existe
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

echo [INFO] Iniciando desinstalación de DINQR...
echo [INFO] Log: %LOG_FILE%

echo [%date% %time%] INICIO: Desinstalación de DINQR >> "%LOG_FILE%"

echo.
echo [WARNING] Esta operación eliminará:
echo [WARNING] - Sitio web DINQR de IIS
echo [WARNING] - Pool de aplicaciones DinqrAppPool
echo [WARNING] - Archivos del sitio web
echo [WARNING] - Base de datos dinqr_db (OPCIONAL)
echo [WARNING] - Logs de aplicación (OPCIONAL)

echo.
set /p confirm="¿Continuar con la desinstalación? (s/N): "
if /i not "%confirm%"=="s" (
    echo [INFO] Desinstalación cancelada por el usuario
    echo [%date% %time%] INFO: Desinstalación cancelada por el usuario >> "%LOG_FILE%"
    pause
    exit /b 0
)

echo.
echo ====================================
echo   PASO 1: DETENER SERVICIOS
echo ====================================

echo [INFO] Deteniendo sitio DINQR en IIS...
echo [%date% %time%] INFO: Deteniendo sitio DINQR >> "%LOG_FILE%"

%windir%\system32\inetsrv\appcmd.exe stop site "DINQR" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] No se pudo detener el sitio DINQR o no existe
    echo [%date% %time%] WARNING: No se pudo detener el sitio DINQR >> "%LOG_FILE%"
) else (
    echo [OK] Sitio DINQR detenido
)

echo [INFO] Deteniendo pool de aplicaciones...
%windir%\system32\inetsrv\appcmd.exe stop apppool "DinqrAppPool" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] No se pudo detener el pool DinqrAppPool o no existe
    echo [%date% %time%] WARNING: No se pudo detener el pool DinqrAppPool >> "%LOG_FILE%"
) else (
    echo [OK] Pool de aplicaciones detenido
)

echo.
echo ====================================
echo   PASO 2: ELIMINAR CONFIGURACIÓN IIS
echo ====================================

echo [INFO] Eliminando sitio de IIS...
%windir%\system32\inetsrv\appcmd.exe delete site "DINQR" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] No se pudo eliminar el sitio DINQR o no existe
    echo [%date% %time%] WARNING: No se pudo eliminar el sitio DINQR >> "%LOG_FILE%"
) else (
    echo [OK] Sitio DINQR eliminado
    echo [%date% %time%] OK: Sitio DINQR eliminado >> "%LOG_FILE%"
)

echo [INFO] Eliminando pool de aplicaciones...
%windir%\system32\inetsrv\appcmd.exe delete apppool "DinqrAppPool" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] No se pudo eliminar el pool DinqrAppPool o no existe
    echo [%date% %time%] WARNING: No se pudo eliminar el pool DinqrAppPool >> "%LOG_FILE%"
) else (
    echo [OK] Pool de aplicaciones eliminado
    echo [%date% %time%] OK: Pool de aplicaciones eliminado >> "%LOG_FILE%"
)

echo.
echo ====================================
echo   PASO 3: ELIMINAR ARCHIVOS
echo ====================================

echo [INFO] Eliminando archivos del sitio web...
if exist "%SITE_DIR%" (
    echo [INFO] Eliminando directorio: %SITE_DIR%
    rmdir /s /q "%SITE_DIR%" >nul 2>&1
    if errorlevel 1 (
        echo [WARNING] No se pudieron eliminar todos los archivos del sitio
        echo [%date% %time%] WARNING: Error eliminando archivos del sitio >> "%LOG_FILE%"
    ) else (
        echo [OK] Archivos del sitio eliminados
        echo [%date% %time%] OK: Archivos del sitio eliminados >> "%LOG_FILE%"
    )
) else (
    echo [INFO] El directorio del sitio no existe
)

echo.
echo ====================================
echo   PASO 4: BASE DE DATOS (OPCIONAL)
echo ====================================

echo [INFO] ¿Deseas eliminar también la base de datos?
echo [WARNING] Esta acción es IRREVERSIBLE
set /p db_confirm="¿Eliminar base de datos dinqr_db? (s/N): "

if /i "%db_confirm%"=="s" (
    echo [INFO] Eliminando base de datos...
    echo [%date% %time%] INFO: Eliminando base de datos dinqr_db >> "%LOG_FILE%"
    
    :: Intentar conectar y eliminar la base de datos
    psql -U postgres -c "DROP DATABASE IF EXISTS dinqr_db;" >nul 2>&1
    if errorlevel 1 (
        echo [WARNING] No se pudo eliminar la base de datos automáticamente
        echo [INFO] Puedes eliminarla manualmente con: DROP DATABASE dinqr_db;
        echo [%date% %time%] WARNING: Error eliminando base de datos >> "%LOG_FILE%"
    ) else (
        echo [OK] Base de datos eliminada
        echo [%date% %time%] OK: Base de datos eliminada >> "%LOG_FILE%"
    )
    
    :: Eliminar usuario de base de datos
    psql -U postgres -c "DROP USER IF EXISTS dinqr_user;" >nul 2>&1
    if not errorlevel 1 (
        echo [OK] Usuario de base de datos eliminado
        echo [%date% %time%] OK: Usuario de base de datos eliminado >> "%LOG_FILE%"
    )
) else (
    echo [INFO] Base de datos conservada
    echo [%date% %time%] INFO: Base de datos conservada >> "%LOG_FILE%"
)

echo.
echo ====================================
echo   PASO 5: LOGS (OPCIONAL)
echo ====================================

echo [INFO] ¿Deseas eliminar los logs de la aplicación?
set /p logs_confirm="¿Eliminar logs? (s/N): "

if /i "%logs_confirm%"=="s" (
    echo [INFO] Eliminando logs...
    echo [%date% %time%] INFO: Eliminando logs de aplicación >> "%LOG_FILE%"
    
    if exist "%PROJECT_ROOT%\backend\logs" (
        rmdir /s /q "%PROJECT_ROOT%\backend\logs" >nul 2>&1
        echo [OK] Logs de backend eliminados
    )
    
    if exist "%LOG_DIR%" (
        :: Crear respaldo del log actual antes de eliminar
        copy "%LOG_FILE%" "%TEMP%\dinqr_desinstalacion_final.log" >nul 2>&1
        echo [OK] Log final respaldado en: %TEMP%\dinqr_desinstalacion_final.log
    )
) else (
    echo [INFO] Logs conservados
    echo [%date% %time%] INFO: Logs conservados >> "%LOG_FILE%"
)

echo.
echo ====================================
echo   PASO 6: LIMPIEZA FINAL
echo ====================================

echo [INFO] Realizando limpieza final...

:: Limpiar variables de entorno (opcional)
echo [INFO] Las variables de entorno del sistema permanecen intactas
echo [INFO] Puedes eliminar manualmente:
echo [INFO] - PYTHONPATH si fue configurado para DINQR
echo [INFO] - NODE_PATH si fue configurado para DINQR

:: Verificar servicios de Windows que puedan estar relacionados
echo [INFO] Verificando servicios relacionados...
sc query "W3SVC" >nul 2>&1
if not errorlevel 1 (
    echo [OK] Servicio IIS (W3SVC) sigue activo
)

echo.
echo ====================================
echo   DESINSTALACIÓN COMPLETADA
echo ====================================

echo [SUCCESS] DINQR ha sido desinstalado exitosamente
echo [%date% %time%] SUCCESS: Desinstalación completada >> "%LOG_FILE%"

echo.
echo [INFO] Resumen de lo eliminado:
echo [INFO] ✓ Sitio web DINQR de IIS
echo [INFO] ✓ Pool de aplicaciones DinqrAppPool
echo [INFO] ✓ Archivos del sitio web
if /i "%db_confirm%"=="s" echo [INFO] ✓ Base de datos dinqr_db
if /i "%logs_confirm%"=="s" echo [INFO] ✓ Logs de aplicación

echo.
echo [INFO] Lo que permanece:
echo [INFO] - Código fuente en: %PROJECT_ROOT%
echo [INFO] - PostgreSQL (servidor)
echo [INFO] - Python, Node.js y otras dependencias del sistema
echo [INFO] - IIS (servidor web)

if /i not "%logs_confirm%"=="s" (
    echo [INFO] - Logs en: %PROJECT_ROOT%\backend\logs\
    echo [INFO] - Logs de despliegue en: %LOG_DIR%
)

echo.
echo [INFO] Para reinstalar DINQR, ejecuta: instalar_completo.bat

echo.
echo [INFO] Log de desinstalación guardado en: %LOG_FILE%
if /i "%logs_confirm%"=="s" (
    echo [INFO] Log final respaldado en: %TEMP%\dinqr_desinstalacion_final.log
)

pause
