@echo off
REM Quick Railway Deployment - Minimal Steps

echo ============================================================
echo   Quick Railway Deployment
echo ============================================================
echo.

cd /d "%~dp0backend"

REM Check Railway CLI
where railway >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Railway CLI...
    npm install -g @railway/cli
)

REM Login if needed
railway whoami >nul 2>&1
if %errorlevel% neq 0 (
    railway login
)

REM Initialize if needed
railway status >nul 2>&1
if %errorlevel% neq 0 (
    railway init
)

echo.
echo Enter your Supabase connection string:
echo Format: postgresql://postgres:PASSWORD@db.xxx.supabase.co:5432/postgres
set /p DB_URL="Database URL: "

if "%DB_URL%"=="" (
    echo [ERROR] Database URL required!
    pause
    exit /b 1
)

echo.
echo Setting up Railway...
railway variables set DATABASE_URL="%DB_URL%"
railway variables set SECRET_KEY="cedos-secret-key-$(date +%s)"
railway variables set BACKEND_CORS_ORIGINS="[\"*\"]"

echo.
echo Running migrations...
railway run alembic upgrade head

echo.
echo Deploying...
railway up

echo.
echo [OK] Deployment complete!
echo.
railway domain
echo.
echo Your backend is now globally accessible!
echo.
pause
