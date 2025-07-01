@echo off
echo ====================================
echo   BACKUP APLICACION DINQR
echo ====================================

:: Configurar colores para Windows
color 0D

:: Obtener directorio actual
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..
set BACKUP_ROOT=%SCRIPT_DIR%backups

echo [INFO] Creando backup completo de DINQR...
echo [INFO] Proyecto: %PROJECT_ROOT%
echo [INFO] Destino: %BACKUP_ROOT%

:: Crear directorio de backups si no existe
if not exist "%BACKUP_ROOT%" mkdir "%BACKUP_ROOT%"

:: Generar timestamp para el backup
for /f "tokens=1-6 delims=/: " %%a in ('echo %date% %time%') do (
    set TIMESTAMP=%%c%%b%%a_%%d%%e%%f
)
set TIMESTAMP=%TIMESTAMP: =0%
set TIMESTAMP=%TIMESTAMP:~0,15%

set BACKUP_DIR=%BACKUP_ROOT%\dinqr_backup_%TIMESTAMP%
echo [INFO] Directorio de backup: %BACKUP_DIR%

echo.
echo ====================================
echo   FASE 1: PREPARACION
echo ====================================

echo [PASO 1] Creando estructura de backup...
mkdir "%BACKUP_DIR%"
mkdir "%BACKUP_DIR%\backend"
mkdir "%BACKUP_DIR%\frontend"
mkdir "%BACKUP_DIR%\database"
mkdir "%BACKUP_DIR%\logs"
mkdir "%BACKUP_DIR%\config"
mkdir "%BACKUP_DIR%\scripts"

echo [OK] Estructura creada

echo.
echo [PASO 2] Verificando herramientas...
where 7z >nul 2>&1
if errorlevel 1 (
    echo [WARNING] 7-Zip no encontrado, usando copy
    set USE_7ZIP=false
) else (
    echo [OK] 7-Zip disponible para compresión
    set USE_7ZIP=true
)

echo.
echo ====================================
echo   FASE 2: BACKUP DEL BACKEND
echo ====================================

echo [PASO 1] Copiando archivos del backend...
if exist "%PROJECT_ROOT%\backend" (
    echo [INFO] Copiando backend...
    
    :: Copiar archivos principales
    xcopy /E /I /Y "%PROJECT_ROOT%\backend\*.py" "%BACKUP_DIR%\backend\" >nul 2>&1
    xcopy /E /I /Y "%PROJECT_ROOT%\backend\*.txt" "%BACKUP_DIR%\backend\" >nul 2>&1
    xcopy /E /I /Y "%PROJECT_ROOT%\backend\*.ini" "%BACKUP_DIR%\backend\" >nul 2>&1
    xcopy /E /I /Y "%PROJECT_ROOT%\backend\*.toml" "%BACKUP_DIR%\backend\" >nul 2>&1
    xcopy /E /I /Y "%PROJECT_ROOT%\backend\*.json" "%BACKUP_DIR%\backend\" >nul 2>&1
    xcopy /E /I /Y "%PROJECT_ROOT%\backend\.env*" "%BACKUP_DIR%\backend\" >nul 2>&1
    
    :: Copiar directorios importantes
    if exist "%PROJECT_ROOT%\backend\models" xcopy /E /I /Y "%PROJECT_ROOT%\backend\models" "%BACKUP_DIR%\backend\models\" >nul 2>&1
    if exist "%PROJECT_ROOT%\backend\routes" xcopy /E /I /Y "%PROJECT_ROOT%\backend\routes" "%BACKUP_DIR%\backend\routes\" >nul 2>&1
    if exist "%PROJECT_ROOT%\backend\services" xcopy /E /I /Y "%PROJECT_ROOT%\backend\services" "%BACKUP_DIR%\backend\services\" >nul 2>&1
    if exist "%PROJECT_ROOT%\backend\utils" xcopy /E /I /Y "%PROJECT_ROOT%\backend\utils" "%BACKUP_DIR%\backend\utils\" >nul 2>&1
    if exist "%PROJECT_ROOT%\backend\migrations" xcopy /E /I /Y "%PROJECT_ROOT%\backend\migrations" "%BACKUP_DIR%\backend\migrations\" >nul 2>&1
    if exist "%PROJECT_ROOT%\backend\static" xcopy /E /I /Y "%PROJECT_ROOT%\backend\static" "%BACKUP_DIR%\backend\static\" >nul 2>&1
    
    echo [OK] Backend copiado
) else (
    echo [WARNING] Directorio backend no encontrado
)

echo.
echo [PASO 2] Copiando logs del backend...
if exist "%PROJECT_ROOT%\backend\logs" (
    xcopy /E /I /Y "%PROJECT_ROOT%\backend\logs\*" "%BACKUP_DIR%\logs\backend\" >nul 2>&1
    echo [OK] Logs del backend copiados
) else (
    echo [INFO] No hay logs del backend
)

echo.
echo ====================================
echo   FASE 3: BACKUP DEL FRONTEND
echo ====================================

echo [PASO 1] Copiando archivos del frontend...
if exist "%PROJECT_ROOT%\frontend" (
    echo [INFO] Copiando frontend...
    
    :: Copiar archivos de configuración
    xcopy /Y "%PROJECT_ROOT%\frontend\package*.json" "%BACKUP_DIR%\frontend\" >nul 2>&1
    xcopy /Y "%PROJECT_ROOT%\frontend\*.config.*" "%BACKUP_DIR%\frontend\" >nul 2>&1
    xcopy /Y "%PROJECT_ROOT%\frontend\*.json" "%BACKUP_DIR%\frontend\" >nul 2>&1
    xcopy /Y "%PROJECT_ROOT%\frontend\.env*" "%BACKUP_DIR%\frontend\" >nul 2>&1
    xcopy /Y "%PROJECT_ROOT%\frontend\*.md" "%BACKUP_DIR%\frontend\" >nul 2>&1
    
    :: Copiar código fuente
    if exist "%PROJECT_ROOT%\frontend\src" xcopy /E /I /Y "%PROJECT_ROOT%\frontend\src" "%BACKUP_DIR%\frontend\src\" >nul 2>&1
    if exist "%PROJECT_ROOT%\frontend\public" xcopy /E /I /Y "%PROJECT_ROOT%\frontend\public" "%BACKUP_DIR%\frontend\public\" >nul 2>&1
    
    :: Copiar build si existe
    if exist "%PROJECT_ROOT%\frontend\dist" (
        echo [INFO] Copiando build de producción...
        xcopy /E /I /Y "%PROJECT_ROOT%\frontend\dist" "%BACKUP_DIR%\frontend\dist\" >nul 2>&1
    )
    
    echo [OK] Frontend copiado
) else (
    echo [WARNING] Directorio frontend no encontrado
)

echo.
echo ====================================
echo   FASE 4: BACKUP DE BASE DE DATOS
echo ====================================

echo [PASO 1] Verificando PostgreSQL...
where pg_dump >nul 2>&1
if errorlevel 1 (
    echo [WARNING] pg_dump no encontrado, saltando backup de BD
    goto :skip_db_backup
)

echo [PASO 2] Creando backup de PostgreSQL...
set PGPASSWORD=postgr3s
pg_dump -U postgres -h localhost -p 5432 localdb > "%BACKUP_DIR%\database\localdb_%TIMESTAMP%.sql" 2>&1
if errorlevel 1 (
    echo [WARNING] Error al crear backup de PostgreSQL
) else (
    echo [OK] Backup de PostgreSQL creado
)

echo.
echo [PASO 3] Exportando configuraciones de BD...
psql -U postgres -h localhost -p 5432 -d localdb -c "COPY (SELECT key, value FROM settings) TO STDOUT WITH CSV HEADER;" > "%BACKUP_DIR%\database\settings_%TIMESTAMP%.csv" 2>&1
if not errorlevel 1 (
    echo [OK] Configuraciones exportadas
)

:skip_db_backup
set PGPASSWORD=

echo.
echo ====================================
echo   FASE 5: BACKUP DE CONFIGURACIONES
echo ====================================

echo [PASO 1] Copiando archivos de configuración...
if exist "%PROJECT_ROOT%\docker-compose.yml" copy "%PROJECT_ROOT%\docker-compose.yml" "%BACKUP_DIR%\config\" >nul 2>&1
if exist "%PROJECT_ROOT%\.env" copy "%PROJECT_ROOT%\.env" "%BACKUP_DIR%\config\" >nul 2>&1
if exist "%PROJECT_ROOT%\README.md" copy "%PROJECT_ROOT%\README.md" "%BACKUP_DIR%\config\" >nul 2>&1

echo [OK] Configuraciones copiadas

echo.
echo [PASO 2] Copiando scripts de deployment...
xcopy /E /I /Y "%SCRIPT_DIR%*.bat" "%BACKUP_DIR%\scripts\" >nul 2>&1
xcopy /E /I /Y "%SCRIPT_DIR%*.ps1" "%BACKUP_DIR%\scripts\" >nul 2>&1
xcopy /E /I /Y "%SCRIPT_DIR%*.sql" "%BACKUP_DIR%\scripts\" >nul 2>&1
xcopy /E /I /Y "%SCRIPT_DIR%*.md" "%BACKUP_DIR%\scripts\" >nul 2>&1

echo [OK] Scripts copiados

echo.
echo ====================================
echo   FASE 6: BACKUP DE IIS (SI EXISTE)
echo ====================================

echo [PASO 1] Verificando instalación IIS...
if exist "C:\inetpub\wwwroot\dinqr" (
    echo [INFO] Instalación IIS encontrada, creando backup...
    mkdir "%BACKUP_DIR%\iis"
    
    :: Copiar configuraciones web.config
    if exist "C:\inetpub\wwwroot\dinqr\web.config" copy "C:\inetpub\wwwroot\dinqr\web.config" "%BACKUP_DIR%\iis\" >nul 2>&1
    if exist "C:\inetpub\wwwroot\dinqr\api\web.config" copy "C:\inetpub\wwwroot\dinqr\api\web.config" "%BACKUP_DIR%\iis\" >nul 2>&1
    
    :: Copiar logs de IIS
    if exist "C:\inetpub\wwwroot\dinqr\logs" xcopy /E /I /Y "C:\inetpub\wwwroot\dinqr\logs\*" "%BACKUP_DIR%\logs\iis\" >nul 2>&1
    
    :: Copiar uploads si existen
    if exist "C:\inetpub\wwwroot\dinqr\uploads" xcopy /E /I /Y "C:\inetpub\wwwroot\dinqr\uploads" "%BACKUP_DIR%\iis\uploads\" >nul 2>&1
    
    echo [OK] Backup IIS completado
) else (
    echo [INFO] No hay instalación IIS para respaldar
)

echo.
echo ====================================
echo   FASE 7: GENERACION DE METADATA
echo ====================================

echo [PASO 1] Creando manifiesto del backup...
set MANIFEST_FILE=%BACKUP_DIR%\backup_manifest.txt

echo DINQR - Manifiesto de Backup > %MANIFEST_FILE%
echo ============================= >> %MANIFEST_FILE%
echo. >> %MANIFEST_FILE%
echo Fecha de creación: %DATE% %TIME% >> %MANIFEST_FILE%
echo Timestamp: %TIMESTAMP% >> %MANIFEST_FILE%
echo Directorio origen: %PROJECT_ROOT% >> %MANIFEST_FILE%
echo Directorio backup: %BACKUP_DIR% >> %MANIFEST_FILE%
echo. >> %MANIFEST_FILE%
echo CONTENIDO: >> %MANIFEST_FILE%
echo. >> %MANIFEST_FILE%

:: Listar contenido del backup
echo BACKEND: >> %MANIFEST_FILE%
if exist "%BACKUP_DIR%\backend" dir "%BACKUP_DIR%\backend" /s /b >> %MANIFEST_FILE%
echo. >> %MANIFEST_FILE%

echo FRONTEND: >> %MANIFEST_FILE%
if exist "%BACKUP_DIR%\frontend" dir "%BACKUP_DIR%\frontend" /s /b >> %MANIFEST_FILE%
echo. >> %MANIFEST_FILE%

echo DATABASE: >> %MANIFEST_FILE%
if exist "%BACKUP_DIR%\database" dir "%BACKUP_DIR%\database" /b >> %MANIFEST_FILE%
echo. >> %MANIFEST_FILE%

echo LOGS: >> %MANIFEST_FILE%
if exist "%BACKUP_DIR%\logs" dir "%BACKUP_DIR%\logs" /s /b >> %MANIFEST_FILE%
echo. >> %MANIFEST_FILE%

echo [OK] Manifiesto creado

echo.
echo [PASO 2] Creando script de restauración...
set RESTORE_SCRIPT=%BACKUP_DIR%\restaurar_backup.bat

echo @echo off > %RESTORE_SCRIPT%
echo echo ==================================== >> %RESTORE_SCRIPT%
echo echo   RESTAURANDO BACKUP DINQR >> %RESTORE_SCRIPT%
echo echo ==================================== >> %RESTORE_SCRIPT%
echo. >> %RESTORE_SCRIPT%
echo echo [WARNING] Esto sobreescribirá la instalación actual >> %RESTORE_SCRIPT%
echo echo [INFO] Backup creado: %DATE% %TIME% >> %RESTORE_SCRIPT%
echo echo [INFO] Timestamp: %TIMESTAMP% >> %RESTORE_SCRIPT%
echo. >> %RESTORE_SCRIPT%
echo set /p CONFIRM="¿Continuar con la restauración? (S/N): " >> %RESTORE_SCRIPT%
echo if /i not "%%CONFIRM%%"=="S" exit /b 1 >> %RESTORE_SCRIPT%
echo. >> %RESTORE_SCRIPT%
echo echo [INFO] Restaurando archivos... >> %RESTORE_SCRIPT%
echo if exist "backend" xcopy /E /I /Y "backend\*" "%PROJECT_ROOT%\backend\" >> %RESTORE_SCRIPT%
echo if exist "frontend" xcopy /E /I /Y "frontend\*" "%PROJECT_ROOT%\frontend\" >> %RESTORE_SCRIPT%
echo. >> %RESTORE_SCRIPT%
echo echo [INFO] Restauración completada >> %RESTORE_SCRIPT%
echo echo [NEXT] Ejecutar migrar_base_datos.bat para restaurar BD >> %RESTORE_SCRIPT%
echo pause >> %RESTORE_SCRIPT%

echo [OK] Script de restauración creado

echo.
echo ====================================
echo   FASE 8: COMPRESION (OPCIONAL)
echo ====================================

if "%USE_7ZIP%"=="true" (
    echo [PASO 1] Comprimiendo backup...
    set ARCHIVE_FILE=%BACKUP_ROOT%\dinqr_backup_%TIMESTAMP%.7z
    
    7z a "%ARCHIVE_FILE%" "%BACKUP_DIR%\*" -mx=5 >nul 2>&1
    if errorlevel 1 (
        echo [WARNING] Error al comprimir, manteniendo carpeta
    ) else (
        echo [OK] Backup comprimido: %ARCHIVE_FILE%
        echo [INFO] ¿Eliminar carpeta temporal? (S/N)
        set /p DELETE_TEMP="Respuesta: "
        if /i "%DELETE_TEMP%"=="S" (
            rmdir /s /q "%BACKUP_DIR%"
            echo [OK] Carpeta temporal eliminada
        )
    )
) else (
    echo [INFO] Backup mantenido como carpeta: %BACKUP_DIR%
)

echo.
echo ====================================
echo   FASE 9: LIMPIEZA DE BACKUPS ANTIGUOS
echo ====================================

echo [PASO 1] Verificando backups antiguos...
set BACKUP_COUNT=0
for /d %%d in ("%BACKUP_ROOT%\dinqr_backup_*") do (
    set /a BACKUP_COUNT+=1
)

echo [INFO] Backups existentes: %BACKUP_COUNT%

if %BACKUP_COUNT% gtr 5 (
    echo [INFO] Hay más de 5 backups, ¿eliminar los más antiguos? (S/N)
    set /p CLEANUP="Respuesta: "
    if /i "%CLEANUP%"=="S" (
        echo [INFO] Eliminando backups antiguos...
        :: Eliminar los backups más antiguos (mantener solo los últimos 5)
        for /f "skip=5" %%d in ('dir "%BACKUP_ROOT%\dinqr_backup_*" /ad /od /b') do (
            rmdir /s /q "%BACKUP_ROOT%\%%d"
            echo [OK] Eliminado: %%d
        )
    )
)

echo.
echo ====================================
echo   BACKUP COMPLETADO
echo ====================================

echo.
echo [RESUMEN DEL BACKUP]
echo ✓ Backend: Archivos de código y configuración
echo ✓ Frontend: Código fuente y build
echo ✓ Base de datos: SQL dump y configuraciones
echo ✓ Logs: Archivos de log del sistema
echo ✓ Configuraciones: Archivos de ambiente
echo ✓ Scripts: Scripts de deployment
echo ✓ IIS: Configuraciones y uploads (si aplica)
echo.
echo [UBICACION DEL BACKUP]
if "%USE_7ZIP%"=="true" (
    if exist "%ARCHIVE_FILE%" (
        echo Archivo comprimido: %ARCHIVE_FILE%
    ) else (
        echo Carpeta: %BACKUP_DIR%
    )
) else (
    echo Carpeta: %BACKUP_DIR%
)
echo.
echo [ARCHIVOS IMPORTANTES]
echo - Manifiesto: %BACKUP_DIR%\backup_manifest.txt
echo - Restauración: %BACKUP_DIR%\restaurar_backup.bat
echo - DB Dump: %BACKUP_DIR%\database\localdb_%TIMESTAMP%.sql
echo.
echo [INSTRUCCIONES DE RESTAURACION]
echo 1. Extraer backup (si está comprimido)
echo 2. Ejecutar: restaurar_backup.bat
echo 3. Ejecutar: migrar_base_datos.bat
echo 4. Ejecutar: desplegar_iis.bat
echo.

:: Calcular tamaño del backup
if exist "%BACKUP_DIR%" (
    for /f "tokens=3" %%a in ('dir "%BACKUP_DIR%" /s /-c ^| find "bytes"') do set BACKUP_SIZE=%%a
    echo [INFO] Tamaño del backup: %BACKUP_SIZE% bytes
)

echo.
echo [INFO] Backup completado exitosamente
echo [TIMESTAMP] %TIMESTAMP%
echo.

:: Mantener ventana abierta
echo Presiona cualquier tecla para continuar...
pause >nul
