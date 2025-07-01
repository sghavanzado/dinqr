# Script PowerShell para Habilitar Características IIS para DINQR
# Ejecutar como Administrador

param(
    [switch]$Force = $false,
    [switch]$Verify = $false
)

Write-Host "=====================================" -ForegroundColor Green
Write-Host "   CONFIGURANDO CARACTERÍSTICAS IIS" -ForegroundColor Green
Write-Host "   PARA DINQR" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# Verificar permisos de administrador
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator"))
{
    Write-Host "[ERROR] Este script debe ejecutarse como Administrador" -ForegroundColor Red
    Write-Host "[INFO] Ejecuta PowerShell como Administrador" -ForegroundColor Yellow
    Read-Host "Presiona Enter para continuar..."
    exit 1
}

Write-Host "[INFO] Configurando IIS para DINQR..." -ForegroundColor Cyan

# Lista de características necesarias para DINQR
$RequiredFeatures = @(
    # Características básicas de IIS
    "IIS-WebServerRole",
    "IIS-WebServer",
    "IIS-CommonHttpFeatures",
    "IIS-HttpErrors",
    "IIS-HttpLogging",
    "IIS-RequestFiltering",
    "IIS-StaticContent",
    "IIS-DefaultDocument",
    "IIS-DirectoryBrowsing",
    
    # Desarrollo de aplicaciones
    "IIS-ApplicationDevelopment",
    "IIS-NetFxExtensibility45",
    "IIS-ASPNET45",
    "IIS-CGI",
    "IIS-ISAPIExtensions",
    "IIS-ISAPIFilter",
    "IIS-ServerSideIncludes",
    "IIS-WebSockets",
    "IIS-ApplicationInit",
    
    # Seguridad
    "IIS-Security",
    "IIS-BasicAuthentication",
    "IIS-WindowsAuthentication",
    "IIS-DigestAuthentication",
    "IIS-ClientCertificateMappingAuthentication",
    "IIS-IISCertificateMappingAuthentication",
    "IIS-URLAuthorization",
    "IIS-IPSecurity",
    
    # Rendimiento
    "IIS-Performance",
    "IIS-HttpCompressionStatic",
    "IIS-HttpCompressionDynamic",
    
    # Redirección
    "IIS-HttpRedirect",
    
    # Diagnóstico
    "IIS-HttpTracing",
    "IIS-CustomLogging",
    "IIS-LoggingLibraries",
    "IIS-ODBC",
    
    # Herramientas de administración
    "IIS-ManagementConsole",
    "IIS-IIS6ManagementCompatibility",
    "IIS-Metabase",
    "IIS-WMICompatibility",
    "IIS-LegacySnapIn",
    "IIS-LegacyScripts",
    "IIS-ManagementService"
)

if ($Verify) {
    Write-Host "`n[VERIFICACIÓN] Comprobando características instaladas..." -ForegroundColor Yellow
    
    $installedCount = 0
    $notInstalledCount = 0
    
    foreach ($feature in $RequiredFeatures) {
        $featureState = Get-WindowsOptionalFeature -Online -FeatureName $feature -ErrorAction SilentlyContinue
        
        if ($featureState -and $featureState.State -eq "Enabled") {
            Write-Host "✅ $feature - HABILITADO" -ForegroundColor Green
            $installedCount++
        } else {
            Write-Host "❌ $feature - NO HABILITADO" -ForegroundColor Red
            $notInstalledCount++
        }
    }
    
    Write-Host "`n[RESUMEN VERIFICACIÓN]" -ForegroundColor Cyan
    Write-Host "Características habilitadas: $installedCount" -ForegroundColor Green
    Write-Host "Características faltantes: $notInstalledCount" -ForegroundColor Red
    Write-Host "Total requeridas: $($RequiredFeatures.Count)" -ForegroundColor Cyan
    
    if ($notInstalledCount -eq 0) {
        Write-Host "`n🎉 Todas las características están habilitadas!" -ForegroundColor Green
    } else {
        Write-Host "`n⚠️ Faltan $notInstalledCount características por habilitar" -ForegroundColor Yellow
        Write-Host "Ejecuta este script sin -Verify para instalarlas" -ForegroundColor Yellow
    }
    
    Read-Host "Presiona Enter para continuar..."
    exit 0
}

Write-Host "`n[PASO 1] Verificando características existentes..." -ForegroundColor Yellow

$toInstall = @()
$alreadyInstalled = @()

foreach ($feature in $RequiredFeatures) {
    try {
        $featureState = Get-WindowsOptionalFeature -Online -FeatureName $feature -ErrorAction SilentlyContinue
        
        if ($featureState -and $featureState.State -eq "Enabled") {
            $alreadyInstalled += $feature
            Write-Host "✅ $feature ya está habilitado" -ForegroundColor Green
        } else {
            $toInstall += $feature
            Write-Host "❌ $feature necesita ser habilitado" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "⚠️ $feature no se pudo verificar, se intentará instalar" -ForegroundColor Yellow
        $toInstall += $feature
    }
}

Write-Host "`n[RESUMEN]" -ForegroundColor Cyan
Write-Host "Características ya instaladas: $($alreadyInstalled.Count)" -ForegroundColor Green
Write-Host "Características a instalar: $($toInstall.Count)" -ForegroundColor Yellow

if ($toInstall.Count -eq 0) {
    Write-Host "`n🎉 Todas las características necesarias ya están habilitadas!" -ForegroundColor Green
    Write-Host "IIS está listo para DINQR" -ForegroundColor Green
    Read-Host "Presiona Enter para continuar..."
    exit 0
}

if (-not $Force) {
    Write-Host "`n¿Continuar con la instalación de $($toInstall.Count) características?" -ForegroundColor Yellow
    $confirmation = Read-Host "Escribe 'si' para continuar"
    
    if ($confirmation -ne "si") {
        Write-Host "Instalación cancelada por el usuario" -ForegroundColor Yellow
        exit 0
    }
}

Write-Host "`n[PASO 2] Habilitando características necesarias..." -ForegroundColor Yellow

$successCount = 0
$failCount = 0
$errorLog = @()

foreach ($feature in $toInstall) {
    Write-Host "Habilitando $feature..." -ForegroundColor Cyan
    
    try {
        $result = Enable-WindowsOptionalFeature -Online -FeatureName $feature -All -NoRestart
        
        if ($result.RestartNeeded) {
            Write-Host "⚠️ $feature habilitado (requiere reinicio)" -ForegroundColor Yellow
        } else {
            Write-Host "✅ $feature habilitado exitosamente" -ForegroundColor Green
        }
        
        $successCount++
    }
    catch {
        Write-Host "❌ Error habilitando $feature`: $($_.Exception.Message)" -ForegroundColor Red
        $errorLog += "$feature`: $($_.Exception.Message)"
        $failCount++
    }
}

Write-Host "`n[PASO 3] Configuraciones adicionales..." -ForegroundColor Yellow

# Verificar y configurar ASP.NET
try {
    Write-Host "Registrando ASP.NET con IIS..." -ForegroundColor Cyan
    $aspnetRegiis = "${env:WINDIR}\Microsoft.NET\Framework64\v4.0.30319\aspnet_regiis.exe"
    if (Test-Path $aspnetRegiis) {
        & $aspnetRegiis -i
        Write-Host "✅ ASP.NET registrado con IIS" -ForegroundColor Green
    }
}
catch {
    Write-Host "⚠️ No se pudo registrar ASP.NET: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Desbloquear configuraciones necesarias
Write-Host "Desbloqueando configuraciones de IIS..." -ForegroundColor Cyan
try {
    & "$env:WINDIR\system32\inetsrv\appcmd.exe" unlock config -section:system.webServer/handlers
    & "$env:WINDIR\system32\inetsrv\appcmd.exe" unlock config -section:system.webServer/modules
    Write-Host "✅ Configuraciones desbloqueadas" -ForegroundColor Green
}
catch {
    Write-Host "⚠️ No se pudieron desbloquear todas las configuraciones" -ForegroundColor Yellow
}

Write-Host "`n=====================================" -ForegroundColor Green
Write-Host "   INSTALACIÓN COMPLETADA" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

Write-Host "`n[RESUMEN FINAL]" -ForegroundColor Cyan
Write-Host "Características habilitadas exitosamente: $successCount" -ForegroundColor Green
Write-Host "Errores encontrados: $failCount" -ForegroundColor Red

if ($failCount -gt 0) {
    Write-Host "`n[ERRORES ENCONTRADOS]" -ForegroundColor Red
    foreach ($error in $errorLog) {
        Write-Host "❌ $error" -ForegroundColor Red
    }
}

# Verificar si IIS está funcionando
Write-Host "`n[VERIFICACIÓN FINAL]" -ForegroundColor Yellow
try {
    $iisService = Get-Service -Name "W3SVC" -ErrorAction SilentlyContinue
    if ($iisService) {
        if ($iisService.Status -eq "Running") {
            Write-Host "✅ Servicio IIS está ejecutándose" -ForegroundColor Green
        } else {
            Write-Host "⚠️ Servicio IIS no está ejecutándose, intentando iniciar..." -ForegroundColor Yellow
            Start-Service -Name "W3SVC"
            Write-Host "✅ Servicio IIS iniciado" -ForegroundColor Green
        }
    } else {
        Write-Host "❌ Servicio IIS no encontrado" -ForegroundColor Red
    }
}
catch {
    Write-Host "❌ Error verificando/iniciando IIS: $($_.Exception.Message)" -ForegroundColor Red
}

# Verificar sitio por defecto
try {
    $defaultSite = & "$env:WINDIR\system32\inetsrv\appcmd.exe" list site "Default Web Site" 2>$null
    if ($defaultSite) {
        Write-Host "✅ Sitio web por defecto disponible" -ForegroundColor Green
    }
}
catch {
    Write-Host "⚠️ No se pudo verificar el sitio web por defecto" -ForegroundColor Yellow
}

Write-Host "`n[PRÓXIMOS PASOS]" -ForegroundColor Cyan
Write-Host "1. Reiniciar el servidor si alguna característica lo requiere" -ForegroundColor White
Write-Host "2. Instalar Application Request Routing (ARR) para proxy reverso" -ForegroundColor White
Write-Host "3. Configurar el sitio DINQR en IIS" -ForegroundColor White
Write-Host "4. Probar acceso a: http://localhost" -ForegroundColor White

Write-Host "`n[COMANDOS ÚTILES]" -ForegroundColor Cyan
Write-Host "Verificar características: .\configurar_iis_features.ps1 -Verify" -ForegroundColor White
Write-Host "Verificar IIS: iisreset /status" -ForegroundColor White
Write-Host "Lista de sitios: appcmd list sites" -ForegroundColor White

if ($successCount -eq $toInstall.Count) {
    Write-Host "`n🎉 IIS configurado exitosamente para DINQR!" -ForegroundColor Green
} else {
    Write-Host "`n⚠️ IIS configurado con algunos errores. Revisa los mensajes anteriores." -ForegroundColor Yellow
}

Read-Host "`nPresiona Enter para continuar..."
