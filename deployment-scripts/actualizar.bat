@echo off
echo ====================================
echo   ACTUALIZAR DINQR
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
set LOG_FILE=%LOG_DIR%\actualizacion_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.log

:: Crear directorio de logs si no existe
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

echo [INFO] Iniciando actualización de DINQR...
echo [INFO] Log: %LOG_FILE%

echo [%date% %time%] INICIO: Actualización de DINQR >> "%LOG_FILE%"

echo.
echo [WARNING] Esta operación realizará:
echo [WARNING] - Backup del sistema actual
echo [WARNING] - Actualización del código fuente
echo [WARNING] - Recompilación de la aplicación
echo [WARNING] - Migración de base de datos (si es necesaria)
echo [WARNING] - Reinicio de servicios

echo.
set /p confirm="¿Continuar con la actualización? (s/N): "
if /i not "%confirm%"=="s" (
    echo [INFO] Actualización cancelada por el usuario
    echo [%date% %time%] INFO: Actualización cancelada >> "%LOG_FILE%"
    pause
    exit /b 0
)

echo.
echo ====================================
echo   PASO 1: BACKUP PRE-ACTUALIZACIÓN
echo ====================================

echo [INFO] Creando backup del sistema actual...
echo [%date% %time%] INFO: Iniciando backup pre-actualización >> "%LOG_FILE%"

call "%SCRIPT_DIR%backup_aplicacion.bat"
if errorlevel 1 (
    echo [ERROR] Backup falló - Abortando actualización
    echo [%date% %time%] ERROR: Backup falló >> "%LOG_FILE%"
    pause
    exit /b 1
)

echo [OK] Backup completado
echo [%date% %time%] OK: Backup completado >> "%LOG_FILE%"

echo.
echo ====================================
echo   PASO 2: VERIFICAR ACTUALIZACIONES
echo ====================================

echo [INFO] Verificando actualizaciones disponibles...

cd /d "%PROJECT_ROOT%"

:: Verificar si es un repositorio git
if not exist ".git" (
    echo [ERROR] El proyecto no es un repositorio Git
    echo [ERROR] Actualización manual requerida
    echo [%date% %time%] ERROR: No es repositorio Git >> "%LOG_FILE%"
    pause
    exit /b 1
)

:: Obtener información del repositorio remoto
echo [INFO] Obteniendo información del repositorio...
git fetch origin >nul 2>&1
if errorlevel 1 (
    echo [WARNING] No se pudo conectar al repositorio remoto
    echo [WARNING] Continuando con actualizaciones locales...
    echo [%date% %time%] WARNING: No conexión a repositorio remoto >> "%LOG_FILE%"
    set remote_available=false
) else (
    echo [OK] Conexión al repositorio remoto establecida
    echo [%date% %time%] OK: Conexión a repositorio remoto >> "%LOG_FILE%"
    set remote_available=true
)

:: Verificar cambios pendientes
git status --porcelain > temp_status.txt 2>&1
set /p has_changes=<temp_status.txt
del temp_status.txt

if not "%has_changes%"=="" (
    echo [WARNING] Hay cambios locales no confirmados
    echo [WARNING] Estos cambios pueden perderse durante la actualización
    
    echo.
    echo Cambios detectados:
    git status --short
    
    echo.
    set /p backup_changes="¿Hacer stash de los cambios locales? (s/N): "
    if /i "%backup_changes%"=="s" (
        echo [INFO] Guardando cambios locales...
        git stash push -m "Backup automático antes de actualización %date% %time%"
        echo [OK] Cambios guardados en stash
        echo [%date% %time%] OK: Cambios guardados en stash >> "%LOG_FILE%"
    )
)

echo.
echo ====================================
echo   PASO 3: DETENER SERVICIOS
echo ====================================

echo [INFO] Deteniendo servicios para actualización...
echo [%date% %time%] INFO: Deteniendo servicios >> "%LOG_FILE%"

%windir%\system32\inetsrv\appcmd.exe stop site "DINQR" >nul 2>&1
%windir%\system32\inetsrv\appcmd.exe stop apppool "DinqrAppPool" >nul 2>&1

echo [OK] Servicios detenidos
echo [%date% %time%] OK: Servicios detenidos >> "%LOG_FILE%"

echo.
echo ====================================
echo   PASO 4: ACTUALIZAR CÓDIGO FUENTE
echo ====================================

if "%remote_available%"=="true" (
    echo [INFO] Actualizando desde repositorio remoto...
    
    :: Mostrar commits pendientes
    echo [INFO] Nuevos commits disponibles:
    git log --oneline HEAD..origin/main 2>nul
    
    echo [INFO] Aplicando actualizaciones...
    git pull origin main
    if errorlevel 1 (
        echo [ERROR] Error al actualizar código fuente
        echo [%date% %time%] ERROR: Error en git pull >> "%LOG_FILE%"
        goto :restore_services
    )
    
    echo [OK] Código fuente actualizado
    echo [%date% %time%] OK: Código fuente actualizado >> "%LOG_FILE%"
) else (
    echo [INFO] Actualización desde repositorio remoto no disponible
    echo [INFO] Usando código local actual
    echo [%date% %time%] INFO: Usando código local >> "%LOG_FILE%"
)

echo.
echo ====================================
echo   PASO 5: ACTUALIZAR DEPENDENCIAS
echo ====================================

echo [INFO] Actualizando dependencias del backend...
cd /d "%PROJECT_ROOT%\backend"

:: Verificar si requirements.txt cambió
git diff HEAD~1 requirements.txt >nul 2>&1
if not errorlevel 1 (
    echo [INFO] requirements.txt cambió - Actualizando dependencias Python...
    pip install -r requirements.txt --upgrade
    echo [%date% %time%] INFO: Dependencias Python actualizadas >> "%LOG_FILE%"
) else (
    echo [INFO] No hay cambios en requirements.txt
)

echo [INFO] Actualizando dependencias del frontend...
cd /d "%PROJECT_ROOT%\frontend"

:: Verificar si package.json cambió
git diff HEAD~1 package.json >nul 2>&1
if not errorlevel 1 (
    echo [INFO] package.json cambió - Actualizando dependencias Node.js...
    npm install
    echo [%date% %time%] INFO: Dependencias Node.js actualizadas >> "%LOG_FILE%"
) else (
    echo [INFO] No hay cambios en package.json
)

echo.
echo ====================================
echo   PASO 6: VERIFICAR MIGRACIONES
echo ====================================

echo [INFO] Verificando migraciones de base de datos...
cd /d "%PROJECT_ROOT%\backend"

:: Verificar si hay nuevas migraciones
python -c "from flask_migrate import current; print('current')" >nul 2>&1
if not errorlevel 1 (
    echo [INFO] Verificando estado de migraciones...
    
    :: Ejecutar migraciones pendientes
    call "%SCRIPT_DIR%migrar_base_datos.bat"
    if errorlevel 1 (
        echo [WARNING] Error en migraciones - Continuando con precaución
        echo [%date% %time%] WARNING: Error en migraciones >> "%LOG_FILE%"
    ) else (
        echo [OK] Migraciones aplicadas exitosamente
        echo [%date% %time%] OK: Migraciones aplicadas >> "%LOG_FILE%"
    )
)

echo.
echo ====================================
echo   PASO 7: RECOMPILAR APLICACIÓN
echo ====================================

echo [INFO] Recompilando aplicación...
echo [%date% %time%] INFO: Iniciando recompilación >> "%LOG_FILE%"

call "%SCRIPT_DIR%compilar_todo.bat"
if errorlevel 1 (
    echo [ERROR] Error en la compilación
    echo [%date% %time%] ERROR: Error en compilación >> "%LOG_FILE%"
    goto :restore_services
)

echo [OK] Aplicación recompilada exitosamente
echo [%date% %time%] OK: Aplicación recompilada >> "%LOG_FILE%"

echo.
echo ====================================
echo   PASO 8: ACTUALIZAR CONFIGURACIÓN IIS
echo ====================================

echo [INFO] Actualizando configuración de IIS...

:: Verificar si web.config cambió
cd /d "%PROJECT_ROOT%"
git diff HEAD~1 web.config >nul 2>&1
if not errorlevel 1 (
    echo [INFO] web.config cambió - Aplicando nueva configuración...
    
    :: Redeployar configuración de IIS
    call "%SCRIPT_DIR%desplegar_iis.bat"
    if errorlevel 1 (
        echo [WARNING] Error actualizando configuración IIS
        echo [%date% %time%] WARNING: Error actualizando IIS >> "%LOG_FILE%"
    )
) else (
    echo [INFO] No hay cambios en configuración de IIS
)

echo.
echo ====================================
echo   PASO 9: REINICIAR SERVICIOS
echo ====================================

:restore_services
echo [INFO] Reiniciando servicios...
echo [%date% %time%] INFO: Reiniciando servicios >> "%LOG_FILE%"

call "%SCRIPT_DIR%reiniciar_servicios.bat"
if errorlevel 1 (
    echo [ERROR] Error al reiniciar servicios
    echo [%date% %time%] ERROR: Error reiniciando servicios >> "%LOG_FILE%"
    goto :error
)

echo [OK] Servicios reiniciados
echo [%date% %time%] OK: Servicios reiniciados >> "%LOG_FILE%"

echo.
echo ====================================
echo   PASO 10: VERIFICACIÓN POST-ACTUALIZACIÓN
echo ====================================

echo [INFO] Verificando sistema después de la actualización...
echo [%date% %time%] INFO: Verificación post-actualización >> "%LOG_FILE%"

call "%SCRIPT_DIR%monitoreo_salud.bat"

echo.
echo ====================================
echo   ACTUALIZACIÓN COMPLETADA
echo ====================================

echo [SUCCESS] ¡DINQR ha sido actualizado exitosamente!
echo [%date% %time%] SUCCESS: Actualización completada >> "%LOG_FILE%"

:: Obtener información de la nueva versión
cd /d "%PROJECT_ROOT%"
for /f "delims=" %%i in ('git rev-parse --short HEAD') do set current_commit=%%i
for /f "delims=" %%i in ('git log -1 --format^=^"%%s^"') do set last_commit_msg=%%i

echo.
echo [INFO] Información de la actualización:
echo [INFO] - Commit actual: %current_commit%
echo [INFO] - Último cambio: %last_commit_msg%
echo [INFO] - Fecha de actualización: %date% %time%

echo.
echo [INFO] URLs de acceso (verificar funcionamiento):
echo [INFO] - Frontend: http://localhost:8080
echo [INFO] - API: http://localhost:8080/api
echo [INFO] - Documentación: http://localhost:8080/api/apidocs

echo.
echo [INFO] Logs y recursos:
echo [INFO] - Log de actualización: %LOG_FILE%
echo [INFO] - Para monitoreo: monitoreo_salud.bat
echo [INFO] - Para logs en tiempo real: logs_aplicacion.bat

echo.
echo [INFO] En caso de problemas:
echo [INFO] - Revisa el log de actualización
echo [INFO] - Ejecuta monitoreo_salud.bat
echo [INFO] - Restaura desde el backup si es necesario

goto :end

:error
echo [ERROR] La actualización falló
echo [ERROR] Revisa el log para más detalles: %LOG_FILE%
echo [%date% %time%] ERROR: Actualización falló >> "%LOG_FILE%"

echo.
echo [INFO] El sistema puede estar en un estado inconsistente
echo [INFO] Recomendaciones:
echo [INFO] 1. Revisar logs de error
echo [INFO] 2. Intentar reiniciar servicios manualmente
echo [INFO] 3. Restaurar desde backup si es necesario
echo [INFO] 4. Contactar soporte técnico

pause
exit /b 1

:end
echo.
echo [SUCCESS] Actualización completada satisfactoriamente
echo [INFO] Sistema listo para uso
pause
