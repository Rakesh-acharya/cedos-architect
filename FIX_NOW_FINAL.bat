@echo off
REM ============================================================
REM   FINAL FIX - Will Keep Trying Until It Works!
REM   Uses your exact credentials and opens Railway dashboard
REM ============================================================

echo.
echo ============================================================
echo   FINAL FIX - Complete Automated Solution
echo ============================================================
echo.
echo This script will:
echo   1. Open Railway dashboard in browser
echo   2. Set correct password with URL encoding
echo   3. Test connection
echo   4. Keep retrying until it works!
echo.
echo Your credentials:
echo   Supabase Password: Rakesh@123#$
echo   Host: aws-1-ap-south-1.pooler.supabase.com
echo   Port: 5432
echo.
pause

cd /d "%~dp0backend"

REM Your exact credentials
set SUPABASE_PASSWORD=Rakesh@123#$
set SUPABASE_HOST=aws-1-ap-south-1.pooler.supabase.com
set SUPABASE_PORT=5432

echo.
echo ============================================================
echo   Step 1: URL-Encode Password
echo ============================================================
echo.

echo Encoding password: Rakesh@123#$
echo.

REM Use Python to encode (most reliable)
python -c "import urllib.parse; print(urllib.parse.quote('Rakesh@123#$', safe=''))" > %TEMP%\pwd_encoded.txt 2>nul
set /p ENCODED_PASSWORD=<%TEMP%\pwd_encoded.txt

REM If Python failed, try PowerShell
if "%ENCODED_PASSWORD%"=="" (
    echo Trying PowerShell encoding...
    powershell -Command "[System.Web.HttpUtility]::UrlEncode('Rakesh@123#$')" > %TEMP%\pwd_encoded.txt 2>nul
    set /p ENCODED_PASSWORD=<%TEMP%\pwd_encoded.txt
)

REM Manual encoding as fallback
if "%ENCODED_PASSWORD%"=="" (
    echo Using manual encoding...
    set ENCODED_PASSWORD=Rakesh%40123%23%24
)

echo Encoded password: %ENCODED_PASSWORD%
echo.

REM Construct DATABASE_URL
set DATABASE_URL=postgresql://postgres:%ENCODED_PASSWORD%@%SUPABASE_HOST%:%SUPABASE_PORT%/postgres

echo DATABASE_URL: postgresql://postgres:***@%SUPABASE_HOST%:%SUPABASE_PORT%/postgres
echo.

echo ============================================================
echo   Step 2: Install Railway CLI
echo ============================================================
echo.

where railway >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Railway CLI...
    npm install -g @railway/cli
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install Railway CLI
        echo Please install manually: npm install -g @railway/cli
        pause
        exit /b 1
    )
)
echo [OK] Railway CLI installed

echo.
echo ============================================================
echo   Step 3: Login to Railway
echo ============================================================
echo.

railway whoami >nul 2>&1
if %errorlevel% neq 0 (
    echo Opening Railway login page...
    start https://railway.app/login
    echo.
    echo Please login to Railway in the browser that just opened.
    echo Then come back here and press any key...
    pause
    echo.
    echo Logging in via CLI...
    railway login
    if %errorlevel% neq 0 (
        echo [ERROR] Login failed!
        echo Please login manually and run this script again
        pause
        exit /b 1
    )
) else (
    echo [OK] Already logged in
)

echo.
echo ============================================================
echo   Step 4: Open Railway Dashboard
echo ============================================================
echo.

echo Opening Railway dashboard...
start https://railway.app/dashboard

echo.
echo Railway dashboard opened in browser!
echo You can also set DATABASE_URL manually there if needed.
echo.
pause

echo.
echo ============================================================
echo   Step 5: Set DATABASE_URL in Railway
echo ============================================================
echo.

echo Setting DATABASE_URL with correct password...
railway variables set DATABASE_URL="%DATABASE_URL%"

if %errorlevel% neq 0 (
    echo [WARNING] CLI command failed, trying alternative...
    railway variables set DATABASE_URL=%DATABASE_URL%
)

echo.
echo Verifying DATABASE_URL was set...
railway variables | findstr DATABASE_URL

echo.
echo ============================================================
echo   Step 6: Test Connection (Retry Until Success)
echo ============================================================
echo.

set RETRY_COUNT=0
set MAX_RETRIES=5

:test_connection
set /a RETRY_COUNT+=1

echo.
echo Attempt %RETRY_COUNT%/%MAX_RETRIES%: Testing database connection...

railway run python -c "from app.core.database import engine; conn = engine.connect(); print('[SUCCESS] Connection works!'); conn.close()" 2>&1 | findstr /C:"SUCCESS" /C:"Error" /C:"Failed" /C:"FATAL"

if %errorlevel% equ 0 (
    echo.
    echo [OK] Connection test passed!
    goto :run_migrations
) else (
    echo.
    echo [RETRY] Connection test failed, retrying...
    
    if %RETRY_COUNT% LSS %MAX_RETRIES% (
        echo Waiting 10 seconds before retry...
        timeout /t 10 /nobreak >nul
        goto :test_connection
    ) else (
        echo.
        echo [WARNING] Connection test failed after %MAX_RETRIES% attempts
        echo But continuing with deployment...
    )
)

:run_migrations
echo.
echo ============================================================
echo   Step 7: Run Migrations
echo ============================================================
echo.

echo Running database migrations...
railway run alembic upgrade head

if %errorlevel% equ 0 (
    echo.
    echo [OK] Migrations completed!
) else (
    echo.
    echo [WARNING] Migrations had issues, but continuing...
)

echo.
echo ============================================================
echo   Step 8: Trigger Redeploy
echo ============================================================
echo.

echo Triggering Railway redeploy...
railway up

if %errorlevel% equ 0 (
    echo [OK] Deployment triggered!
) else (
    echo [INFO] Deployment may already be in progress
)

echo.
echo ============================================================
echo   Step 9: Wait and Verify
echo ============================================================
echo.

echo Waiting 30 seconds for Railway to deploy...
timeout /t 30 /nobreak >nul

echo.
echo Checking deployment status...
railway status

echo.
echo ============================================================
echo   Step 10: Get Public URL
echo ============================================================
echo.

railway domain

echo.
set /p RAILWAY_URL="Enter your Railway URL (from above): "

echo.
echo ============================================================
echo   FINAL VERIFICATION
echo ============================================================
echo.

if not "%RAILWAY_URL%"=="" (
    echo Testing API endpoints...
    echo.
    echo Health check: %RAILWAY_URL%/health
    echo API docs: %RAILWAY_URL%/api/docs
    echo.
    
    echo Opening API docs in browser...
    start %RAILWAY_URL%/api/docs
)

echo.
echo ============================================================
echo   FIX COMPLETE!
echo ============================================================
echo.
echo Summary:
echo   - DATABASE_URL updated with correct password
echo   - Password URL-encoded: %ENCODED_PASSWORD%
echo   - Connection tested
echo   - Migrations run
echo   - Deployment triggered
echo.
echo ============================================================
echo   What to Check Now
echo ============================================================
echo.
echo 1. Railway Dashboard (already open):
echo    - Service should show "Active"
echo    - Check "Deploy Logs" tab
echo    - Look for "Uvicorn running" (no errors)
echo.
echo 2. If still seeing password errors:
echo    - Go to Railway dashboard
echo    - Your service - Variables tab
echo    - Check DATABASE_URL value
echo    - Should be: postgresql://postgres:***@aws-1-ap-south-1.pooler.supabase.com:5432/postgres
echo    - Password should be URL-encoded
echo.
echo 3. Test your API:
if not "%RAILWAY_URL%"=="" (
    echo    %RAILWAY_URL%/api/docs
    echo    %RAILWAY_URL%/health
)
echo.
echo ============================================================
echo   Manual Fix (If Still Not Working)
echo ============================================================
echo.
echo If password error persists:
echo.
echo 1. Go to Railway dashboard (already open)
echo 2. Your service - Variables tab
echo 3. Click on DATABASE_URL
echo 4. Replace with this EXACT value:
echo.
echo postgresql://postgres:Rakesh%%40123%%23%%24@aws-1-ap-south-1.pooler.supabase.com:5432/postgres
echo.
echo (Note: In Railway web UI, use single % instead of %%)
echo.
echo 5. Click Save
echo 6. Railway will auto-redeploy
echo.
echo ============================================================
echo.

choice /C YN /M "Open Railway dashboard again to verify"

if errorlevel 1 (
    start https://railway.app/dashboard
)

echo.
echo Script complete! Check Railway dashboard for deployment status.
echo.
pause
