@echo off
REM Simple CLI Deployment - Run from backend folder

echo ============================================================
echo   Simple Railway CLI Deployment
echo ============================================================
echo.

REM Navigate to backend folder (where Python app is)
cd /d "%~dp0backend"

echo [INFO] Current directory: %CD%
echo [INFO] This ensures Railway uses backend as root
echo.

echo Step 1: Railway Login...
railway login
if %errorlevel% neq 0 (
    echo.
    echo Login failed. You may need to login via browser first.
    pause
    exit /b 1
)

echo.
echo Step 2: Link to existing project or create new...
railway link
if %errorlevel% neq 0 (
    echo Creating new project...
    railway init
)

echo.
echo Step 3: Enter Supabase password:
set /p SUPABASE_PASSWORD="Password: "

if "%SUPABASE_PASSWORD%"=="" (
    echo [ERROR] Password required!
    pause
    exit /b 1
)

echo.
echo Step 4: Setting variables and deploying...
railway variables set DATABASE_URL="postgresql://postgres:%SUPABASE_PASSWORD%@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres"
railway variables set SECRET_KEY="cedos-secret-$(Get-Random)"
railway variables set BACKEND_CORS_ORIGINS=["*"]

echo.
echo Step 5: Deploying (this takes 3-5 minutes)...
railway up

echo.
echo Step 6: Post-deploy tasks...
railway run alembic upgrade head
railway run python create_default_users.py

echo.
echo Step 7: Your URL...
railway domain

echo.
echo ============================================================
echo   DONE!
echo ============================================================
pause
