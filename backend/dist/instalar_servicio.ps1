# DINQR - Instalador de Servicio con Elevación Automática
# Verifica permisos y eleva automáticamente si es necesario

param(
    [string]$Action = "install"
)

# Función para verificar si se ejecuta como administrador
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Función para elevar permisos
function Invoke-AsAdministrator {
    param([string]$ScriptPath, [string]$Arguments)
    
    Write-Host "🔧 Elevando permisos de administrador..." -ForegroundColor Yellow
    
    $startInfo = New-Object System.Diagnostics.ProcessStartInfo
    $startInfo.FileName = "powershell.exe"
    $startInfo.Arguments = "-NoProfile -ExecutionPolicy Bypass -Command `"& '$ScriptPath' $Arguments`""
    $startInfo.Verb = "runas"
    $startInfo.UseShellExecute = $true
    
    try {
        $process = [System.Diagnostics.Process]::Start($startInfo)
        $process.WaitForExit()
        return $process.ExitCode
    }
    catch {
        Write-Host "❌ Error al elevar permisos: $($_.Exception.Message)" -ForegroundColor Red
        return 1
    }
}

# Función principal
function Install-DINQRService {
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host "DINQR Backend - Instalador de Servicio (PowerShell)" -ForegroundColor Cyan
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host ""

    # Verificar que el ejecutable existe
    $exePath = Join-Path $PSScriptRoot "generadorqr.exe"
    if (-not (Test-Path $exePath)) {
        Write-Host "❌ ERROR: No se encontró generadorqr.exe en $PSScriptRoot" -ForegroundColor Red
        Write-Host "Asegúrese de que este script esté en el mismo directorio que generadorqr.exe" -ForegroundColor Yellow
        Read-Host "Presione Enter para salir"
        exit 1
    }

    # Verificar permisos
    if (-not (Test-Administrator)) {
        Write-Host "⚠️  ADVERTENCIA: No se está ejecutando como administrador" -ForegroundColor Yellow
        Write-Host "Se requieren permisos de administrador para instalar servicios de Windows" -ForegroundColor Yellow
        Write-Host ""
        
        $choice = Read-Host "¿Desea elevar automáticamente los permisos? (S/N)"
        if ($choice -match '^[Ss]') {
            # Re-ejecutar como administrador
            $exitCode = Invoke-AsAdministrator $MyInvocation.MyCommand.Path $Action
            exit $exitCode
        } else {
            Write-Host "❌ Instalación cancelada por el usuario" -ForegroundColor Red
            Read-Host "Presione Enter para salir"
            exit 1
        }
    }

    Write-Host "✅ Ejecutándose con permisos de administrador" -ForegroundColor Green
    Write-Host ""

    # Verificar archivo .env
    $envPath = Join-Path $PSScriptRoot ".env"
    $envTemplatePath = Join-Path $PSScriptRoot ".env.template"
    
    if (-not (Test-Path $envPath)) {
        Write-Host "⚠️  ADVERTENCIA: No se encontró el archivo .env" -ForegroundColor Yellow
        if (Test-Path $envTemplatePath) {
            $choice = Read-Host "¿Desea copiar .env.template como .env? (S/N)"
            if ($choice -match '^[Ss]') {
                Copy-Item $envTemplatePath $envPath
                Write-Host "✅ Archivo .env creado desde plantilla" -ForegroundColor Green
                Write-Host "🔧 IMPORTANTE: Edite .env con sus configuraciones antes de usar el servicio" -ForegroundColor Yellow
                Write-Host ""
            }
        }
    }

    # Ejecutar la instalación del servicio
    Write-Host "🔧 Instalando servicio DINQR Backend..." -ForegroundColor Cyan
    Write-Host ""

    $process = Start-Process -FilePath $exePath -ArgumentList "--service", $Action -Wait -PassThru -NoNewWindow
    
    if ($process.ExitCode -eq 0) {
        Write-Host ""
        Write-Host "✅ Operación completada exitosamente" -ForegroundColor Green
        
        if ($Action -eq "install") {
            Write-Host ""
            $choice = Read-Host "¿Desea iniciar el servicio ahora? (S/N)"
            if ($choice -match '^[Ss]') {
                Write-Host "🚀 Iniciando servicio..." -ForegroundColor Cyan
                & $exePath --service start
            }
        }
    } else {
        Write-Host ""
        Write-Host "❌ Error en la operación del servicio" -ForegroundColor Red
        Write-Host "Código de salida: $($process.ExitCode)" -ForegroundColor Red
        
        Write-Host ""
        Write-Host "💡 ALTERNATIVAS:" -ForegroundColor Yellow
        Write-Host "1. Usar NSSM: instalar_servicio_nssm.bat" -ForegroundColor White
        Write-Host "2. Ejecutar como aplicación: generadorqr.exe" -ForegroundColor White
        Write-Host "3. Verificar permisos: verificar_permisos.bat" -ForegroundColor White
    }

    Write-Host ""
    Read-Host "Presione Enter para salir"
}

# Ejecutar función principal
Install-DINQRService
