@echo off
REM Complete Deployment Script
REM Run this and provide Supabase password when asked

echo ============================================================
echo   CEDOS Backend - Complete Deployment
echo ============================================================
echo.

cd /d "%~dp0backend"

echo [INFO] Railway Token: c87c4dea-c118-4afb-9db6-e323a68ff5d2
echo [INFO] If token is invalid, get a new one from: https://railway.app/account/tokens
echo.

REM Set token
set RAILWAY_TOKEN=c87c4dea-c118-4afb-9db6-e323a68ff5d2

echo Step 1: Checking Railway CLI...
railway --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Railway CLI...
    call npm install -g @railway/cli
)

echo.
echo Step 2: Testing Railway authentication...
railway whoami
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Authentication failed!
    echo.
    echo Please do ONE of the following:
    echo.
    echo Option A: Get new token
    echo   1. Go to: https://railway.app/account/tokens
    echo   2. Create new token
    echo   3. Update this script with new token
    echo.
    echo Option B: Login interactively
    echo   Run: railway login
    echo   Then run this script again
    echo.
    pause
    exit /b 1
)

echo [OK] Authenticated!
echo.

echo Step 3: Enter your Supabase password:
set /p SUPABASE_PASSWORD="Password: "

if "%SUPABASE_PASSWORD%"=="" (
    echo [ERROR] Password required!
    pause
    exit /b 1
)

echo.
echo Step 4: Initializing Railway project...
railway init --name cedos-backend

echo.
echo Step 5: Setting environment variables...
railway variables set DATABASE_URL="postgresql://postgres:%SUPABASE_PASSWORD%@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres"
railway variables set SECRET_KEY="cedos-secret-key-$(powershell -Command "[System.Web.Security.Membership]::GeneratePassword(32, 0)")"
railway variables set BACKEND_CORS_ORIGINS=["*"]

echo.
echo Step 6: Deploying (this takes 3-5 minutes)...
railway up

echo.
echo Step 7: Running migrations...
railway run alembic upgrade head

echo.
echo Step 8: Creating users...
railway run python create_default_users.py

echo.
echo Step 9: Getting URL...
railway domain

echo.
echo ============================================================
echo   DONE! Your backend is live!
echo ============================================================
pause
