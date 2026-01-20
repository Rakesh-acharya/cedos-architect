@echo off
REM Complete Railway Deployment Script
REM Uses token for authentication

echo ============================================================
echo   CEDOS Backend - Complete Railway Deployment
echo ============================================================
echo.

REM Set Railway token
set RAILWAY_TOKEN=c87c4dea-c118-4afb-9db6-e323a68ff5d2

REM Navigate to backend
cd /d "%~dp0backend"

echo Step 1: Checking Railway CLI...
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

echo.
echo Step 2: Setting Railway token...
set RAILWAY_TOKEN=c87c4dea-c118-4afb-9db6-e323a68ff5d2

echo.
echo Step 3: Initializing Railway project...
echo Please enter a project name (or press Enter for default: cedos-backend):
set /p PROJECT_NAME="Project name: "
if "%PROJECT_NAME%"=="" set PROJECT_NAME=cedos-backend

railway init --name %PROJECT_NAME%
if %errorlevel% neq 0 (
    echo [WARN] Project might already exist, continuing...
)

echo.
echo Step 4: Setting environment variables...
echo.
echo Please enter your Supabase password:
set /p SUPABASE_PASSWORD="Supabase Password: "

if "%SUPABASE_PASSWORD%"=="" (
    echo [ERROR] Supabase password is required!
    pause
    exit /b 1
)

echo.
echo Setting DATABASE_URL...
railway variables set DATABASE_URL="postgresql://postgres:%SUPABASE_PASSWORD%@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres"

echo.
echo Generating secret key...
for /f "delims=" %%i in ('powershell -Command "[System.Web.Security.Membership]::GeneratePassword(32, 0)"') do set SECRET_KEY=%%i
railway variables set SECRET_KEY="%SECRET_KEY%"

echo.
echo Setting CORS origins...
railway variables set BACKEND_CORS_ORIGINS=["*"]

echo.
echo Step 5: Deploying to Railway...
echo This may take a few minutes...
railway up
if %errorlevel% neq 0 (
    echo [ERROR] Deployment failed
    pause
    exit /b 1
)

echo.
echo Step 6: Running database migrations...
railway run alembic upgrade head
if %errorlevel% neq 0 (
    echo [WARN] Migrations might have failed, but continuing...
)

echo.
echo Step 7: Creating default users...
railway run python create_default_users.py
if %errorlevel% neq 0 (
    echo [WARN] User creation might have failed, but continuing...
)

echo.
echo Step 8: Getting your deployment URL...
railway domain

echo.
echo ============================================================
echo   Deployment Complete!
echo ============================================================
echo.
echo Your backend is now live!
echo.
echo Next steps:
echo 1. Copy the URL above
echo 2. Test it: https://your-url.up.railway.app/api/docs
echo 3. Update mobile app: cedos-mobile/src/theme.ts
echo 4. Update with your Railway URL
echo.
pause
