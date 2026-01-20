@echo off
REM Run this first to complete Railway login and deployment

echo ============================================================
echo   CEDOS Backend - Complete Deployment Setup
echo ============================================================
echo.

echo Step 1: Railway Login
echo.
echo This will open a browser window.
echo Please login with your GitHub account.
echo.
pause

railway login

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Login failed!
    echo.
    echo Alternative: Get token from https://railway.app/account/tokens
    echo Then run: railway login --browserless YOUR_TOKEN
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] Logged in successfully!
echo.

echo Step 2: Ready to deploy?
echo.
echo Next, run: .\DEPLOY_WITH_PASSWORD.bat
echo.
echo Or follow the manual steps in COMPLETE_DEPLOYMENT_STEPS.md
echo.
pause
