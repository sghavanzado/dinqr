# ====================================
# CONFIGURACIÓN MANUAL DE IIS PARA DINQR
# ====================================
# 
# Este archivo contiene todos los comandos PowerShell necesarios para
# configurar IIS manualmente para el proyecto DINQR.
# 
# INSTRUCCIONES DE USO:
# 1. Abrir PowerShell como Administrador
# 2. Copiar y pegar cada sección paso a paso
# 3. Verificar que cada comando se ejecute correctamente
# 4. Continuar con la siguiente sección
#
# NOTA: Si PowerShell está bloqueado, usar comandos DISM al final del archivo
#
# ====================================

# ====================================
# PASO 1: VERIFICAR PERMISOS
# ====================================

Write-Host "=== VERIFICANDO PERMISOS DE ADMINISTRADOR ===" -ForegroundColor Yellow

$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "[ERROR] Debe ejecutar PowerShell como Administrador" -ForegroundColor Red
    Write-Host "Click derecho en PowerShell > Ejecutar como administrador" -ForegroundColor Yellow
    Read-Host "Presiona Enter para continuar cuando ejecutes como Admin"
} else {
    Write-Host "[OK] Permisos de administrador confirmados" -ForegroundColor Green
}

# ====================================
# PASO 2: HABILITAR CARACTERÍSTICAS BÁSICAS DE IIS
# ====================================

Write-Host "=== HABILITANDO CARACTERÍSTICAS BÁSICAS DE IIS ===" -ForegroundColor Yellow

# Servicios básicos de IIS
Enable-WindowsOptionalFeature -Online -FeatureName IIS-WebServerRole -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-WebServer -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-CommonHttpFeatures -All

Write-Host "[OK] Características básicas habilitadas" -ForegroundColor Green

# ====================================
# PASO 3: CARACTERÍSTICAS HTTP COMUNES
# ====================================

Write-Host "=== CONFIGURANDO CARACTERÍSTICAS HTTP ===" -ForegroundColor Yellow

# Documentos y navegación
Enable-WindowsOptionalFeature -Online -FeatureName IIS-DefaultDocument -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-DirectoryBrowsing -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-StaticContent -All

# Manejo de errores y redirección
Enable-WindowsOptionalFeature -Online -FeatureName IIS-HttpErrors -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-HttpRedirect -All

Write-Host "[OK] Características HTTP configuradas" -ForegroundColor Green

# ====================================
# PASO 4: DESARROLLO DE APLICACIONES
# ====================================

Write-Host "=== CONFIGURANDO DESARROLLO DE APLICACIONES ===" -ForegroundColor Yellow

# .NET Framework y ASP.NET
Enable-WindowsOptionalFeature -Online -FeatureName IIS-NetFxExtensibility45 -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ASPNET45 -All

# CGI y ISAPI (necesario para Python/Flask)
Enable-WindowsOptionalFeature -Online -FeatureName IIS-CGI -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ISAPIExtensions -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ISAPIFilter -All

# Características adicionales de desarrollo
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ApplicationDevelopment -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ApplicationInit -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-WebSockets -All

Write-Host "[OK] Características de desarrollo configuradas" -ForegroundColor Green

# ====================================
# PASO 5: SEGURIDAD
# ====================================

Write-Host "=== CONFIGURANDO SEGURIDAD ===" -ForegroundColor Yellow

# Filtrado de solicitudes (esencial)
Enable-WindowsOptionalFeature -Online -FeatureName IIS-RequestFiltering -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-Security -All

# Autenticación
Enable-WindowsOptionalFeature -Online -FeatureName IIS-BasicAuthentication -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-WindowsAuthentication -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-DigestAuthentication -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ClientCertificateMappingAuthentication -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-IISCertificateMappingAuthentication -All

# Autorización y restricciones
Enable-WindowsOptionalFeature -Online -FeatureName IIS-URLAuthorization -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-IPSecurity -All

Write-Host "[OK] Características de seguridad configuradas" -ForegroundColor Green

# ====================================
# PASO 6: RENDIMIENTO Y COMPRESIÓN
# ====================================

Write-Host "=== CONFIGURANDO RENDIMIENTO ===" -ForegroundColor Yellow

# Compresión de contenido
Enable-WindowsOptionalFeature -Online -FeatureName IIS-HttpCompressionStatic -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-HttpCompressionDynamic -All

Write-Host "[OK] Características de rendimiento configuradas" -ForegroundColor Green

# ====================================
# PASO 7: LOGGING Y MONITOREO
# ====================================

Write-Host "=== CONFIGURANDO LOGGING ===" -ForegroundColor Yellow

# Registro y monitoreo
Enable-WindowsOptionalFeature -Online -FeatureName IIS-HttpLogging -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-CustomLogging -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-LoggingLibraries -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-HttpTracing -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ODBC -All

Write-Host "[OK] Características de logging configuradas" -ForegroundColor Green

# ====================================
# PASO 8: HERRAMIENTAS DE ADMINISTRACIÓN
# ====================================

Write-Host "=== CONFIGURANDO HERRAMIENTAS DE ADMINISTRACIÓN ===" -ForegroundColor Yellow

# Consola de administración
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ManagementConsole -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ManagementService -All

# Compatibilidad con IIS 6 (para herramientas legacy)
Enable-WindowsOptionalFeature -Online -FeatureName IIS-IIS6ManagementCompatibility -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-Metabase -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-WMICompatibility -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-LegacySnapIn -All
Enable-WindowsOptionalFeature -Online -FeatureName IIS-LegacyScripts -All

Write-Host "[OK] Herramientas de administración configuradas" -ForegroundColor Green

# ====================================
# PASO 9: CONFIGURACIÓN AVANZADA
# ====================================

Write-Host "=== CONFIGURACIÓN AVANZADA DE IIS ===" -ForegroundColor Yellow

# Desbloquear configuraciones importantes para aplicaciones personalizadas
& "$env:windir\system32\inetsrv\appcmd.exe" unlock config -section:system.webServer/handlers
& "$env:windir\system32\inetsrv\appcmd.exe" unlock config -section:system.webServer/modules
& "$env:windir\system32\inetsrv\appcmd.exe" unlock config -section:system.webServer/httpCompression
& "$env:windir\system32\inetsrv\appcmd.exe" unlock config -section:system.webServer/urlCompression

Write-Host "[OK] Configuraciones avanzadas aplicadas" -ForegroundColor Green

# ====================================
# PASO 10: VERIFICACIÓN DE INSTALACIÓN
# ====================================

Write-Host "=== VERIFICANDO INSTALACIÓN ===" -ForegroundColor Yellow

# Verificar que IIS esté funcionando
try {
    & "$env:windir\system32\inetsrv\appcmd.exe" list sites
    Write-Host "[OK] IIS está funcionando correctamente" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] IIS no está funcionando: $($_.Exception.Message)" -ForegroundColor Red
}

# Verificar servicio World Wide Web
$w3svc = Get-Service -Name W3SVC -ErrorAction SilentlyContinue
if ($w3svc -and $w3svc.Status -eq 'Running') {
    Write-Host "[OK] Servicio World Wide Web está corriendo" -ForegroundColor Green
} else {
    Write-Host "[WARNING] Servicio World Wide Web no está corriendo" -ForegroundColor Yellow
    Write-Host "Ejecutar: Start-Service W3SVC" -ForegroundColor Cyan
}

# Mostrar características habilitadas
Write-Host "=== CARACTERÍSTICAS IIS HABILITADAS ===" -ForegroundColor Cyan
Get-WindowsOptionalFeature -Online | Where-Object {$_.FeatureName -like "IIS-*" -and $_.State -eq "Enabled"} | Select-Object FeatureName, State

Write-Host "=== CONFIGURACIÓN COMPLETADA ===" -ForegroundColor Green
Write-Host "IIS ha sido configurado exitosamente para DINQR" -ForegroundColor Green
Write-Host ""
Write-Host "PRÓXIMOS PASOS:" -ForegroundColor Yellow
Write-Host "1. Descargar e instalar Application Request Routing (ARR)" -ForegroundColor White
Write-Host "   URL: https://www.iis.net/downloads/microsoft/application-request-routing" -ForegroundColor White
Write-Host "2. Crear sitio web DINQR en IIS Manager" -ForegroundColor White
Write-Host "3. Configurar proxy reverso para la API" -ForegroundColor White
Write-Host ""

# ====================================
# COMANDOS ALTERNATIVOS CON DISM
# ====================================
# 
# Si PowerShell no funciona debido a políticas de ejecución,
# copiar y pegar estos comandos en CMD como Administrador:
#
# ====================================

Write-Host "=== COMANDOS ALTERNATIVOS CON DISM ===" -ForegroundColor Magenta
Write-Host "Si PowerShell está bloqueado, usar estos comandos en CMD:" -ForegroundColor Yellow
Write-Host ""

$dismCommands = @"
@echo off
echo === CONFIGURANDO IIS CON DISM ===

REM Características básicas
dism /online /enable-feature /featurename:IIS-WebServerRole /all
dism /online /enable-feature /featurename:IIS-WebServer /all
dism /online /enable-feature /featurename:IIS-CommonHttpFeatures /all

REM Características HTTP
dism /online /enable-feature /featurename:IIS-DefaultDocument /all
dism /online /enable-feature /featurename:IIS-DirectoryBrowsing /all
dism /online /enable-feature /featurename:IIS-StaticContent /all
dism /online /enable-feature /featurename:IIS-HttpErrors /all
dism /online /enable-feature /featurename:IIS-HttpRedirect /all

REM Desarrollo de aplicaciones
dism /online /enable-feature /featurename:IIS-NetFxExtensibility45 /all
dism /online /enable-feature /featurename:IIS-ASPNET45 /all
dism /online /enable-feature /featurename:IIS-CGI /all
dism /online /enable-feature /featurename:IIS-ISAPIExtensions /all
dism /online /enable-feature /featurename:IIS-ISAPIFilter /all
dism /online /enable-feature /featurename:IIS-ApplicationDevelopment /all
dism /online /enable-feature /featurename:IIS-ApplicationInit /all
dism /online /enable-feature /featurename:IIS-WebSockets /all

REM Seguridad
dism /online /enable-feature /featurename:IIS-RequestFiltering /all
dism /online /enable-feature /featurename:IIS-Security /all
dism /online /enable-feature /featurename:IIS-BasicAuthentication /all
dism /online /enable-feature /featurename:IIS-WindowsAuthentication /all
dism /online /enable-feature /featurename:IIS-URLAuthorization /all
dism /online /enable-feature /featurename:IIS-IPSecurity /all

REM Rendimiento
dism /online /enable-feature /featurename:IIS-HttpCompressionStatic /all
dism /online /enable-feature /featurename:IIS-HttpCompressionDynamic /all

REM Logging
dism /online /enable-feature /featurename:IIS-HttpLogging /all
dism /online /enable-feature /featurename:IIS-CustomLogging /all
dism /online /enable-feature /featurename:IIS-LoggingLibraries /all
dism /online /enable-feature /featurename:IIS-HttpTracing /all

REM Administración
dism /online /enable-feature /featurename:IIS-ManagementConsole /all
dism /online /enable-feature /featurename:IIS-IIS6ManagementCompatibility /all
dism /online /enable-feature /featurename:IIS-Metabase /all

echo === CONFIGURACIÓN COMPLETADA ===
echo IIS configurado exitosamente
pause
"@

Write-Host $dismCommands -ForegroundColor White

# Guardar comandos DISM en archivo
$dismFile = "$PSScriptRoot\configurar_iis_dism.bat"
$dismCommands | Out-File -FilePath $dismFile -Encoding ASCII
Write-Host ""
Write-Host "Comandos DISM guardados en: $dismFile" -ForegroundColor Green
Write-Host "Ejecutar ese archivo si PowerShell no funciona" -ForegroundColor Yellow

Write-Host ""
Write-Host "=== CONFIGURACIÓN DE IIS COMPLETADA ===" -ForegroundColor Green
Write-Host "Archivo de configuración manual creado exitosamente" -ForegroundColor Green
