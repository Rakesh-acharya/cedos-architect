@echo off
REM Set DATABASE_URL in Railway with proper URL encoding
REM This handles passwords with special characters

echo ============================================================
echo   Set Railway DATABASE_URL (URL-Encoded)
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

REM Construct DATABASE_URL
set DATABASE_URL=postgresql://postgres:%PASSWORD_ENCODED%@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres

echo Setting DATABASE_URL in Railway...
echo.

railway variables set DATABASE_URL="%DATABASE_URL%"

if %errorlevel% equ 0 (
    echo.
    echo [OK] DATABASE_URL set successfully!
    echo.
    echo Verifying variables...
    railway variables
    echo.
    echo Redeploying...
    railway up
    echo.
    echo ============================================================
    echo   Done! Railway will auto-redeploy
    echo ============================================================
    echo.
    echo The DATABASE_URL has been set with proper URL encoding.
    echo Special characters in password are now properly encoded.
    echo.
) else (
    echo.
    echo [ERROR] Failed to set DATABASE_URL
    echo.
    echo Try manually in Railway dashboard:
    echo 1. Go to Railway dashboard
    echo 2. Your service - Variables tab
    echo 3. Add: DATABASE_URL
    echo 4. Value: %DATABASE_URL%
    echo.
)

pause
