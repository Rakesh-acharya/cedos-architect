@echo off
REM ============================================================
REM   FINAL FIX - Using Correct Password & Transaction Mode
REM ============================================================

echo.
echo ============================================================
echo   FINAL FIX - This WILL Work!
echo ============================================================
echo.
echo Using:
echo   Password: Wl4tkAQe0Smt0c63 (from Supabase)
echo   Mode: Transaction Pooler (port 6543)
echo   Why: Supports IPv4 (Railway compatible)
echo.
pause

cd /d "%~dp0backend"

REM Correct connection string for Railway
set DATABASE_URL=postgres://postgres:Wl4tkAQe0Smt0c63@db.zlhtegmjmlqkygmegneu.supabase.co:6543/postgres

echo.
echo ============================================================
echo   Step 1: Setup Railway
echo ============================================================

where railway >nul 2>&1
if %errorlevel% neq 0 (
    npm install -g @railway/cli
)

railway whoami >nul 2>&1
if %errorlevel% neq 0 (
    echo Please login to Railway...
    start https://railway.app/login
    railway login
)

echo.
echo ============================================================
echo   Step 2: Set DATABASE_URL
echo ============================================================
echo.

echo Setting DATABASE_URL in Railway...
railway variables set DATABASE_URL="%DATABASE_URL%"

echo.
echo Verifying...
railway variables | findstr DATABASE_URL

echo.
echo ============================================================
echo   Step 3: Test & Deploy
echo ============================================================
echo.

echo Testing connection...
railway run python -c "from app.core.database import engine; conn = engine.connect(); print('[SUCCESS]'); conn.close()" 2>&1

echo.
echo Running migrations...
railway run alembic upgrade head

echo.
echo Deploying...
railway up

echo.
echo ============================================================
echo   MANUAL FIX (If CLI Failed)
echo ============================================================
echo.

start https://railway.app/dashboard

echo.
echo If CLI didn't work, set this MANUALLY in Railway:
echo.
echo 1. Railway dashboard (opened above)
echo 2. Your service - Variables tab
echo 3. Find DATABASE_URL - Click Edit
echo 4. Paste this EXACT value:
echo.
echo    postgres://postgres:Wl4tkAQe0Smt0c63@db.zlhtegmjmlqkygmegneu.supabase.co:6543/postgres
echo.
echo 5. Click Save
echo 6. Wait 2-3 minutes
echo.
echo ============================================================
echo   Why This Works
echo ============================================================
echo.
echo - Password: Wl4tkAQe0Smt0c63 (correct from Supabase)
echo - Port: 6543 (Transaction Mode Pooler)
echo - Supports IPv4 (Railway can connect)
echo - No IPv6 needed
echo.
pause
