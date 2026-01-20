@echo off
REM Deploy Backend to Railway (FREE)

echo ============================================================
echo   Deploy Backend to Railway (FREE)
echo ============================================================
echo.

cd /d "%~dp0backend"

REM Check if Railway CLI is installed
where railway >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Railway CLI...
    npm install -g @railway/cli
)

echo Logging in to Railway...
railway login

echo.
echo Initializing Railway project...
railway init

echo.
echo Setting environment variables...
echo.
set /p DATABASE_URL="Enter DATABASE_URL (Supabase): "

if "%DATABASE_URL%"=="" (
    echo [ERROR] DATABASE_URL required!
    pause
    exit /b 1
)

railway variables set DATABASE_URL="%DATABASE_URL%"
railway variables set SECRET_KEY="cedos-secret-key-change-in-production"
railway variables set BACKEND_CORS_ORIGINS="[\"*\"]"

echo.
echo Deploying backend...
railway up

echo.
echo [OK] Backend deployed!
echo.
echo Getting your Railway URL...
railway domain
echo.
echo Your backend is live! Check Railway dashboard for URL.
echo.
pause
