@echo off
echo =================================
echo   DINQR Service Verification
echo =================================
echo.

echo Checking if DINQRBackend service is installed...
sc query DINQRBackend > nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Service DINQRBackend is installed!
    echo.
    echo Service Details:
    sc query DINQRBackend
    echo.
    echo Service Configuration:
    sc qc DINQRBackend
) else (
    echo ❌ Service DINQRBackend is NOT installed
    echo.
    echo To install the service, run:
    echo generadorqr.exe install
)

echo.
echo =================================
echo   Verification Complete
echo =================================
pause
