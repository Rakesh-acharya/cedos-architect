@echo off
REM ============================================================
REM   Fix Supabase Pooler Connection Format
REM   Error: "Tenant or user not found" = Wrong username format!
REM ============================================================

echo.
echo ============================================================
echo   Fix Supabase Pooler Connection Format
echo ============================================================
echo.
echo ERROR: "Tenant or user not found"
echo.
echo This means the connection string format is wrong!
echo Supabase pooler needs: postgres.PROJECT_REF (not just postgres)
echo.
pause

cd /d "%~dp0backend"

REM Your credentials
set PASSWORD=Rakesh@123#$
set HOST=aws-1-ap-south-1.pooler.supabase.com
set PORT=6543

echo.
echo ============================================================
echo   Step 1: Get Supabase Project Reference
echo ============================================================
echo.
echo The pooler connection needs your PROJECT REFERENCE!
echo.
echo To find it:
echo   1. Go to: https://supabase.com/dashboard
echo   2. Your project - Settings - Database
echo   3. Look for "Connection string" or "Pooler connection"
echo   4. Find the PROJECT REF (usually 6-8 characters)
echo.
echo Example: If connection string shows:
echo   postgres://postgres.abcdefgh:PASSWORD@...
echo   Then PROJECT_REF is: abcdefgh
echo.
set /p PROJECT_REF="Enter your Supabase PROJECT REF: "

if "%PROJECT_REF%"=="" (
    echo.
    echo [ERROR] Project reference required!
    echo.
    echo Opening Supabase dashboard...
    start https://supabase.com/dashboard
    echo.
    echo Please get your PROJECT REF and run this script again.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   Step 2: URL-Encode Password
echo ============================================================
echo.

python -c "import urllib.parse; print(urllib.parse.quote('Rakesh@123#$', safe=''))" > %TEMP%\pwd.txt 2>nul
set /p ENCODED_PASSWORD=<%TEMP%\pwd.txt

if "%ENCODED_PASSWORD%"=="" (
    set ENCODED_PASSWORD=Rakesh%40123%23%24
)

echo Password encoded: %ENCODED_PASSWORD%

echo.
echo ============================================================
echo   Step 3: Construct Correct Connection String
echo ============================================================
echo.

REM Correct format for Supabase pooler:
REM postgresql://postgres.PROJECT_REF:PASSWORD@pooler-host:6543/postgres

set DATABASE_URL=postgresql://postgres.%PROJECT_REF%:%ENCODED_PASSWORD%@%HOST%:%PORT%/postgres

echo Correct DATABASE_URL format:
echo postgresql://postgres.%PROJECT_REF%:***@%HOST%:%PORT%/postgres
echo.

echo ============================================================
echo   Step 4: Update Railway
echo ============================================================
echo.

where railway >nul 2>&1
if %errorlevel% neq 0 (
    npm install -g @railway/cli
)

railway whoami >nul 2>&1
if %errorlevel% neq 0 (
    echo Please login to Railway...
    railway login
)

echo.
echo Setting DATABASE_URL in Railway...
railway variables set DATABASE_URL="%DATABASE_URL%"

if %errorlevel% equ 0 (
    echo [OK] DATABASE_URL updated!
) else (
    echo [WARNING] CLI command failed
)

echo.
echo Verifying...
railway variables | findstr DATABASE_URL

echo.
echo ============================================================
echo   Step 5: Test Connection
echo ============================================================
echo.

echo Testing connection...
railway run python -c "from app.core.database import engine; conn = engine.connect(); print('[SUCCESS] Connection works!'); conn.close()" 2>&1

echo.
echo ============================================================
echo   Step 6: Run Migrations
echo ============================================================
echo.

echo Running migrations...
railway run alembic upgrade head

echo.
echo ============================================================
echo   Step 7: Trigger Redeploy
echo ============================================================
echo.

railway up

echo.
echo ============================================================
echo   FIX COMPLETE!
echo ============================================================
echo.
echo Summary:
echo   - Using correct pooler format: postgres.%PROJECT_REF%
echo   - Password URL-encoded
echo   - DATABASE_URL updated in Railway
echo.
echo ============================================================
echo   Manual Fix (If Needed)
echo ============================================================
echo.
echo If CLI didn't work, set this in Railway dashboard:
echo.
echo DATABASE_URL = postgresql://postgres.%PROJECT_REF%:%ENCODED_PASSWORD%@%HOST%:%PORT%/postgres
echo.
echo Opening Railway dashboard...
start https://railway.app/dashboard
echo.
pause
