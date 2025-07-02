# ====================================
# CONFIGURAR POWERSHELL EXECUTION POLICY
# ====================================
# Este script configura la política de ejecución de PowerShell
# para permitir la ejecución de scripts necesarios para DINQR

param(
    [switch]$Force = $false
)

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "   CONFIGURANDO POWERSHELL EXECUTION POLICY" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si se ejecuta como administrador
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "[ERROR] Este script debe ejecutarse como Administrador" -ForegroundColor Red
    Write-Host "[INFO] Click derecho y selecciona 'Ejecutar como administrador'" -ForegroundColor Yellow
    exit 1
}

Write-Host "[INFO] Verificando política de ejecución actual..." -ForegroundColor Yellow

# Obtener política actual
$currentPolicy = Get-ExecutionPolicy -Scope CurrentUser
$machinePolicy = Get-ExecutionPolicy -Scope LocalMachine

Write-Host "[INFO] Política actual (CurrentUser): $currentPolicy" -ForegroundColor Cyan
Write-Host "[INFO] Política actual (LocalMachine): $machinePolicy" -ForegroundColor Cyan
Write-Host ""

# Verificar si ya permite ejecución
if ($currentPolicy -eq "RemoteSigned" -or $currentPolicy -eq "Unrestricted" -or $machinePolicy -eq "RemoteSigned" -or $machinePolicy -eq "Unrestricted") {
    Write-Host "[OK] PowerShell ya permite ejecución de scripts" -ForegroundColor Green
    exit 0
}

# Configurar política
Write-Host "[INFO] Configurando política de ejecución..." -ForegroundColor Yellow

try {
    # Intentar configurar para el usuario actual primero (más seguro)
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
    Write-Host "[OK] Política configurada para CurrentUser: RemoteSigned" -ForegroundColor Green
    
    # Verificar el cambio
    $newPolicy = Get-ExecutionPolicy -Scope CurrentUser
    if ($newPolicy -eq "RemoteSigned") {
        Write-Host "[OK] Configuración exitosa" -ForegroundColor Green
        Write-Host ""
        Write-Host "Ahora puedes ejecutar:" -ForegroundColor Cyan
        Write-Host "  .\configurar_iis_features.ps1" -ForegroundColor White
        Write-Host ""
        exit 0
    }
} catch {
    Write-Host "[WARNING] No se pudo configurar para CurrentUser: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Si falla el usuario actual, intentar máquina local
try {
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine -Force
    Write-Host "[OK] Política configurada para LocalMachine: RemoteSigned" -ForegroundColor Green
    
    # Verificar el cambio
    $newPolicy = Get-ExecutionPolicy -Scope LocalMachine
    if ($newPolicy -eq "RemoteSigned") {
        Write-Host "[OK] Configuración exitosa" -ForegroundColor Green
        Write-Host ""
        Write-Host "Ahora puedes ejecutar:" -ForegroundColor Cyan
        Write-Host "  .\configurar_iis_features.ps1" -ForegroundColor White
        Write-Host ""
        exit 0
    }
} catch {
    Write-Host "[ERROR] No se pudo configurar ExecutionPolicy: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Red
Write-Host "   CONFIGURACIÓN MANUAL REQUERIDA" -ForegroundColor Red
Write-Host "================================================" -ForegroundColor Red
Write-Host ""
Write-Host "Si este script no funcionó, ejecuta manualmente:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Abrir PowerShell como Administrador" -ForegroundColor Cyan
Write-Host "2. Ejecutar: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor White
Write-Host "3. Confirmar con 'S' o 'Y'" -ForegroundColor White
Write-Host "4. Ejecutar: .\configurar_iis_features.ps1" -ForegroundColor White
Write-Host ""
Write-Host "Alternativamente, ejecutar con Bypass:" -ForegroundColor Yellow
Write-Host "PowerShell -ExecutionPolicy Bypass -File .\configurar_iis_features.ps1" -ForegroundColor White
Write-Host ""

exit 1
