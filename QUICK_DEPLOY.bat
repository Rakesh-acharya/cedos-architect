@echo off
REM Quick Deploy Script for Railway (Windows)

echo ============================================================
echo   CEDOS Backend - Railway Deployment
echo ============================================================
echo.

REM Check if Railway CLI is installed
where railway >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Railway CLI...
    call npm install -g @railway/cli
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install Railway CLI
        pause
        exit /b 1
    )
)

REM Navigate to backend
cd /d "%~dp0backend"

echo Step 1: Login to Railway...
echo This will open a browser window - please login with GitHub
railway login
if %errorlevel% neq 0 (
    echo [ERROR] Login failed
    pause
    exit /b 1
)

echo.
echo Step 2: Initialize Railway project...
railway init
if %errorlevel% neq 0 (
    echo [ERROR] Initialization failed
    pause
    exit /b 1
)

echo.
echo Step 3: Setting environment variables...
echo Please enter your Supabase password:
set /p SUPABASE_PASSWORD="Password: "

railway variables set DATABASE_URL="postgresql://postgres:%SUPABASE_PASSWORD%@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres"

REM Generate random secret key
for /f "delims=" %%i in ('powershell -Command "[System.Web.Security.Membership]::GeneratePassword(32, 0)"') do set SECRET_KEY=%%i
railway variables set SECRET_KEY="%SECRET_KEY%"

railway variables set BACKEND_CORS_ORIGINS=["*"]

echo.
echo Step 4: Deploying to Railway...
railway up
if %errorlevel% neq 0 (
    echo [ERROR] Deployment failed
    pause
    exit /b 1
)

echo.
echo Step 5: Running migrations...
railway run alembic upgrade head

echo.
echo Step 6: Creating default users...
railway run python create_default_users.py

echo.
echo ============================================================
echo   Deployment Complete!
echo ============================================================
echo.
echo Getting your deployment URL...
railway domain
echo.
echo API Docs will be at: https://your-url.up.railway.app/api/docs
echo.
echo Next steps:
echo 1. Copy the URL above
echo 2. Update cedos-mobile/src/theme.ts with the URL
echo 3. Rebuild mobile app APK
echo.
pause
