#!/usr/bin/env powershell

# PowerShell script to restart the backend
Write-Host "🔄 Restarting Backend Server" -ForegroundColor Cyan
Write-Host "=" * 40

# Stop any running Python processes
Write-Host "🛑 Stopping existing Python processes..." -ForegroundColor Yellow
try {
    taskkill /F /IM python.exe 2>$null
    Start-Sleep -Seconds 2
    Write-Host "✅ Stopped existing processes" -ForegroundColor Green
} catch {
    Write-Host "ℹ️  No existing processes to stop" -ForegroundColor Blue
}

# Change to backend directory
Set-Location "c:\Users\administrator.GTS\Develop\dinqr\backend"

# Start the backend
Write-Host "🚀 Starting backend server..." -ForegroundColor Yellow
try {
    Start-Process python -ArgumentList "app.py" -WindowStyle Hidden
    Start-Sleep -Seconds 5
    Write-Host "✅ Backend started successfully!" -ForegroundColor Green
    Write-Host "🌐 Backend should be running at http://localhost:5000" -ForegroundColor Blue
} catch {
    Write-Host "❌ Failed to start backend" -ForegroundColor Red
}

Write-Host "=" * 40
Write-Host "🎯 You can now test cargo creation from the frontend!" -ForegroundColor Green
