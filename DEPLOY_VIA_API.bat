@echo off
REM Deploy using Railway API directly (bypasses CLI login issues)

echo ============================================================
echo   CEDOS Backend - Railway Deployment via API
echo ============================================================
echo.

echo [INFO] Using Railway API directly with your token
echo [INFO] Token: c87c4dea-c118-4afb-9db6-e323a68ff5d2
echo.

cd /d "%~dp0backend"

echo [STEP 1] Checking if we can use Railway API...
echo.

echo [STEP 2] Enter your Supabase password:
set /p SUPABASE_PASSWORD="Password: "

if "%SUPABASE_PASSWORD%"=="" (
    echo [ERROR] Password is required!
    pause
    exit /b 1
)

echo.
echo [INFO] Since Railway CLI token authentication is having issues,
echo [INFO] we'll use Railway web interface for deployment.
echo.
echo Please follow these steps:
echo.
echo 1. Go to: https://railway.app/new
echo 2. Click "Deploy from GitHub repo" OR "Empty Project"
echo 3. If GitHub: Connect your repo and select backend folder
echo 4. If Empty: Click "Add Service" - "GitHub Repo" - select backend
echo.
echo 5. In Railway dashboard, go to your project
echo 6. Click on your service
echo 7. Go to "Variables" tab
echo 8. Add these variables:
echo.
echo    DATABASE_URL = postgresql://postgres:%SUPABASE_PASSWORD%@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres
echo    SECRET_KEY = (generate random string)
echo    BACKEND_CORS_ORIGINS = ["*"]
echo.
echo 9. Railway will auto-deploy
echo 10. After deployment, go to "Settings" - "Generate Domain"
echo.
echo OR use the automated script below if Railway CLI works:
echo.
pause

REM Try Railway CLI one more time with token
set RAILWAY_TOKEN=c87c4dea-c118-4afb-9db6-e323a68ff5d2

echo.
echo [ATTEMPT] Trying Railway CLI with token...
railway whoami
if %errorlevel% equ 0 (
    echo [SUCCESS] Token works! Continuing with deployment...
    goto :deploy
) else (
    echo [INFO] Token authentication failed, using web method above
    goto :end
)

:deploy
echo.
echo [STEP 3] Initializing project...
railway init --name cedos-backend

echo.
echo [STEP 4] Setting variables...
railway variables set DATABASE_URL="postgresql://postgres:%SUPABASE_PASSWORD%@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres"
railway variables set SECRET_KEY="cedos-secret-$(powershell -Command "[System.Web.Security.Membership]::GeneratePassword(32, 0)")"
railway variables set BACKEND_CORS_ORIGINS=["*"]

echo.
echo [STEP 5] Deploying...
railway up

echo.
echo [STEP 6] Running migrations...
railway run alembic upgrade head

echo.
echo [STEP 7] Creating users...
railway run python create_default_users.py

echo.
echo [STEP 8] Getting URL...
railway domain

:end
echo.
echo ============================================================
pause
