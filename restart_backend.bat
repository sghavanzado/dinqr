@echo off
echo Restarting DINQR Backend Server...
echo.

REM Find and kill any existing Python processes running the backend
tasklist /FI "IMAGENAME eq python.exe" /FO CSV | find /I "python.exe" > nul
if %ERRORLEVEL% EQU 0 (
    echo Stopping existing Python processes...
    taskkill /F /IM python.exe
    timeout /t 2 /nobreak > nul
)

REM Navigate to backend directory
cd /d "c:\Users\administrator.GTS\Develop\dinqr\backend"

REM Check if we're in the right directory
if not exist "app.py" (
    echo ERROR: app.py not found in current directory
    echo Current directory: %CD%
    pause
    exit /b 1
)

echo Starting backend server...
echo Directory: %CD%
echo.

REM Start the backend server
python app.py

pause
