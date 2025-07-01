# Script de Configuración SSL/HTTPS para DINQR
# Debe ejecutarse como Administrador con PowerShell

param(
    [string]$DomainName = "localhost",
    [string]$SiteName = "DINQR",
    [int]$HttpsPort = 443,
    [string]$CertificateThumbprint = "",
    [switch]$SelfSigned = $false
)

Write-Host "=====================================" -ForegroundColor Green
Write-Host "   CONFIGURANDO SSL/HTTPS PARA DINQR" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# Verificar permisos de administrador
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator"))
{
    Write-Host "[ERROR] Este script debe ejecutarse como Administrador" -ForegroundColor Red
    Write-Host "[INFO] Ejecuta PowerShell como Administrador" -ForegroundColor Yellow
    Read-Host "Presiona Enter para continuar..."
    exit 1
}

Write-Host "[INFO] Configurando SSL para:" -ForegroundColor Cyan
Write-Host "[INFO] - Dominio: $DomainName" -ForegroundColor Cyan
Write-Host "[INFO] - Sitio: $SiteName" -ForegroundColor Cyan
Write-Host "[INFO] - Puerto HTTPS: $HttpsPort" -ForegroundColor Cyan

# Importar módulos necesarios
Import-Module WebAdministration -ErrorAction SilentlyContinue
Import-Module PKI -ErrorAction SilentlyContinue

if (-not (Get-Module WebAdministration)) {
    Write-Host "[ERROR] Módulo WebAdministration no disponible" -ForegroundColor Red
    exit 1
}

Write-Host "`n[PASO 1] Verificando certificado SSL..." -ForegroundColor Yellow

$certificate = $null

if ($CertificateThumbprint -ne "") {
    # Usar certificado existente
    Write-Host "[INFO] Buscando certificado con thumbprint: $CertificateThumbprint"
    $certificate = Get-ChildItem -Path "Cert:\LocalMachine\My" | Where-Object { $_.Thumbprint -eq $CertificateThumbprint }
    
    if (-not $certificate) {
        Write-Host "[ERROR] Certificado con thumbprint $CertificateThumbprint no encontrado" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "[OK] Certificado encontrado: $($certificate.Subject)" -ForegroundColor Green
}
elseif ($SelfSigned) {
    # Crear certificado auto-firmado
    Write-Host "[INFO] Creando certificado auto-firmado para $DomainName"
    
    try {
        $certificate = New-SelfSignedCertificate -DnsName $DomainName -CertStoreLocation "Cert:\LocalMachine\My" -KeyLength 2048 -KeyAlgorithm RSA -HashAlgorithm SHA256 -KeyUsage DigitalSignature,KeyEncipherment -Type SSLServerAuthentication -NotAfter (Get-Date).AddYears(2)
        
        Write-Host "[OK] Certificado auto-firmado creado exitosamente" -ForegroundColor Green
        Write-Host "[INFO] Thumbprint: $($certificate.Thumbprint)" -ForegroundColor Cyan
    }
    catch {
        Write-Host "[ERROR] Error creando certificado auto-firmado: $($_.Exception.Message)" -ForegroundColor Red
        exit 1
    }
}
else {
    Write-Host "[ERROR] Debe especificar un certificado existente (-CertificateThumbprint) o crear uno auto-firmado (-SelfSigned)" -ForegroundColor Red
    Write-Host "[INFO] Ejemplo: .\configurar_ssl.ps1 -DomainName 'mi-servidor.com' -SelfSigned" -ForegroundColor Yellow
    Write-Host "[INFO] O: .\configurar_ssl.ps1 -DomainName 'mi-servidor.com' -CertificateThumbprint '1234567890ABCDEF...'" -ForegroundColor Yellow
    exit 1
}

Write-Host "`n[PASO 2] Configurando binding HTTPS en IIS..." -ForegroundColor Yellow

try {
    # Verificar si el sitio existe
    $site = Get-Website -Name $SiteName -ErrorAction SilentlyContinue
    if (-not $site) {
        Write-Host "[ERROR] Sitio '$SiteName' no encontrado en IIS" -ForegroundColor Red
        exit 1
    }
    
    # Eliminar binding HTTPS existente si existe
    $existingBinding = Get-WebBinding -Name $SiteName -Protocol "https" -ErrorAction SilentlyContinue
    if ($existingBinding) {
        Write-Host "[INFO] Eliminando binding HTTPS existente..."
        Remove-WebBinding -Name $SiteName -Protocol "https" -Port $HttpsPort -ErrorAction SilentlyContinue
    }
    
    # Crear nuevo binding HTTPS
    Write-Host "[INFO] Creando binding HTTPS para puerto $HttpsPort..."
    New-WebBinding -Name $SiteName -Protocol "https" -Port $HttpsPort -HostHeader $DomainName -SslFlags 1
    
    # Asociar certificado al binding
    Write-Host "[INFO] Asociando certificado SSL al binding..."
    $binding = Get-WebBinding -Name $SiteName -Protocol "https" -Port $HttpsPort
    $binding.AddSslCertificate($certificate.Thumbprint, "my")
    
    Write-Host "[OK] Binding HTTPS configurado exitosamente" -ForegroundColor Green
}
catch {
    Write-Host "[ERROR] Error configurando binding HTTPS: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host "`n[PASO 3] Configurando redirección HTTP a HTTPS..." -ForegroundColor Yellow

try {
    # Instalar módulo URL Rewrite si no está disponible
    $rewriteModule = Get-WindowsFeature -Name "IIS-HttpRedirect" -ErrorAction SilentlyContinue
    if ($rewriteModule -and $rewriteModule.InstallState -ne "Installed") {
        Write-Host "[INFO] Instalando módulo HTTP Redirect..."
        Enable-WindowsOptionalFeature -Online -FeatureName "IIS-HttpRedirect" -All
    }
    
    # Configurar redirección en web.config
    $webConfigPath = "$($site.PhysicalPath)\web.config"
    
    if (Test-Path $webConfigPath) {
        Write-Host "[INFO] Actualizando web.config con redirección HTTPS..."
        
        # Leer web.config actual
        [xml]$webConfig = Get-Content $webConfigPath
        
        # Buscar o crear nodo system.webServer
        $systemWebServer = $webConfig.configuration.'system.webServer'
        if (-not $systemWebServer) {
            $systemWebServer = $webConfig.CreateElement("system.webServer")
            $webConfig.configuration.AppendChild($systemWebServer)
        }
        
        # Buscar o crear nodo rewrite
        $rewrite = $systemWebServer.rewrite
        if (-not $rewrite) {
            $rewrite = $webConfig.CreateElement("rewrite")
            $systemWebServer.AppendChild($rewrite)
        }
        
        # Buscar o crear nodo rules
        $rules = $rewrite.rules
        if (-not $rules) {
            $rules = $webConfig.CreateElement("rules")
            $rewrite.AppendChild($rules)
        }
        
        # Crear regla de redirección HTTPS
        $httpsRule = $webConfig.CreateElement("rule")
        $httpsRule.SetAttribute("name", "Redirect to HTTPS")
        $httpsRule.SetAttribute("enabled", "true")
        $httpsRule.SetAttribute("patternSyntax", "Wildcard")
        $httpsRule.SetAttribute("stopProcessing", "true")
        
        $match = $webConfig.CreateElement("match")
        $match.SetAttribute("url", "*")
        $httpsRule.AppendChild($match)
        
        $conditions = $webConfig.CreateElement("conditions")
        $condition = $webConfig.CreateElement("add")
        $condition.SetAttribute("input", "{HTTPS}")
        $condition.SetAttribute("pattern", "off")
        $condition.SetAttribute("ignoreCase", "true")
        $conditions.AppendChild($condition)
        $httpsRule.AppendChild($conditions)
        
        $action = $webConfig.CreateElement("action")
        $action.SetAttribute("type", "Redirect")
        $action.SetAttribute("url", "https://{HTTP_HOST}:{SERVER_PORT}{REQUEST_URI}")
        $action.SetAttribute("redirectType", "Permanent")
        $httpsRule.AppendChild($action)
        
        # Eliminar regla existente si existe
        $existingRule = $rules.rule | Where-Object { $_.name -eq "Redirect to HTTPS" }
        if ($existingRule) {
            $rules.RemoveChild($existingRule)
        }
        
        $rules.AppendChild($httpsRule)
        
        # Guardar web.config
        $webConfig.Save($webConfigPath)
        
        Write-Host "[OK] Redirección HTTPS configurada en web.config" -ForegroundColor Green
    }
    else {
        Write-Host "[WARNING] web.config no encontrado - redirección no configurada" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "[WARNING] Error configurando redirección HTTPS: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host "`n[PASO 4] Configurando firewall..." -ForegroundColor Yellow

try {
    # Verificar y abrir puerto HTTPS en firewall
    $firewallRule = Get-NetFirewallRule -DisplayName "DINQR HTTPS" -ErrorAction SilentlyContinue
    if (-not $firewallRule) {
        Write-Host "[INFO] Creando regla de firewall para puerto $HttpsPort..."
        New-NetFirewallRule -DisplayName "DINQR HTTPS" -Direction Inbound -Protocol TCP -LocalPort $HttpsPort -Action Allow
        Write-Host "[OK] Regla de firewall creada" -ForegroundColor Green
    } else {
        Write-Host "[INFO] Regla de firewall ya existe" -ForegroundColor Cyan
    }
}
catch {
    Write-Host "[WARNING] Error configurando firewall: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host "[INFO] Configura manualmente el firewall para permitir puerto $HttpsPort" -ForegroundColor Yellow
}

Write-Host "`n[PASO 5] Reiniciando IIS..." -ForegroundColor Yellow

try {
    Write-Host "[INFO] Reiniciando servicios IIS..."
    iisreset /restart | Out-Null
    Start-Sleep -Seconds 5
    Write-Host "[OK] IIS reiniciado exitosamente" -ForegroundColor Green
}
catch {
    Write-Host "[ERROR] Error reiniciando IIS: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n[PASO 6] Verificando configuración SSL..." -ForegroundColor Yellow

Start-Sleep -Seconds 10

try {
    Write-Host "[INFO] Probando conectividad HTTPS..."
    
    # Verificar binding
    $httpsBinding = Get-WebBinding -Name $SiteName -Protocol "https" -Port $HttpsPort
    if ($httpsBinding) {
        Write-Host "[OK] Binding HTTPS activo" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Binding HTTPS no encontrado" -ForegroundColor Red
    }
    
    # Probar conexión HTTPS
    $uri = "https://$DomainName"
    if ($HttpsPort -ne 443) {
        $uri += ":$HttpsPort"
    }
    
    Write-Host "[INFO] Probando URL: $uri"
    
    # Ignorar errores de certificado para prueba
    [System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}
    
    try {
        $response = Invoke-WebRequest -Uri $uri -TimeoutSec 30 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Host "[OK] Sitio HTTPS responde correctamente" -ForegroundColor Green
        } else {
            Write-Host "[WARNING] Sitio HTTPS responde pero con código: $($response.StatusCode)" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "[WARNING] Error probando conectividad HTTPS: $($_.Exception.Message)" -ForegroundColor Yellow
        Write-Host "[INFO] Esto puede ser normal si usas un certificado auto-firmado" -ForegroundColor Cyan
    }
}
catch {
    Write-Host "[WARNING] Error en verificación SSL: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host "`n=====================================" -ForegroundColor Green
Write-Host "   CONFIGURACIÓN SSL COMPLETADA" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

Write-Host "`n[INFO] Resumen de configuración:" -ForegroundColor Cyan
Write-Host "- Sitio: $SiteName" -ForegroundColor White
Write-Host "- Dominio: $DomainName" -ForegroundColor White
Write-Host "- Puerto HTTPS: $HttpsPort" -ForegroundColor White
Write-Host "- Certificado Thumbprint: $($certificate.Thumbprint)" -ForegroundColor White
Write-Host "- Tipo de certificado: $(if($SelfSigned){'Auto-firmado'}else{'Existente'})" -ForegroundColor White

Write-Host "`n[INFO] URLs de acceso:" -ForegroundColor Cyan
Write-Host "- HTTPS: https://$DomainName$(if($HttpsPort -ne 443){":$HttpsPort"})" -ForegroundColor White
Write-Host "- HTTP: http://$DomainName (redirige a HTTPS)" -ForegroundColor White

Write-Host "`n[INFO] Notas importantes:" -ForegroundColor Yellow
if ($SelfSigned) {
    Write-Host "- Certificado auto-firmado: Los navegadores mostrarán advertencia de seguridad" -ForegroundColor Yellow
    Write-Host "- Para producción, usa un certificado de una CA confiable" -ForegroundColor Yellow
}
Write-Host "- Verifica que el firewall permita el puerto $HttpsPort" -ForegroundColor Yellow
Write-Host "- Para certificados auto-firmados, agrega excepción en navegadores" -ForegroundColor Yellow

Write-Host "`n[INFO] Comandos útiles:" -ForegroundColor Cyan
Write-Host "- Ver certificados: Get-ChildItem -Path 'Cert:\LocalMachine\My'" -ForegroundColor White
Write-Host "- Ver bindings: Get-WebBinding -Name '$SiteName'" -ForegroundColor White
Write-Host "- Reiniciar IIS: iisreset" -ForegroundColor White

Write-Host "`nConfiguración SSL completada exitosamente!" -ForegroundColor Green
Read-Host "Presiona Enter para continuar..."
