# ========================================
# SCRIPT DE INSTALACIÓN COMPLETA
# Cartón de Visita - SIGA
# ========================================

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  INSTALACIÓN CARTÓN DE VISITA - SIGA" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Variables
$projectRoot = "c:\Users\administrator.GTS\Develop\dinqr"
$backendDir = "$projectRoot\backend"
$frontendDir = "$projectRoot\frontend"

# ========================================
# PASO 1: MIGRACIÓN DE BASE DE DATOS
# ========================================
Write-Host "PASO 1: Migración de Base de Datos" -ForegroundColor Yellow
Write-Host "-----------------------------------" -ForegroundColor Yellow

$respuesta = Read-Host "¿Ejecutar migración de BD? (s/n)"
if ($respuesta -eq 's') {
    Write-Host "Ejecutando migración..." -ForegroundColor Green
    
    Set-Location $backendDir
    
    # Intentar con Flask-Migrate primero
    Write-Host "Intentando con flask db upgrade..." -ForegroundColor Gray
    $output = flask db upgrade 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Migración completada con Flask-Migrate" -ForegroundColor Green
    }
    else {
        Write-Host "⚠ Flask-Migrate falló, usando SQL manual..." -ForegroundColor Yellow
        
        # Ejecutar SQL manual
        $sqlFile = "$backendDir\migrations\create_business_cards_manual.sql"
        
        Write-Host "Ejecutando: psql -U postgres -d localdb -f $sqlFile" -ForegroundColor Gray
        psql -U postgres -d localdb -f $sqlFile
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Migración completada con SQL manual" -ForegroundColor Green
        }
        else {
            Write-Host "✗ Error en migración SQL" -ForegroundColor Red
            Write-Host "Por favor ejecuta manualmente el SQL en pgAdmin" -ForegroundColor Yellow
        }
    }
    
    Write-Host ""
}
else {
    Write-Host "⊗ Migración omitida" -ForegroundColor Yellow
    Write-Host ""
}

# ========================================
# PASO 2: VERIFICAR TABLA CREADA
# ========================================
Write-Host "PASO 2: Verificar Tabla Creada" -ForegroundColor Yellow
Write-Host "-------------------------------" -ForegroundColor Yellow

$respuesta = Read-Host "¿Verificar tabla business_cards? (s/n)"
if ($respuesta -eq 's') {
    Write-Host "Verificando tabla..." -ForegroundColor Green
    
    psql -U postgres -d localdb -c "\d business_cards"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Tabla business_cards existe" -ForegroundColor Green
    }
    else {
        Write-Host "✗ Tabla no encontrada" -ForegroundColor Red
    }
    
    Write-Host ""
}
else {
    Write-Host "⊗ Verificación omitida" -ForegroundColor Yellow
    Write-Host ""
}

# ========================================
# PASO 3: REINSTALAR DEPENDENCIAS FRONTEND
# ========================================
Write-Host "PASO 3: Dependencias Frontend" -ForegroundColor Yellow
Write-Host "-----------------------------" -ForegroundColor Yellow

$respuesta = Read-Host "¿Reinstalar dependencias npm? (s/n)"
if ($respuesta -eq 's') {
    Write-Host "Limpiando node_modules..." -ForegroundColor Green
    
    Set-Location $frontendDir
    
    if (Test-Path "node_modules") {
        Remove-Item -Recurse -Force node_modules
    }
    
    if (Test-Path "package-lock.json") {
        Remove-Item -Force package-lock.json
    }
    
    if (Test-Path ".vite") {
        Remove-Item -Recurse -Force .vite
    }
    
    Write-Host "Ejecutando npm install..." -ForegroundColor Green
    npm install
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Dependencias instaladas" -ForegroundColor Green
    }
    else {
        Write-Host "✗ Error instalando dependencias" -ForegroundColor Red
    }
    
    Write-Host ""
}
else {
    Write-Host "⊗ Instalación omitida" -ForegroundColor Yellow
    Write-Host ""
}

# ========================================
# PASO 4: COMPILAR FRONTEND
# ========================================
Write-Host "PASO 4: Compilar Frontend" -ForegroundColor Yellow
Write-Host "-------------------------" -ForegroundColor Yellow

$respuesta = Read-Host "¿Compilar frontend? (s/n)"
if ($respuesta -eq 's') {
    Write-Host "Ejecutando npm run build..." -ForegroundColor Green
    
    Set-Location $frontendDir
    npm run build
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Frontend compilado" -ForegroundColor Green
    }
    else {
        Write-Host "✗ Error compilando frontend" -ForegroundColor Red
    }
    
    Write-Host ""
}
else {
    Write-Host "⊗ Compilación omitida" -ForegroundColor Yellow
    Write-Host ""
}

# ========================================
# PASO 5: REINICIAR BACKEND
# ========================================
Write-Host "PASO 5: Reiniciar Backend" -ForegroundColor Yellow
Write-Host "-------------------------" -ForegroundColor Yellow

$respuesta = Read-Host "¿Reiniciar backend? (s/n)"
if ($respuesta -eq 's') {
    Write-Host "Intentando reiniciar backend..." -ForegroundColor Green
    
    Set-Location $backendDir
    
    # Matar procesos Python existentes
    Write-Host "Deteniendo procesos Python..." -ForegroundColor Gray
    taskkill /F /IM python.exe /T 2>$null
    
    Start-Sleep -Seconds 2
    
    # Iniciar backend en modo background
    Write-Host "Iniciando backend..." -ForegroundColor Gray
    Start-Process python -ArgumentList "app.py" -WindowStyle Minimized
    
    Start-Sleep -Seconds 3
    
    Write-Host "✓ Backend reiniciado" -ForegroundColor Green
    Write-Host ""
}
else {
    Write-Host "⊗ Reinicio omitido (reinicia manualmente)" -ForegroundColor Yellow
    Write-Host ""
}

# ========================================
# PASO 6: EJECUTAR PRUEBAS
# ========================================
Write-Host "PASO 6: Ejecutar Pruebas" -ForegroundColor Yellow
Write-Host "------------------------" -ForegroundColor Yellow

$respuesta = Read-Host "¿Ejecutar script de pruebas? (s/n)"
if ($respuesta -eq 's') {
    Write-Host "Verificando dependencias de pruebas..." -ForegroundColor Green
    
    Set-Location $backendDir
    
    pip install colorama requests --quiet
    
    Write-Host "Ejecutando test_business_card.py..." -ForegroundColor Green
    Write-Host ""
    
    python test_business_card.py
    
    Write-Host ""
}
else {
    Write-Host "⊗ Pruebas omitidas" -ForegroundColor Yellow
    Write-Host ""
}

# ========================================
# RESUMEN FINAL
# ========================================
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  INSTALACIÓN COMPLETADA" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Próximos pasos:" -ForegroundColor Yellow
Write-Host "1. Accede a la aplicación:" -ForegroundColor White
Write-Host "   - Desarrollo: http://localhost:5173/" -ForegroundColor Gray
Write-Host "   - Producción: https://localhost/" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Navega a: Funcionários → Gerar CV" -ForegroundColor White
Write-Host ""
Write-Host "3. Verifica que la tabla carga correctamente" -ForegroundColor White
Write-Host ""
Write-Host "4. Genera un cartón de prueba" -ForegroundColor White
Write-Host ""
Write-Host "5. Escanea el QR y verifica la landing page" -ForegroundColor White
Write-Host ""

Write-Host "Documentación:" -ForegroundColor Yellow
Write-Host "- RESUMEN_FINAL_CARTON_VISITA.md" -ForegroundColor Gray
Write-Host "- README_CARTON_VISITA.md" -ForegroundColor Gray
Write-Host "- IMPLEMENTACION_CARTON_VISITA.md" -ForegroundColor Gray
Write-Host ""

Write-Host "¡Listo! 🎉" -ForegroundColor Green
Write-Host ""

# Volver al directorio raíz
Set-Location $projectRoot
