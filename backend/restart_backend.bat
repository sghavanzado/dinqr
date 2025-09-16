@echo off
echo Restarting Backend Server...
echo ==============================

echo Stopping existing Python processes...
taskkill /F /IM python.exe >nul 2>&1
timeout /t 2 >nul

echo Starting backend server...
cd /d "c:\Users\administrator.GTS\Develop\dinqr\backend"
start /B python app.py

echo Backend started successfully!
echo Backend should be running at http://localhost:5000
echo You can now test cargo creation from the frontend!
echo ==============================
