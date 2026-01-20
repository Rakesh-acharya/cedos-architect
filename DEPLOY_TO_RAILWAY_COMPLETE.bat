@echo off
REM ============================================================
REM   Complete Railway Deployment - Auto Migrations & Deploy
REM   Makes CEDOS globally accessible!
REM ============================================================

echo.
echo ============================================================
echo   CEDOS - Complete Railway Deployment
echo ============================================================
echo.
echo This will:
echo   1. Run database migrations
echo   2. Deploy backend to Railway
echo   3. Configure environment variables
echo   4. Make your app globally accessible
echo.
pause

cd /d "%~dp0backend"

echo.
echo ============================================================
echo   Step 1: Check Prerequisites
echo ============================================================
echo.

REM Check Railway CLI
where railway >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Railway CLI...
    npm install -g @railway/cli
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install Railway CLI
        echo Please install manually: npm install -g @railway/cli
        pause
        exit /b 1
    )
)
echo [OK] Railway CLI installed

REM Check if logged in
railway whoami >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ============================================================
    echo   Step 2: Login to Railway
    echo ============================================================
    echo.
    echo Please login to Railway...
    railway login
    if %errorlevel% neq 0 (
        echo [ERROR] Railway login failed!
        pause
        exit /b 1
    )
) else (
    echo [OK] Already logged in to Railway
)

echo.
echo ============================================================
echo   Step 3: Setup Railway Project
echo ============================================================
echo.

REM Check if project exists
railway status >nul 2>&1
if %errorlevel% neq 0 (
    echo Initializing Railway project...
    railway init
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to initialize Railway project
        pause
        exit /b 1
    )
) else (
    echo [OK] Railway project already initialized
)

echo.
echo ============================================================
echo   Step 4: Setup Database (Supabase)
echo ============================================================
echo.

echo Do you want to use:
echo   1. Supabase (Cloud - Recommended)
echo   2. Local PostgreSQL (for testing)
echo.
choice /C 12 /M "Choose database option"

if errorlevel 2 goto :local_db
if errorlevel 1 goto :supabase_db

:supabase_db
echo.
echo ============================================================
echo   Using Supabase Database
echo ============================================================
echo.
echo Please provide your Supabase connection string:
echo Format: postgresql://postgres:PASSWORD@db.xxx.supabase.co:5432/postgres
echo.
set /p SUPABASE_URL="Supabase Connection String: "

if "%SUPABASE_URL%"=="" (
    echo [ERROR] Supabase URL required!
    echo.
    echo Get it from: https://supabase.com/dashboard
    echo   Your project - Settings - Database - Connection string
    echo.
    pause
    exit /b 1
)

REM URL encode password if needed
echo.
echo Setting DATABASE_URL in Railway...
railway variables set DATABASE_URL="%SUPABASE_URL%"

goto :env_setup

:local_db
echo.
echo ============================================================
echo   Using Local PostgreSQL
echo ============================================================
echo.
echo Using local database: postgresql://cedos_user:cedos_pass@localhost:5432/cedos_db
echo.
echo NOTE: For global access, Railway needs a cloud database!
echo       Local database only works for local development.
echo.
choice /C YN /M "Continue with local database (not recommended for Railway)"

if errorlevel 2 (
    echo Switching to Supabase...
    goto :supabase_db
)

railway variables set DATABASE_URL="postgresql://cedos_user:cedos_pass@localhost:5432/cedos_db"

:env_setup
echo.
echo ============================================================
echo   Step 5: Setup Environment Variables
echo ============================================================
echo.

echo Setting environment variables...
railway variables set SECRET_KEY="cedos-secret-key-change-in-production-$(date +%s)"
railway variables set BACKEND_CORS_ORIGINS="[\"*\"]"
railway variables set AI_ENABLED="true"

echo [OK] Environment variables set

echo.
echo ============================================================
echo   Step 6: Run Database Migrations
echo ============================================================
echo.

echo Running database migrations on Railway...
echo.
railway run alembic upgrade head

if %errorlevel% equ 0 (
    echo.
    echo [OK] Migrations completed successfully!
) else (
    echo.
    echo [WARNING] Migrations may have failed
    echo This is OK if tables already exist
    echo.
)

echo.
echo ============================================================
echo   Step 7: Deploy to Railway
echo ============================================================
echo.

echo Deploying backend to Railway...
echo This may take a few minutes...
echo.
railway up

if %errorlevel% equ 0 (
    echo.
    echo [OK] Deployment successful!
) else (
    echo.
    echo [ERROR] Deployment failed!
    echo Check Railway dashboard for details
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   Step 8: Get Public URL
echo ============================================================
echo.

echo Getting Railway public URL...
railway domain

echo.
set /p RAILWAY_URL="Enter your Railway URL (from above): "

if "%RAILWAY_URL%"=="" (
    echo.
    echo Getting URL from Railway...
    for /f "tokens=*" %%i in ('railway domain') do set RAILWAY_URL=%%i
)

echo.
echo ============================================================
echo   Step 9: Create Default Users
echo ============================================================
echo.

echo Creating default users...
railway run python create_default_users.py

if %errorlevel% equ 0 (
    echo [OK] Default users created
) else (
    echo [INFO] Users may already exist
)

echo.
echo ============================================================
echo   Deployment Complete!
echo ============================================================
echo.
echo Your CEDOS backend is now globally accessible!
echo.
echo ============================================================
echo   Access Information
echo ============================================================
echo.
echo Backend URL: %RAILWAY_URL%
echo API Docs:    %RAILWAY_URL%/api/docs
echo Health Check: %RAILWAY_URL%/health
echo.
echo ============================================================
echo   Default Login Credentials
echo ============================================================
echo.
echo Admin:
echo   Username: admin
echo   Password: admin123
echo.
echo Engineer:
echo   Username: engineer
echo   Password: engineer123
echo.
echo ============================================================
echo   Next Steps
echo ============================================================
echo.
echo 1. Test your API:
echo    %RAILWAY_URL%/api/docs
echo.
echo 2. Update frontend to use this URL:
echo    Edit frontend/src/config.ts
echo    Set API_URL = "%RAILWAY_URL%"
echo.
echo 3. Deploy frontend to Vercel:
echo    .\DEPLOY_FRONTEND_VERCEL.bat
echo.
echo ============================================================
echo   Railway Dashboard
echo ============================================================
echo.
echo View logs and manage deployment:
echo https://railway.app/dashboard
echo.
echo ============================================================
echo.

choice /C YN /M "Open Railway dashboard in browser"

if errorlevel 1 (
    start https://railway.app/dashboard
)

echo.
echo Deployment complete! Your app is globally accessible!
echo.
pause
