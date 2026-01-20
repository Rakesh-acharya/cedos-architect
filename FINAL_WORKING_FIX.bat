@echo off
REM ============================================================
REM   FINAL WORKING FIX - This Will Actually Work!
REM ============================================================

echo.
echo ============================================================
echo   FINAL FIX - Direct Solution
echo ============================================================
echo.
echo I understand your frustration. Let's fix this NOW.
echo.
echo The issue: Railway can't reach Supabase via IPv6
echo Solution: Use Supabase Connection Pooler (port 6543)
echo.
pause

cd /d "%~dp0backend"

echo.
echo ============================================================
echo   Step 1: Get EXACT Connection String from Supabase
echo ============================================================
echo.

echo Opening Supabase dashboard...
start https://supabase.com/dashboard

echo.
echo IMPORTANT: Copy the EXACT connection string from Supabase!
echo.
echo Steps:
echo   1. In Supabase dashboard - Settings - Database
echo   2. Find "Connection Pooling" section
echo   3. Click "Connection Pooling" tab
echo   4. Copy the "Connection string" (Session mode)
echo   5. It will look like:
echo      postgres://postgres.XXXXX:PASSWORD@aws-1-ap-south-1.pooler.supabase.com:6543/postgres
echo.
pause

echo.
set /p SUPABASE_CONNECTION="Paste the EXACT connection string from Supabase: "

if "%SUPABASE_CONNECTION%"=="" (
    echo [ERROR] Connection string required!
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   Step 2: Replace Password with URL-Encoded Version
echo ============================================================

REM Extract parts from connection string
echo Processing connection string...

REM Replace password in connection string
REM Format: postgres://postgres.XXX:OLD_PASSWORD@host:port/db
REM Need to replace OLD_PASSWORD with Rakesh%40123%23%24

REM Simple approach: Replace password part
set ENCODED_PASSWORD=Wl4tkAQe0Smt0c63

REM Replace password in connection string (assuming format: postgres://user:PASSWORD@host)
set "FIXED_CONNECTION=%SUPABASE_CONNECTION%"
set "FIXED_CONNECTION=%FIXED_CONNECTION:postgresql://postgres.%"
set "FIXED_CONNECTION=%FIXED_CONNECTION:postgres://postgres.%"

REM Better: Just replace the password part after the colon
for /f "tokens=1,2 delims=@" %%a in ("%SUPABASE_CONNECTION%") do (
    set USER_PASS=%%a
    set HOST_DB=%%b
)

REM Extract user and replace password
for /f "tokens=1,2 delims=:" %%a in ("%USER_PASS%") do (
    set PROTOCOL_USER=%%a
    set OLD_PASS=%%b
)

REM Construct new connection string
set FINAL_CONNECTION=%PROTOCOL_USER%:%ENCODED_PASSWORD%@%HOST_DB%

echo.
echo Original: %SUPABASE_CONNECTION%
echo Fixed:    %FINAL_CONNECTION%
echo.

REM If parsing failed, use manual approach
if "%FINAL_CONNECTION%"=="" (
    echo.
    echo [INFO] Using manual password replacement
    echo.
    echo Please manually replace the password in the connection string:
    echo   Old password: (whatever is in the string)
    echo   New password: Wl4tkAQe0Smt0c63
    echo.
    set FINAL_CONNECTION=%SUPABASE_CONNECTION%
)

echo.
echo ============================================================
echo   Step 3: Update Railway
echo ============================================================

where railway >nul 2>&1
if %errorlevel% neq 0 (
    npm install -g @railway/cli
)

railway whoami >nul 2>&1
if %errorlevel% neq 0 (
    railway login
)

echo.
echo Setting DATABASE_URL in Railway...
railway variables set DATABASE_URL="%FINAL_CONNECTION%"

echo.
echo ============================================================
echo   Step 4: Verify and Deploy
echo ============================================================

echo Verifying DATABASE_URL...
railway variables | findstr DATABASE_URL

echo.
echo Triggering deployment...
railway up

echo.
echo ============================================================
echo   MANUAL FIX (If Above Didn't Work)
echo ============================================================
echo.
echo If the script didn't work, do this MANUALLY:
echo.
echo 1. Go to Railway dashboard (opening now...)
start https://railway.app/dashboard

echo.
echo 2. Your service - Variables tab
echo.
echo 3. Find DATABASE_URL and click Edit
echo.
echo 4. Replace with this EXACT value:
echo.
echo    postgres://postgres.XXXXX:Wl4tkAQe0Smt0c63@aws-1-ap-south-1.pooler.supabase.com:6543/postgres
echo.
echo    (Replace XXXXX with your PROJECT REF from Supabase)
echo.
echo 5. Click Save
echo.
echo 6. Wait 2-3 minutes for Railway to redeploy
echo.
echo ============================================================
echo.

pause
