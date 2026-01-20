@echo off
REM ============================================================
REM   Direct Railway Password Fix - Opens Browser
REM ============================================================

echo ============================================================
echo   Direct Railway Password Fix
echo ============================================================

cd /d "%~dp0backend"

REM Your exact credentials
set PASSWORD=Rakesh@123#$
set ENCODED=Rakesh%40123%23%24
set HOST=aws-1-ap-south-1.pooler.supabase.com
set PORT=5432

echo.
echo Opening Railway dashboard...
start https://railway.app/dashboard

echo.
echo ============================================================
echo   MANUAL FIX INSTRUCTIONS
echo ============================================================
echo.
echo Follow these steps in Railway dashboard:
echo.
echo 1. Click your service "cedos-architect"
echo.
echo 2. Go to "Variables" tab
echo.
echo 3. Find "DATABASE_URL" and click it
echo.
echo 4. Replace the value with this EXACT string:
echo.
echo    postgresql://postgres:Rakesh%%40123%%23%%24@aws-1-ap-south-1.pooler.supabase.com:5432/postgres
echo.
echo    (In Railway web UI, use single %% instead of %%%%)
echo.
echo 5. Click "Save"
echo.
echo 6. Railway will auto-redeploy
echo.
echo 7. Wait 2-3 minutes
echo.
echo 8. Check "Deploy Logs" - should show "Uvicorn running"
echo.
echo ============================================================
echo   OR USE CLI (Automated)
echo ============================================================
echo.

where railway >nul 2>&1
if %errorlevel% equ 0 (
    echo Using Railway CLI to set password...
    railway variables set DATABASE_URL="postgresql://postgres:%ENCODED%@%HOST%:%PORT%/postgres"
    echo.
    echo [OK] DATABASE_URL updated via CLI
    echo.
    echo Triggering redeploy...
    railway up
    echo.
    echo [OK] Deployment triggered!
) else (
    echo Railway CLI not found - use manual method above
)

echo.
echo ============================================================
echo   Password Encoding Reference
echo ============================================================
echo.
echo Original: Rakesh@123#$
echo Encoded:  Rakesh%40123%23%24
echo.
echo @ = %40
echo # = %23
echo $ = %24
echo.
pause
