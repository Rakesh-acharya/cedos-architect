@echo off
REM Automatic Railway Deployment with Token
REM This script will deploy everything automatically

echo ============================================================
echo   CEDOS Backend - Automatic Railway Deployment
echo ============================================================
echo.

REM Set Railway token as environment variable
set RAILWAY_TOKEN=c87c4dea-c118-4afb-9db6-e323a68ff5d2

REM Navigate to backend directory
cd /d "%~dp0backend"

echo [INFO] Railway Token: c87c4dea-c118-4afb-9db6-e323a68ff5d2
echo.

echo Step 1: Checking Railway CLI...
railway --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Railway CLI...
    call npm install -g @railway/cli
)

echo.
echo Step 2: Authenticating with Railway...
set RAILWAY_TOKEN=c87c4dea-c118-4afb-9db6-e323a68ff5d2
railway link
if %errorlevel% neq 0 (
    echo [INFO] No existing project linked, will create new one
)

echo.
echo Step 3: Please provide your Supabase password:
set /p SUPABASE_PASSWORD="Enter Supabase Password: "

if "%SUPABASE_PASSWORD%"=="" (
    echo [ERROR] Password is required!
    echo Please run this script again and enter your password.
    pause
    exit /b 1
)

echo.
echo Step 4: Setting up Railway project...
railway init --name cedos-backend 2>nul
if %errorlevel% neq 0 (
    echo [INFO] Project might already exist or will be created during deployment
)

echo.
echo Step 5: Setting environment variables...

echo   - Setting DATABASE_URL...
railway variables set DATABASE_URL="postgresql://postgres:%SUPABASE_PASSWORD%@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres"

echo   - Generating SECRET_KEY...
for /f "delims=" %%i in ('powershell -Command "$bytes = New-Object byte[] 32; $rng = [System.Security.Cryptography.RandomNumberGenerator]::Create(); $rng.GetBytes($bytes); [Convert]::ToBase64String($bytes)"') do set SECRET_KEY=%%i
railway variables set SECRET_KEY="%SECRET_KEY%"

echo   - Setting CORS origins...
railway variables set BACKEND_CORS_ORIGINS=["*"]

echo.
echo Step 6: Deploying to Railway...
echo This will take 3-5 minutes, please wait...
railway up --detach

echo.
echo Waiting for deployment to complete...
timeout /t 30 /nobreak >nul

echo.
echo Step 7: Running database migrations...
railway run alembic upgrade head

echo.
echo Step 8: Creating default users...
railway run python create_default_users.py

echo.
echo Step 9: Getting your deployment URL...
railway domain

echo.
echo ============================================================
echo   DEPLOYMENT COMPLETE!
echo ============================================================
echo.
echo Your backend is now live on Railway!
echo.
echo Next steps:
echo 1. Copy the URL shown above
echo 2. Test API: https://your-url.up.railway.app/api/docs
echo 3. Update mobile app: Edit cedos-mobile/src/theme.ts
echo    Change API_BASE_URL to your Railway URL
echo.
echo Example:
echo   export const API_BASE_URL = 'https://your-url.up.railway.app/api/v1';
echo.
pause
