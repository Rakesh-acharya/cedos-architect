@echo off
REM ============================================================
REM   Deploy CEDOS to FREE Hosting Platforms
REM   Frontend: Vercel | Backend: Railway | Database: Supabase
REM ============================================================

echo.
echo ============================================================
echo   CEDOS - Free Hosting Deployment
echo ============================================================
echo.
echo This will deploy your project to FREE hosting:
echo   Frontend:  Vercel (Free)
echo   Backend:   Railway (Free $5 credit)
echo   Database:  Supabase (Free 500MB)
echo.
echo Total Cost: $0/month
echo.
pause

echo.
echo ============================================================
echo   Step 1: Check Prerequisites
echo ============================================================
echo.

REM Check Node.js
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found!
    echo.
    echo Please install Node.js: https://nodejs.org/
    pause
    exit /b 1
)
echo [OK] Node.js found

REM Check npm
where npm >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] npm not found!
    pause
    exit /b 1
)
echo [OK] npm found

REM Check Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    echo.
    echo Please install Python: https://www.python.org/
    pause
    exit /b 1
)
echo [OK] Python found

REM Check Git
where git >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Git not found - some features may not work
) else (
    echo [OK] Git found
)

echo.
echo ============================================================
echo   Step 2: Setup Accounts
echo ============================================================
echo.
echo You need FREE accounts on these platforms:
echo.
echo 1. Vercel (Frontend): https://vercel.com/signup
echo 2. Railway (Backend):  https://railway.app/signup
echo 3. Supabase (Database): https://supabase.com/signup
echo.
choice /C YN /M "Do you have accounts on all platforms"

if errorlevel 2 (
    echo.
    echo Please create accounts and run this script again.
    echo.
    echo Opening signup pages...
    start https://vercel.com/signup
    start https://railway.app/signup
    start https://supabase.com/signup
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   Step 3: Deploy Frontend to Vercel
echo ============================================================
echo.

cd /d "%~dp0frontend"

REM Check if Vercel CLI is installed
where vercel >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Vercel CLI...
    npm install -g vercel
)

echo.
echo Logging in to Vercel...
vercel login

if %errorlevel% neq 0 (
    echo [ERROR] Vercel login failed!
    echo Please login manually and try again.
    pause
    exit /b 1
)

echo.
echo Deploying frontend to Vercel...
echo.
echo IMPORTANT: When asked:
echo   - Set up and deploy? Y
echo   - Which scope? [Your account]
echo   - Link to existing project? N
echo   - Project name? cedos-frontend
echo   - Directory? ./
echo   - Override settings? N
echo.
pause

vercel --prod

if %errorlevel% equ 0 (
    echo.
    echo [OK] Frontend deployed to Vercel!
    echo.
    echo Copy your Vercel URL (e.g., https://cedos-frontend.vercel.app)
    set /p VERCEL_URL="Vercel URL: "
) else (
    echo.
    echo [WARNING] Vercel deployment may have failed
    echo Please check the output above
    set /p VERCEL_URL="Vercel URL (if deployed): "
)

cd /d "%~dp0"

echo.
echo ============================================================
echo   Step 4: Setup Supabase Database
echo ============================================================
echo.

echo Please setup Supabase database:
echo.
echo 1. Go to: https://supabase.com/dashboard
echo 2. Create new project
echo 3. Copy connection string
echo.
set /p SUPABASE_URL="Supabase Connection String: "

if "%SUPABASE_URL%"=="" (
    echo [ERROR] Supabase URL required!
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   Step 5: Deploy Backend to Railway
echo ============================================================
echo.

cd /d "%~dp0backend"

REM Check if Railway CLI is installed
where railway >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Railway CLI...
    npm install -g @railway/cli
)

echo.
echo Logging in to Railway...
railway login

if %errorlevel% neq 0 (
    echo [ERROR] Railway login failed!
    echo Please login manually and try again.
    pause
    exit /b 1
)

echo.
echo Initializing Railway project...
railway init

echo.
echo Setting DATABASE_URL...
railway variables set DATABASE_URL="%SUPABASE_URL%"

echo.
echo Setting other environment variables...
railway variables set SECRET_KEY="cedos-secret-key-change-in-production"
railway variables set BACKEND_CORS_ORIGINS="[\"https://%VERCEL_URL:~8%\"]"

echo.
echo Deploying backend...
railway up

if %errorlevel% equ 0 (
    echo.
    echo [OK] Backend deployed to Railway!
    echo.
    echo Getting Railway URL...
    railway domain
    echo.
    set /p RAILWAY_URL="Railway Backend URL: "
) else (
    echo.
    echo [WARNING] Railway deployment may have failed
    echo Please check Railway dashboard
    set /p RAILWAY_URL="Railway Backend URL: "
)

cd /d "%~dp0"

echo.
echo ============================================================
echo   Step 6: Update Frontend API URL
echo ============================================================
echo.

cd /d "%~dp0frontend"

REM Check if config file exists
if exist "src\config.ts" (
    echo Updating API URL in config.ts...
    powershell -Command "(Get-Content src\config.ts) -replace 'http://localhost:8000', '%RAILWAY_URL%' | Set-Content src\config.ts"
    echo [OK] Config updated!
) else if exist "src\config.js" (
    echo Updating API URL in config.js...
    powershell -Command "(Get-Content src\config.js) -replace 'http://localhost:8000', '%RAILWAY_URL%' | Set-Content src\config.js"
    echo [OK] Config updated!
) else (
    echo [WARNING] Config file not found
    echo Please manually update API URL to: %RAILWAY_URL%
)

echo.
echo Redeploying frontend with updated API URL...
vercel --prod

cd /d "%~dp0"

echo.
echo ============================================================
echo   Deployment Complete!
echo ============================================================
echo.
echo Your CEDOS app is now live:
echo.
echo Frontend:  %VERCEL_URL%
echo Backend:   %RAILWAY_URL%
echo API Docs:  %RAILWAY_URL%/api/docs
echo Database:  Supabase (configured)
echo.
echo ============================================================
echo   Next Steps
echo ============================================================
echo.
echo 1. Run database migrations:
echo    cd backend
echo    railway run alembic upgrade head
echo.
echo 2. Test your deployment:
echo    - Frontend: %VERCEL_URL%
echo    - API: %RAILWAY_URL%/api/docs
echo.
echo 3. Share your app globally!
echo.
echo ============================================================
echo   Cost Summary
echo ============================================================
echo.
echo Frontend (Vercel):  FREE
echo Backend (Railway):  FREE ($5 credit/month)
echo Database (Supabase): FREE (500MB)
echo.
echo Total: $0/month
echo.
pause
