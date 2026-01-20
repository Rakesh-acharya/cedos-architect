@echo off
REM Quick deployment launcher - Shows output immediately

echo.
echo ============================================================
echo   CEDOS Deployment - Starting...
echo ============================================================
echo.

cd /d "%~dp0"

echo Current directory: %CD%
echo.

if not exist "DEPLOY_ALL_IN_ONE.bat" (
    echo [ERROR] DEPLOY_ALL_IN_ONE.bat not found!
    echo.
    echo Make sure you're in the project root: C:\Users\rakes\architect
    echo.
    pause
    exit /b 1
)

echo Found deployment script!
echo.
echo Running DEPLOY_ALL_IN_ONE.bat...
echo.

call DEPLOY_ALL_IN_ONE.bat

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Deployment failed!
    echo.
    pause
    exit /b 1
)

echo.
echo Deployment completed!
pause
