@echo off
REM Simple launcher for deployment script

cd /d "%~dp0"

echo.
echo ============================================================
echo   Starting Deployment...
echo ============================================================
echo.

if exist "DEPLOY_ALL_IN_ONE.bat" (
    echo Running DEPLOY_ALL_IN_ONE.bat...
    call DEPLOY_ALL_IN_ONE.bat
) else if exist "DEPLOY_ALL_IN_ONE.ps1" (
    echo Running DEPLOY_ALL_IN_ONE.ps1...
    powershell -ExecutionPolicy Bypass -File "DEPLOY_ALL_IN_ONE.ps1"
) else (
    echo [ERROR] Deployment script not found!
    echo.
    echo Please make sure you're in the project root directory.
    pause
    exit /b 1
)
