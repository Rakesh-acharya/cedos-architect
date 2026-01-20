@echo off
REM ============================================================
REM   Fix Supabase Password Authentication Error
REM ============================================================

echo.
echo ============================================================
echo   Fix Supabase Password Authentication
echo ============================================================
echo.
echo ERROR: Password authentication failed for Supabase
echo.
echo This means the DATABASE_URL in Railway has wrong password.
echo.
pause

cd /d "%~dp0backend"

REM Check Railway CLI
where railway >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Railway CLI...
    npm install -g @railway/cli
)

REM Check if logged in
railway whoami >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo Please login to Railway...
    railway login
)

echo.
echo ============================================================
echo   Step 1: Get Correct Supabase Password
echo ============================================================
echo.
echo To get your Supabase password:
echo.
echo Option 1: Reset Database Password
echo   1. Go to: https://supabase.com/dashboard
echo   2. Select your project
echo   3. Settings - Database
echo   4. Click "Reset database password"
echo   5. Copy the new password
echo.
echo Option 2: Find Existing Password
echo   1. Go to: https://supabase.com/dashboard
echo   2. Settings - Database
echo   3. Look for connection string or password field
echo.
pause

echo.
echo ============================================================
echo   Step 2: Enter Supabase Connection Details
echo ============================================================
echo.

set /p SUPABASE_HOST="Supabase Host (e.g., db.xxx.supabase.co): "
set /p SUPABASE_PASSWORD="Supabase Password: "
set /p SUPABASE_PORT="Port (5432 or 6543 for pooler): "

if "%SUPABASE_PORT%"=="" set SUPABASE_PORT=5432

if "%SUPABASE_HOST%"=="" (
    echo [ERROR] Host required!
    pause
    exit /b 1
)

if "%SUPABASE_PASSWORD%"=="" (
    echo [ERROR] Password required!
    pause
    exit /b 1
)

echo.
echo URL-encoding password...
echo.

REM Use Python to URL-encode password
for /f "delims=" %%i in ('python -c "import urllib.parse; print(urllib.parse.quote('%SUPABASE_PASSWORD%', safe=''))"') do set PASSWORD_ENCODED=%%i

REM If Python not available, try PowerShell
if "%PASSWORD_ENCODED%"=="" (
    for /f "delims=" %%i in ('powershell -Command "[System.Web.HttpUtility]::UrlEncode('%SUPABASE_PASSWORD%')"') do set PASSWORD_ENCODED=%%i
)

REM Construct DATABASE_URL
set DATABASE_URL=postgresql://postgres:%PASSWORD_ENCODED%@%SUPABASE_HOST%:%SUPABASE_PORT%/postgres

echo.
echo ============================================================
echo   Step 3: Update DATABASE_URL in Railway
echo ============================================================
echo.

echo Setting DATABASE_URL in Railway...
railway variables set DATABASE_URL="%DATABASE_URL%"

if %errorlevel% equ 0 (
    echo.
    echo [OK] DATABASE_URL updated successfully!
    echo.
    echo Verifying...
    railway variables
    echo.
    echo ============================================================
    echo   Step 4: Test Connection
    echo ============================================================
    echo.
    echo Testing database connection...
    railway run python -c "from app.core.database import engine; conn = engine.connect(); print('Connection successful!'); conn.close()"
    
    if %errorlevel% equ 0 (
        echo.
        echo [OK] Database connection successful!
        echo.
        echo ============================================================
        echo   Step 5: Run Migrations
        echo ============================================================
        echo.
        echo Running migrations...
        railway run alembic upgrade head
        
        if %errorlevel% equ 0 (
            echo.
            echo [OK] Migrations completed!
            echo.
            echo ============================================================
            echo   Fix Complete!
            echo ============================================================
            echo.
            echo Your Railway deployment should now work!
            echo.
            echo Railway will auto-redeploy with the new DATABASE_URL.
            echo.
        ) else (
            echo.
            echo [WARNING] Migrations may have failed
            echo Check Railway logs for details
        )
    ) else (
        echo.
        echo [ERROR] Connection test failed
        echo Please verify:
        echo   1. Password is correct
        echo   2. Host is correct
        echo   3. Supabase project is active
    )
) else (
    echo.
    echo [ERROR] Failed to set DATABASE_URL
    echo.
    echo Try manually in Railway dashboard:
    echo   1. Go to Railway dashboard
    echo   2. Your service - Variables tab
    echo   3. Update DATABASE_URL
    echo   4. Value: %DATABASE_URL%
)

echo.
pause
