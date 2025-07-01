# Script de Configuración de IIS para DINQR
# Debe ejecutarse como Administrador con PowerShell

param(
    [string]$SiteName = "DINQR",
    [int]$Port = 8080,
    [string]$SitePath = "C:\inetpub\wwwroot\dinqr"
)

Write-Host "=====================================" -ForegroundColor Green
Write-Host "   CONFIGURANDO IIS PARA DINQR" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# Verificar permisos de administrador
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator"))
{
    Write-Host "[ERROR] Este script debe ejecutarse como Administrador" -ForegroundColor Red
    Write-Host "[INFO] Ejecuta PowerShell como Administrador" -ForegroundColor Yellow
    Read-Host "Presiona Enter para continuar..."
    exit 1
}

Write-Host "[INFO] Configurando IIS para el sitio: $SiteName" -ForegroundColor Cyan
Write-Host "[INFO] Puerto: $Port" -ForegroundColor Cyan
Write-Host "[INFO] Directorio: $SitePath" -ForegroundColor Cyan

# Importar módulo de IIS
Import-Module WebAdministration -ErrorAction SilentlyContinue

if (-not (Get-Module WebAdministration)) {
    Write-Host "[ERROR] Módulo WebAdministration no disponible" -ForegroundColor Red
    Write-Host "[INFO] Instala las herramientas de administración de IIS" -ForegroundColor Yellow
    Read-Host "Presiona Enter para continuar..."
    exit 1
}

Write-Host "`n[PASO 1] Habilitando características de IIS..." -ForegroundColor Yellow

# Habilitar características necesarias de IIS
$features = @(
    "IIS-WebServerRole",
    "IIS-WebServer", 
    "IIS-CommonHttpFeatures",
    "IIS-HttpErrors",
    "IIS-HttpLogging",
    "IIS-RequestFiltering",
    "IIS-StaticContent",
    "IIS-DefaultDocument",
    "IIS-DirectoryBrowsing",
    "IIS-CGI",
    "IIS-ISAPIExtensions",
    "IIS-ISAPIFilter",
    "IIS-HttpRedirect",
    "IIS-ManagementConsole"
)

foreach ($feature in $features) {
    try {
        Enable-WindowsOptionalFeature -Online -FeatureName $feature -All -NoRestart -WarningAction SilentlyContinue | Out-Null
        Write-Host "  ✓ $feature habilitado" -ForegroundColor Green
    }
    catch {
        Write-Host "  ⚠ Error habilitando $feature" -ForegroundColor Yellow
    }
}

Write-Host "`n[PASO 2] Configurando Application Pools..." -ForegroundColor Yellow

# Crear Application Pool para DINQR
$poolName = "DINQR_Pool"
if (Get-IISAppPool -Name $poolName -ErrorAction SilentlyContinue) {
    Remove-WebAppPool -Name $poolName
    Write-Host "  ✓ Pool anterior eliminado: $poolName" -ForegroundColor Green
}

New-WebAppPool -Name $poolName
Set-ItemProperty -Path "IIS:\AppPools\$poolName" -Name processModel.identityType -Value ApplicationPoolIdentity
Set-ItemProperty -Path "IIS:\AppPools\$poolName" -Name recycling.periodicRestart.time -Value "00:00:00"
Set-ItemProperty -Path "IIS:\AppPools\$poolName" -Name processModel.idleTimeout -Value "00:00:00"
Set-ItemProperty -Path "IIS:\AppPools\$poolName" -Name managedRuntimeVersion -Value ""

Write-Host "  ✓ Application Pool creado: $poolName" -ForegroundColor Green

Write-Host "`n[PASO 3] Configurando sitio web..." -ForegroundColor Yellow

# Eliminar sitio anterior si existe
if (Get-Website -Name $SiteName -ErrorAction SilentlyContinue) {
    Remove-Website -Name $SiteName
    Write-Host "  ✓ Sitio anterior eliminado: $SiteName" -ForegroundColor Green
}

# Crear sitio web
New-Website -Name $SiteName -PhysicalPath $SitePath -Port $Port -ApplicationPool $poolName
Write-Host "  ✓ Sitio web creado: $SiteName" -ForegroundColor Green

Write-Host "`n[PASO 4] Configurando aplicación virtual para API..." -ForegroundColor Yellow

# Crear Application Pool para API
$apiPoolName = "DINQR_API_Pool"
if (Get-IISAppPool -Name $apiPoolName -ErrorAction SilentlyContinue) {
    Remove-WebAppPool -Name $apiPoolName
}

New-WebAppPool -Name $apiPoolName
Set-ItemProperty -Path "IIS:\AppPools\$apiPoolName" -Name processModel.identityType -Value ApplicationPoolIdentity
Set-ItemProperty -Path "IIS:\AppPools\$apiPoolName" -Name managedRuntimeVersion -Value ""
Set-ItemProperty -Path "IIS:\AppPools\$apiPoolName" -Name processModel.idleTimeout -Value "00:00:00"

# Crear aplicación virtual para API
$apiPath = Join-Path $SitePath "api"
New-WebApplication -Site $SiteName -Name "api" -PhysicalPath $apiPath -ApplicationPool $apiPoolName

Write-Host "  ✓ Aplicación virtual API configurada" -ForegroundColor Green

Write-Host "`n[PASO 5] Configurando FastCGI..." -ForegroundColor Yellow

# Configurar FastCGI para Python
$pythonPath = Join-Path $apiPath "venv_production\Scripts\python.exe"
$wfastcgiPath = Join-Path $apiPath "wfastcgi.py"

# Limpiar configuraciones FastCGI anteriores
$existingConfig = Get-WebConfiguration -Filter "system.webServer/fastCgi/application[@fullPath='$pythonPath']" -PSPath "IIS:\"
if ($existingConfig) {
    Clear-WebConfiguration -Filter "system.webServer/fastCgi/application[@fullPath='$pythonPath']" -PSPath "IIS:\"
}

# Agregar configuración FastCGI
Add-WebConfiguration -Filter "system.webServer/fastCgi" -Value @{
    fullPath = $pythonPath
    arguments = $wfastcgiPath
    maxInstances = 4
    idleTimeout = 1800
    activityTimeout = 30
    requestTimeout = 90
    instanceMaxRequests = 10000
    protocol = "NamedPipe"
    flushNamedPipe = $false
} -PSPath "IIS:\"

Write-Host "  ✓ FastCGI configurado para Python" -ForegroundColor Green

Write-Host "`n[PASO 6] Configurando handlers..." -ForegroundColor Yellow

# Configurar handler para Python en la aplicación API
Set-WebConfiguration -Filter "system.webServer/handlers" -Value @{
    name = "Python FastCGI"
    path = "*"
    verb = "*"
    modules = "FastCgiModule"
    scriptProcessor = "$pythonPath|$wfastcgiPath"
    resourceType = "Unspecified"
    requireAccess = "Script"
} -PSPath "IIS:\Sites\$SiteName\api"

Write-Host "  ✓ Handlers configurados" -ForegroundColor Green

Write-Host "`n[PASO 7] Configurando variables de entorno..." -ForegroundColor Yellow

# Configurar variables de entorno para FastCGI
$envVars = @(
    @{ name = "WSGI_HANDLER"; value = "wsgi.application" },
    @{ name = "PYTHONPATH"; value = $apiPath },
    @{ name = "FLASK_ENV"; value = "production" },
    @{ name = "WSGI_LOG"; value = Join-Path $SitePath "logs\wfastcgi.log" }
)

foreach ($envVar in $envVars) {
    Add-WebConfiguration -Filter "system.webServer/fastCgi/application[@fullPath='$pythonPath']/environmentVariables" -Value $envVar -PSPath "IIS:\"
}

Write-Host "  ✓ Variables de entorno configuradas" -ForegroundColor Green

Write-Host "`n[PASO 8] Configurando permisos..." -ForegroundColor Yellow

# Configurar permisos para IIS
$acl = Get-Acl $SitePath
$accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule("IIS_IUSRS","FullControl","ContainerInherit,ObjectInherit","None","Allow")
$acl.SetAccessRule($accessRule)
$accessRule2 = New-Object System.Security.AccessControl.FileSystemAccessRule("IUSR","FullControl","ContainerInherit,ObjectInherit","None","Allow")
$acl.SetAccessRule($accessRule2)
Set-Acl -Path $SitePath -AclObject $acl

Write-Host "  ✓ Permisos configurados" -ForegroundColor Green

Write-Host "`n[PASO 9] Configurando URL Rewrite..." -ForegroundColor Yellow

# Verificar si URL Rewrite está instalado
$rewriteModule = Get-WebGlobalModule -Name "RewriteModule" -ErrorAction SilentlyContinue
if (-not $rewriteModule) {
    Write-Host "  ⚠ URL Rewrite Module no está instalado" -ForegroundColor Yellow
    Write-Host "  [INFO] Descarga desde: https://www.iis.net/downloads/microsoft/url-rewrite" -ForegroundColor Cyan
} else {
    Write-Host "  ✓ URL Rewrite Module disponible" -ForegroundColor Green
}

Write-Host "`n[PASO 10] Configurando logging..." -ForegroundColor Yellow

# Configurar logging para el sitio
Set-WebConfiguration -Filter "system.webServer/httpLogging" -Value @{
    dontLog = $false
    logExtFileFlags = "Date,Time,ClientIP,UserName,SiteName,ComputerName,ServerIP,Method,UriStem,UriQuery,HttpStatus,Win32Status,BytesSent,BytesRecv,TimeTaken,ServerPort,UserAgent,Cookie,Referer,ProtocolVersion,Host,HttpSubStatus"
} -PSPath "IIS:\Sites\$SiteName"

Write-Host "  ✓ Logging configurado" -ForegroundColor Green

Write-Host "`n[PASO 11] Iniciando servicios..." -ForegroundColor Yellow

# Iniciar Application Pools
Start-WebAppPool -Name $poolName
Start-WebAppPool -Name $apiPoolName

# Iniciar sitio web
Start-Website -Name $SiteName

Write-Host "  ✓ Servicios iniciados" -ForegroundColor Green

Write-Host "`n[PASO 12] Verificando configuración..." -ForegroundColor Yellow

# Verificar que el sitio esté funcionando
$site = Get-Website -Name $SiteName
$apiApp = Get-WebApplication -Site $SiteName -Name "api"

if ($site.State -eq "Started") {
    Write-Host "  ✓ Sitio principal: Funcionando" -ForegroundColor Green
} else {
    Write-Host "  ✗ Sitio principal: No funcionando" -ForegroundColor Red
}

if ($apiApp) {
    Write-Host "  ✓ Aplicación API: Configurada" -ForegroundColor Green
} else {
    Write-Host "  ✗ Aplicación API: Error" -ForegroundColor Red
}

Write-Host "`n=====================================" -ForegroundColor Green
Write-Host "   CONFIGURACION COMPLETADA" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

Write-Host "`n[RESUMEN DE CONFIGURACION]" -ForegroundColor Cyan
Write-Host "✓ Sitio: $SiteName" -ForegroundColor Green
Write-Host "✓ Puerto: $Port" -ForegroundColor Green
Write-Host "✓ Directorio: $SitePath" -ForegroundColor Green
Write-Host "✓ Application Pool Principal: $poolName" -ForegroundColor Green
Write-Host "✓ Application Pool API: $apiPoolName" -ForegroundColor Green
Write-Host "✓ FastCGI: Configurado" -ForegroundColor Green
Write-Host "✓ Permisos: Configurados" -ForegroundColor Green

Write-Host "`n[URLS DE ACCESO]" -ForegroundColor Cyan
Write-Host "- Frontend: http://localhost:$Port" -ForegroundColor White
Write-Host "- API: http://localhost:$Port/api" -ForegroundColor White
Write-Host "- IIS Manager: inetmgr" -ForegroundColor White

Write-Host "`n[COMANDOS UTILES]" -ForegroundColor Cyan
Write-Host "- Reiniciar sitio: Restart-Website -Name '$SiteName'" -ForegroundColor White
Write-Host "- Ver logs: Get-Content '$SitePath\logs\wfastcgi.log'" -ForegroundColor White
Write-Host "- Estado del sitio: Get-Website -Name '$SiteName'" -ForegroundColor White

# Crear archivo de configuración para referencia
$configFile = Join-Path (Split-Path $PSScriptRoot -Parent) "deployment-scripts\iis-config.txt"
@"
DINQR - Configuración de IIS
============================

Fecha de configuración: $(Get-Date)
Sitio: $SiteName
Puerto: $Port
Directorio: $SitePath
Application Pool Principal: $poolName
Application Pool API: $apiPoolName
Python: $pythonPath

URLs:
- Frontend: http://localhost:$Port
- API: http://localhost:$Port/api

Comandos PowerShell útiles:
- Get-Website -Name '$SiteName'
- Restart-Website -Name '$SiteName'
- Get-WebApplication -Site '$SiteName'
- Get-IISAppPool -Name '$poolName'
"@ | Out-File -FilePath $configFile -Encoding UTF8

Write-Host "`n[INFO] Configuración guardada en: $configFile" -ForegroundColor Cyan

Write-Host "`nPresiona Enter para continuar..." -ForegroundColor Yellow
Read-Host
