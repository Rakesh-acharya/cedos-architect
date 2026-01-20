@echo off
REM Set DATABASE_URL with Supabase Connection Pooler (port 6543)
REM This fixes IPv6 network connectivity issues on Railway

echo ============================================================
echo   Set Railway DATABASE_URL (Connection Pooler)
echo ============================================================
echo.

cd /d "%~dp0backend"

echo Enter your Supabase password:
echo (Special characters will be automatically URL-encoded)
echo.
set /p SUPABASE_PASSWORD="Supabase Password: "

if "%SUPABASE_PASSWORD%"=="" (
    echo [ERROR] Password required!
    pause
    exit /b 1
)

echo.
echo URL-encoding password...
echo.

REM Use Python to URL-encode the password (more reliable)
for /f "delims=" %%i in ('python -c "import urllib.parse; print(urllib.parse.quote('%SUPABASE_PASSWORD%', safe=''))"') do set PASSWORD_ENCODED=%%i

REM If Python not available, try PowerShell
if "%PASSWORD_ENCODED%"=="" (
    for /f "delims=" %%i in ('powershell -Command "[System.Web.HttpUtility]::UrlEncode('%SUPABASE_PASSWORD%')"') do set PASSWORD_ENCODED=%%i
)

REM Construct DATABASE_URL with CONNECTION POOLER (port 6543)
set DATABASE_URL=postgresql://postgres:%PASSWORD_ENCODED%@db.zlhtegmjmlqkygmegneu.supabase.co:6543/postgres

echo.
echo Setting DATABASE_URL in Railway (Connection Pooler - port 6543)...
echo.

railway variables set DATABASE_URL="%DATABASE_URL%"

if %errorlevel% equ 0 (
    echo.
    echo [OK] DATABASE_URL set successfully with Connection Pooler!
    echo.
    echo Verifying variables...
    railway variables
    echo.
    echo Redeploying...
    railway up
    echo.
    echo ============================================================
    echo   Done!
    echo ============================================================
    echo.
    echo The DATABASE_URL now uses Supabase Connection Pooler (port 6543).
    echo This fixes IPv6 network connectivity issues on Railway.
    echo.
    echo Railway will now:
    echo 1. Connect via connection pooler
    echo 2. Handle IPv6/IPv4 properly
    echo 3. Run migrations successfully
    echo 4. Deploy successfully
    echo.
) else (
    echo.
    echo [ERROR] Failed to set DATABASE_URL
    echo.
    echo Try manually in Railway dashboard:
    echo 1. Go to Railway dashboard
    echo 2. Your service - Variables tab
    echo 3. Update: DATABASE_URL
    echo 4. Value: %DATABASE_URL%
    echo.
    echo IMPORTANT: Change port from 5432 to 6543 (Connection Pooler)
    echo.
)

pause
