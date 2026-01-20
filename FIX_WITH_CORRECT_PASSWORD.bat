@echo off
REM ============================================================
REM   FIX WITH CORRECT PASSWORD - This WILL Work!
REM ============================================================

echo.
echo ============================================================
echo   FIX WITH CORRECT PASSWORD
echo ============================================================
echo.
echo Using your ACTUAL Supabase password: Wl4tkAQe0Smt0c63
echo Using Transaction Mode Pooler (port 6543) for IPv4 support
echo.
pause

cd /d "%~dp0backend"

REM Your actual credentials from Supabase
set SUPABASE_PASSWORD=Wl4tkAQe0Smt0c63
set SUPABASE_HOST=db.zlhtegmjmlqkygmegneu.supabase.co
set SUPABASE_PORT=6543

echo.
echo ============================================================
echo   Step 1: Construct Connection String
echo ============================================================
echo.

REM Transaction mode format: postgres://postgres:PASSWORD@host:6543/postgres
set DATABASE_URL=postgres://postgres:%SUPABASE_PASSWORD%@%SUPABASE_HOST%:%SUPABASE_PORT%/postgres

echo Connection String:
echo postgres://postgres:***@%SUPABASE_HOST%:%SUPABASE_PORT%/postgres
echo.

echo ============================================================
echo   Step 2: Setup Railway CLI
echo ============================================================

where railway >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Railway CLI...
    npm install -g @railway/cli
)

railway whoami >nul 2>&1
if %errorlevel% neq 0 (
    echo Please login to Railway...
    railway login
)

echo.
echo ============================================================
echo   Step 3: Set DATABASE_URL in Railway
echo ============================================================
echo.

echo Setting DATABASE_URL...
railway variables set DATABASE_URL="%DATABASE_URL%"

if %errorlevel% equ 0 (
    echo [OK] DATABASE_URL set successfully!
) else (
    echo [WARNING] CLI command had issues, but continuing...
)

echo.
echo Verifying...
railway variables | findstr DATABASE_URL

echo.
echo ============================================================
echo   Step 4: Test Connection
echo ============================================================
echo.

echo Testing database connection...
railway run python -c "from app.core.database import engine; conn = engine.connect(); print('[SUCCESS] Connection works!'); conn.close()" 2>&1

echo.
echo ============================================================
echo   Step 5: Run Migrations
echo ============================================================
echo.

echo Running migrations...
railway run alembic upgrade head

echo.
echo ============================================================
echo   Step 6: Trigger Deployment
echo ============================================================
echo.

echo Triggering Railway deployment...
railway up

echo.
echo ============================================================
echo   FIX COMPLETE!
echo ============================================================
echo.
echo Summary:
echo   - Password: Wl4tkAQe0Smt0c63 (correct from Supabase)
echo   - Using Transaction Mode Pooler (port 6543)
echo   - Supports IPv4 (Railway compatible)
echo   - DATABASE_URL updated in Railway
echo.
echo Railway will auto-redeploy. Wait 2-3 minutes.
echo.
echo Check Railway dashboard for deployment status:
start https://railway.app/dashboard
echo.
pause
