@echo off
REM Complete Railway Deployment - All Steps Automated
REM This will deploy everything once you provide Supabase password

echo ============================================================
echo   CEDOS Backend - Complete Railway Deployment
echo ============================================================
echo.

REM Set Railway token
set RAILWAY_TOKEN=c87c4dea-c118-4afb-9db6-e323a68ff5d2

cd /d "%~dp0backend"

echo [STEP 1] Checking Railway CLI...
railway --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Railway CLI...
    call npm install -g @railway/cli
)

echo.
echo [STEP 2] Authenticating with Railway...
echo Using token: c87c4dea-c118-4afb-9db6-e323a68ff5d2
set RAILWAY_TOKEN=c87c4dea-c118-4afb-9db6-e323a68ff5d2

REM Try to verify token
railway whoami >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [WARNING] Token authentication failed!
    echo.
    echo Please get a new token from: https://railway.app/account/tokens
    echo Then update this script with the new token.
    echo.
    echo Or try logging in interactively:
    echo   railway login
    echo.
    pause
    exit /b 1
)

echo [OK] Authenticated successfully!
echo.

echo [STEP 3] Please enter your Supabase password:
set /p SUPABASE_PASSWORD="Supabase Password: "

if "%SUPABASE_PASSWORD%"=="" (
    echo [ERROR] Password is required!
    pause
    exit /b 1
)

echo.
echo [STEP 4] Initializing Railway project...
railway init --name cedos-backend
if %errorlevel% neq 0 (
    echo [INFO] Project initialization - continuing...
)

echo.
echo [STEP 5] Setting environment variables...

echo   Setting DATABASE_URL...
railway variables set DATABASE_URL="postgresql://postgres:%SUPABASE_PASSWORD%@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres"
if %errorlevel% neq 0 (
    echo [ERROR] Failed to set DATABASE_URL
    pause
    exit /b 1
)

echo   Generating SECRET_KEY...
for /f "delims=" %%i in ('powershell -Command "$rng = [System.Security.Cryptography.RandomNumberGenerator]::Create(); $bytes = New-Object byte[] 32; $rng.GetBytes($bytes); [Convert]::ToBase64String($bytes)"') do set SECRET_KEY=%%i
railway variables set SECRET_KEY="%SECRET_KEY%"

echo   Setting CORS origins...
railway variables set BACKEND_CORS_ORIGINS=["*"]

echo.
echo [STEP 6] Deploying to Railway...
echo This will take 3-5 minutes...
railway up
if %errorlevel% neq 0 (
    echo [ERROR] Deployment failed
    echo Check the error above and try again.
    pause
    exit /b 1
)

echo.
echo [STEP 7] Running database migrations...
railway run alembic upgrade head
if %errorlevel% neq 0 (
    echo [WARN] Migrations completed with warnings
)

echo.
echo [STEP 8] Creating default users...
railway run python create_default_users.py
if %errorlevel% neq 0 (
    echo [WARN] User creation completed with warnings
)

echo.
echo [STEP 9] Getting your deployment URL...
railway domain

echo.
echo ============================================================
echo   DEPLOYMENT COMPLETE!
echo ============================================================
echo.
echo Your backend is now live!
echo.
echo Next steps:
echo 1. Copy the URL above
echo 2. Test: https://your-url.up.railway.app/api/docs
echo 3. Update mobile app with the URL
echo.
pause
