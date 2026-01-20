@echo off
REM Set DATABASE_URL in Railway via CLI

echo ============================================================
echo   Set Railway DATABASE_URL Environment Variable
echo ============================================================
echo.

cd /d "%~dp0backend"

echo Step 1: Enter your Supabase password:
echo (This will be used to set DATABASE_URL)
echo.
set /p SUPABASE_PASSWORD="Supabase Password: "

if "%SUPABASE_PASSWORD%"=="" (
    echo [ERROR] Password required!
    pause
    exit /b 1
)

echo.
echo Step 2: Setting DATABASE_URL in Railway...
railway variables set DATABASE_URL="postgresql://postgres:%SUPABASE_PASSWORD%@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres"

if %errorlevel% equ 0 (
    echo.
    echo [OK] DATABASE_URL set successfully!
    echo.
    echo Step 3: Verifying other variables...
    railway variables
    echo.
    echo Step 4: Redeploying...
    railway up
    echo.
    echo ============================================================
    echo   Done!
    echo ============================================================
    echo.
    echo Railway will now:
    echo 1. Build successfully
    echo 2. Connect to Supabase database
    echo 3. Run migrations
    echo 4. Start server
    echo.
) else (
    echo.
    echo [ERROR] Failed to set DATABASE_URL
    echo.
    echo Try manually:
    echo 1. Go to Railway dashboard
    echo 2. Your service - Variables tab
    echo 3. Add: DATABASE_URL = postgresql://postgres:%SUPABASE_PASSWORD%@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres
    echo.
)

pause
