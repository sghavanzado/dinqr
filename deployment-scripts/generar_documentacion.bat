@echo off
echo ====================================
echo   GENERAR DOCUMENTACIÓN DINQR
echo ====================================

:: Configurar variables
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..
set DOC_DIR=%SCRIPT_DIR%documentation
set REPORT_FILE=%DOC_DIR%\deployment_report_%date:~-4,4%%date:~-10,2%%date:~-7,2%.html

:: Crear directorio de documentación
if not exist "%DOC_DIR%" mkdir "%DOC_DIR%"

echo [INFO] Generando documentación del despliegue...
echo [INFO] Archivo: %REPORT_FILE%

:: Generar reporte HTML
(
echo ^<!DOCTYPE html^>
echo ^<html lang="es"^>
echo ^<head^>
echo ^<meta charset="UTF-8"^>
echo ^<meta name="viewport" content="width=device-width, initial-scale=1.0"^>
echo ^<title^>Reporte de Despliegue DINQR^</title^>
echo ^<style^>
echo body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
echo .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1^); }
echo h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
echo h2 { color: #34495e; margin-top: 30px; }
echo h3 { color: #7f8c8d; }
echo .script-list { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr^)^); gap: 15px; margin: 20px 0; }
echo .script-item { background: #ecf0f1; padding: 15px; border-radius: 5px; border-left: 4px solid #3498db; }
echo .script-name { font-weight: bold; color: #2980b9; margin-bottom: 5px; }
echo .script-desc { font-size: 14px; color: #7f8c8d; }
echo .status-ok { color: #27ae60; }
echo .status-warning { color: #f39c12; }
echo .status-error { color: #e74c3c; }
echo .info-box { background: #e8f4fd; border: 1px solid #bee5eb; padding: 15px; margin: 15px 0; border-radius: 5px; }
echo .command-box { background: #f8f9fa; border: 1px solid #dee2e6; padding: 10px; margin: 10px 0; border-radius: 3px; font-family: monospace; }
echo table { width: 100%%; border-collapse: collapse; margin: 15px 0; }
echo th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
echo th { background-color: #f8f9fa; }
echo .footer { text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #dee2e6; color: #6c757d; }
echo ^</style^>
echo ^</head^>
echo ^<body^>
echo ^<div class="container"^>
echo ^<h1^>📋 Reporte de Despliegue DINQR^</h1^>
echo ^<p^>^<strong^>Fecha de generación:^</strong^> %date% %time%^</p^>
echo ^<p^>^<strong^>Servidor:^</strong^> %COMPUTERNAME%^</p^>
echo ^<p^>^<strong^>Usuario:^</strong^> %USERNAME%^</p^>
) > "%REPORT_FILE%"

:: Sección de información del proyecto
(
echo ^<h2^>🏗️ Información del Proyecto^</h2^>
echo ^<div class="info-box"^>
echo ^<p^>^<strong^>Nombre:^</strong^> DINQR - Sistema de Generación de Códigos QR^</p^>
echo ^<p^>^<strong^>Versión Backend:^</strong^> Flask + SQLAlchemy + PostgreSQL^</p^>
echo ^<p^>^<strong^>Versión Frontend:^</strong^> React + TypeScript + Material-UI^</p^>
echo ^<p^>^<strong^>Servidor Web:^</strong^> IIS (Internet Information Services^)^</p^>
echo ^<p^>^<strong^>Base de Datos:^</strong^> PostgreSQL^</p^>
echo ^</div^>
) >> "%REPORT_FILE%"

:: Listar scripts disponibles
(
echo ^<h2^>📜 Scripts de Despliegue Disponibles^</h2^>
echo ^<div class="script-list"^>
) >> "%REPORT_FILE%"

:: Array de scripts con descripciones
set "scripts[0]=instalar_completo.bat:Instalación automatizada completa del sistema"
set "scripts[1]=desinstalar.bat:Desinstalación completa del sistema"
set "scripts[2]=actualizar.bat:Actualización automatizada del sistema"
set "scripts[3]=compilar_backend.bat:Compilación del backend Flask"
set "scripts[4]=compilar_frontend.bat:Compilación del frontend React"
set "scripts[5]=compilar_todo.bat:Compilación completa (backend + frontend)"
set "scripts[6]=desplegar_iis.bat:Despliegue en IIS"
set "scripts[7]=configurar_iis.ps1:Configuración avanzada de IIS"
set "scripts[8]=configurar_ssl.ps1:Configuración SSL/HTTPS"
set "scripts[9]=instalar_dependencias.bat:Instalación de dependencias del sistema"
set "scripts[10]=configurar_postgresql.bat:Configuración de PostgreSQL"
set "scripts[11]=migrar_base_datos.bat:Migraciones de base de datos"
set "scripts[12]=configurar_ambiente.bat:Configuración de variables de entorno"
set "scripts[13]=verificar_sistema.bat:Verificación de prerrequisitos"
set "scripts[14]=monitoreo_salud.bat:Monitoreo de salud del sistema"
set "scripts[15]=reiniciar_servicios.bat:Reinicio de servicios"
set "scripts[16]=backup_aplicacion.bat:Backup completo del sistema"
set "scripts[17]=logs_aplicacion.bat:Monitoreo de logs en tiempo real"

:: Procesar cada script
for /L %%i in (0,1,17) do (
    setlocal enabledelayedexpansion
    for /f "tokens=1,2 delims=:" %%a in ("!scripts[%%i]!") do (
        set script_name=%%a
        set script_desc=%%b
        
        if exist "%SCRIPT_DIR%!script_name!" (
            (
            echo ^<div class="script-item"^>
            echo ^<div class="script-name"^>✅ !script_name!^</div^>
            echo ^<div class="script-desc"^>!script_desc!^</div^>
            echo ^</div^>
            ) >> "%REPORT_FILE%"
        ) else (
            (
            echo ^<div class="script-item"^>
            echo ^<div class="script-name"^>❌ !script_name!^</div^>
            echo ^<div class="script-desc"^>!script_desc! (NO ENCONTRADO^)^</div^>
            echo ^</div^>
            ) >> "%REPORT_FILE%"
        )
    )
    endlocal
)

(
echo ^</div^>
) >> "%REPORT_FILE%"

:: Verificar estado de servicios
(
echo ^<h2^>🔧 Estado de Servicios^</h2^>
echo ^<table^>
echo ^<tr^>^<th^>Servicio^</th^>^<th^>Estado^</th^>^<th^>Descripción^</th^>^</tr^>
) >> "%REPORT_FILE%"

:: Verificar IIS
sc query "W3SVC" | find "RUNNING" >nul 2>&1
if errorlevel 1 (
    echo ^<tr^>^<td^>IIS (W3SVC^)^</td^>^<td class="status-error"^>❌ Detenido^</td^>^<td^>Servicio web principal^</td^>^</tr^> >> "%REPORT_FILE%"
) else (
    echo ^<tr^>^<td^>IIS (W3SVC^)^</td^>^<td class="status-ok"^>✅ Ejecutándose^</td^>^<td^>Servicio web principal^</td^>^</tr^> >> "%REPORT_FILE%"
)

:: Verificar PostgreSQL
sc query "postgresql*" | find "RUNNING" >nul 2>&1
if errorlevel 1 (
    echo ^<tr^>^<td^>PostgreSQL^</td^>^<td class="status-error"^>❌ Detenido^</td^>^<td^>Base de datos^</td^>^</tr^> >> "%REPORT_FILE%"
) else (
    echo ^<tr^>^<td^>PostgreSQL^</td^>^<td class="status-ok"^>✅ Ejecutándose^</td^>^<td^>Base de datos^</td^>^</tr^> >> "%REPORT_FILE%"
)

:: Verificar sitio DINQR
%windir%\system32\inetsrv\appcmd.exe list site "DINQR" | find "Started" >nul 2>&1
if errorlevel 1 (
    echo ^<tr^>^<td^>Sitio DINQR^</td^>^<td class="status-warning"^>⚠️ No iniciado^</td^>^<td^>Aplicación web^</td^>^</tr^> >> "%REPORT_FILE%"
) else (
    echo ^<tr^>^<td^>Sitio DINQR^</td^>^<td class="status-ok"^>✅ Activo^</td^>^<td^>Aplicación web^</td^>^</tr^> >> "%REPORT_FILE%"
)

(
echo ^</table^>
) >> "%REPORT_FILE%"

:: Información del sistema
(
echo ^<h2^>💻 Información del Sistema^</h2^>
echo ^<table^>
echo ^<tr^>^<th^>Componente^</th^>^<th^>Valor^</th^>^</tr^>
) >> "%REPORT_FILE%"

:: Sistema operativo
for /f "tokens=2*" %%a in ('reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /v ProductName 2^>nul') do (
    echo ^<tr^>^<td^>Sistema Operativo^</td^>^<td^>%%b^</td^>^</tr^> >> "%REPORT_FILE%"
)

:: Arquitectura
echo ^<tr^>^<td^>Arquitectura^</td^>^<td^>%PROCESSOR_ARCHITECTURE%^</td^>^</tr^> >> "%REPORT_FILE%"

:: Memoria total
for /f "tokens=2 delims==" %%a in ('wmic computersystem get TotalPhysicalMemory /value ^| find "="') do (
    set /a mem_gb=%%a/1073741824
    echo ^<tr^>^<td^>Memoria Total^</td^>^<td^>!mem_gb! GB^</td^>^</tr^> >> "%REPORT_FILE%"
)

:: Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ^<tr^>^<td^>Python^</td^>^<td class="status-error"^>❌ No instalado^</td^>^</tr^> >> "%REPORT_FILE%"
) else (
    for /f "tokens=*" %%a in ('python --version 2^>^&1') do (
        echo ^<tr^>^<td^>Python^</td^>^<td class="status-ok"^>✅ %%a^</td^>^</tr^> >> "%REPORT_FILE%"
    )
)

:: Verificar Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ^<tr^>^<td^>Node.js^</td^>^<td class="status-error"^>❌ No instalado^</td^>^</tr^> >> "%REPORT_FILE%"
) else (
    for /f "tokens=*" %%a in ('node --version 2^>^&1') do (
        echo ^<tr^>^<td^>Node.js^</td^>^<td class="status-ok"^>✅ %%a^</td^>^</tr^> >> "%REPORT_FILE%"
    )
)

(
echo ^</table^>
) >> "%REPORT_FILE%"

:: Rutas importantes
(
echo ^<h2^>📁 Rutas Importantes^</h2^>
echo ^<table^>
echo ^<tr^>^<th^>Componente^</th^>^<th^>Ruta^</th^>^<th^>Estado^</th^>^</tr^>
) >> "%REPORT_FILE%"

:: Verificar rutas críticas
set "paths[0]=Proyecto:%PROJECT_ROOT%"
set "paths[1]=Scripts:%SCRIPT_DIR%"
set "paths[2]=Backend:%PROJECT_ROOT%\backend"
set "paths[3]=Frontend:%PROJECT_ROOT%\frontend"
set "paths[4]=IIS:C:\inetpub\wwwroot\dinqr"
set "paths[5]=Logs Backend:%PROJECT_ROOT%\backend\logs"
set "paths[6]=Logs Despliegue:%SCRIPT_DIR%deployment-logs"

for /L %%i in (0,1,6) do (
    setlocal enabledelayedexpansion
    for /f "tokens=1,2 delims=:" %%a in ("!paths[%%i]!") do (
        set path_name=%%a
        set path_value=%%b
        
        if exist "!path_value!" (
            echo ^<tr^>^<td^>!path_name!^</td^>^<td^>!path_value!^</td^>^<td class="status-ok"^>✅ Existe^</td^>^</tr^> >> "%REPORT_FILE%"
        ) else (
            echo ^<tr^>^<td^>!path_name!^</td^>^<td^>!path_value!^</td^>^<td class="status-error"^>❌ No encontrado^</td^>^</tr^> >> "%REPORT_FILE%"
        )
    )
    endlocal
)

(
echo ^</table^>
) >> "%REPORT_FILE%"

:: Guía rápida
(
echo ^<h2^>🚀 Guía Rápida de Uso^</h2^>
echo ^<div class="info-box"^>
echo ^<h3^>Para instalación nueva:^</h3^>
echo ^<div class="command-box"^>instalar_completo.bat^</div^>
echo ^<p^>Este comando ejecuta toda la instalación automáticamente.^</p^>
echo.
echo ^<h3^>Para monitoreo:^</h3^>
echo ^<div class="command-box"^>monitoreo_salud.bat^</div^>
echo ^<p^>Verifica el estado completo del sistema.^</p^>
echo.
echo ^<h3^>Para actualizar:^</h3^>
echo ^<div class="command-box"^>actualizar.bat^</div^>
echo ^<p^>Actualiza la aplicación desde el repositorio.^</p^>
echo.
echo ^<h3^>Para backup:^</h3^>
echo ^<div class="command-box"^>backup_aplicacion.bat^</div^>
echo ^<p^>Crea un backup completo del sistema.^</p^>
echo ^</div^>
) >> "%REPORT_FILE%"

:: URLs de acceso
(
echo ^<h2^>🌐 URLs de Acceso^</h2^>
echo ^<div class="info-box"^>
echo ^<ul^>
echo ^<li^>^<strong^>Frontend:^</strong^> ^<a href="http://localhost:8080"^>http://localhost:8080^</a^>^</li^>
echo ^<li^>^<strong^>API Backend:^</strong^> ^<a href="http://localhost:8080/api"^>http://localhost:8080/api^</a^>^</li^>
echo ^<li^>^<strong^>Documentación API:^</strong^> ^<a href="http://localhost:8080/api/apidocs"^>http://localhost:8080/api/apidocs^</a^>^</li^>
echo ^</ul^>
echo ^</div^>
) >> "%REPORT_FILE%"

:: Footer
(
echo ^<div class="footer"^>
echo ^<p^>Reporte generado automáticamente por el sistema de despliegue DINQR^</p^>
echo ^<p^>Para más información, consulta el README.md en la carpeta deployment-scripts^</p^>
echo ^</div^>
echo ^</div^>
echo ^</body^>
echo ^</html^>
) >> "%REPORT_FILE%"

echo [SUCCESS] Documentación generada exitosamente
echo [INFO] Archivo: %REPORT_FILE%
echo [INFO] Abriendo reporte en el navegador...

:: Abrir reporte en navegador predeterminado
start "" "%REPORT_FILE%"

echo.
echo [INFO] El reporte se ha guardado y abierto en tu navegador
echo [INFO] También puedes acceder al archivo directamente desde:
echo [INFO] %REPORT_FILE%

pause
