@echo off
REM Complete Railway Deployment via CLI - Fully Automated

echo ============================================================
echo   CEDOS Backend - Railway CLI Deployment
echo ============================================================
echo.

cd /d "%~dp0backend"

echo Step 1: Checking Railway CLI...
railway --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Railway CLI...
    call npm install -g @railway/cli
)

echo.
echo Step 2: Login to Railway...
echo Please login when browser opens, or use token method below
railway login
if %errorlevel% neq 0 (
    echo.
    echo Login failed. Trying with token...
    echo Please enter your Railway token (get from https://railway.app/account/tokens):
    set /p RAILWAY_TOKEN="Token: "
    if not "%RAILWAY_TOKEN%"=="" (
        set RAILWAY_TOKEN=%RAILWAY_TOKEN%
        railway login --browserless %RAILWAY_TOKEN%
    )
)

echo.
echo Step 3: Linking/Initializing Railway project...
railway link
if %errorlevel% neq 0 (
    echo Creating new Railway project...
    railway init --name cedos-backend
)

echo.
echo Step 4: Setting root directory to backend folder...
echo Note: Railway CLI sets root directory relative to current directory
echo Since we're in backend folder, root will be set correctly

echo.
echo Step 5: Enter your Supabase password:
set /p SUPABASE_PASSWORD="Supabase Password: "

if "%SUPABASE_PASSWORD%"=="" (
    echo [ERROR] Password is required!
    pause
    exit /b 1
)

echo.
echo Step 6: Setting environment variables...

echo   Setting DATABASE_URL...
railway variables set DATABASE_URL="postgresql://postgres:%SUPABASE_PASSWORD%@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres"

echo   Generating SECRET_KEY...
for /f "delims=" %%i in ('powershell -Command "$rng = [System.Security.Cryptography.RandomNumberGenerator]::Create(); $bytes = New-Object byte[] 32; $rng.GetBytes($bytes); [Convert]::ToBase64String($bytes)"') do set SECRET_KEY=%%i
railway variables set SECRET_KEY="%SECRET_KEY%"

echo   Setting CORS origins...
railway variables set BACKEND_CORS_ORIGINS=["*"]

echo.
echo Step 7: Deploying to Railway...
echo This will take 3-5 minutes...
railway up
if %errorlevel% neq 0 (
    echo [ERROR] Deployment failed
    echo Check the error above
    pause
    exit /b 1
)

echo.
echo Step 8: Running database migrations...
railway run alembic upgrade head

echo.
echo Step 9: Creating default users...
railway run python create_default_users.py

echo.
echo Step 10: Getting your deployment URL...
railway domain

echo.
echo ============================================================
echo   DEPLOYMENT COMPLETE!
echo ============================================================
echo.
echo Your backend is now live on Railway!
echo.
pause
