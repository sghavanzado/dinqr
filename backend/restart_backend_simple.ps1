# PowerShell script to restart the backend
Write-Host "Restarting Backend Server" -ForegroundColor Cyan
Write-Host "==============================="

# Stop any running Python processes
Write-Host "Stopping existing Python processes..." -ForegroundColor Yellow
taskkill /F /IM python.exe 2>$null
Start-Sleep -Seconds 2
Write-Host "Stopped existing processes" -ForegroundColor Green

# Change to backend directory
Set-Location "c:\Users\administrator.GTS\Develop\dinqr\backend"

# Start the backend
Write-Host "Starting backend server..." -ForegroundColor Yellow
Start-Process python -ArgumentList "app.py" -WindowStyle Hidden
Start-Sleep -Seconds 5
Write-Host "Backend started successfully!" -ForegroundColor Green
Write-Host "Backend should be running at http://localhost:5000" -ForegroundColor Blue

Write-Host "==============================="
Write-Host "You can now test cargo creation from the frontend!" -ForegroundColor Green
