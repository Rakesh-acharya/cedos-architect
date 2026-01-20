@echo off
REM ============================================================
REM CEDOS Web Project - Complete Setup & Run Script (Batch)
REM ============================================================

echo ============================================================
echo   CEDOS - Civil Engineering Digital Operating System
echo   Web Project Setup ^& Run Script
echo ============================================================
echo.

REM Get the project root directory
set "PROJECT_ROOT=%~dp0"
set "BACKEND_DIR=%PROJECT_ROOT%backend"
set "FRONTEND_DIR=%PROJECT_ROOT%frontend"

REM Check if directories exist
if not exist "%BACKEND_DIR%" (
    echo [ERROR] Backend directory not found: %BACKEND_DIR%
    echo Please run this script from the project root directory.
    pause
    exit /b 1
)

if not exist "%FRONTEND_DIR%" (
    echo [ERROR] Frontend directory not found: %FRONTEND_DIR%
    echo Please run this script from the project root directory.
    pause
    exit /b 1
)

REM ============================================================
REM STEP 1: Check Prerequisites
REM ============================================================
echo [STEP 1] Checking Prerequisites...
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   [FAIL] Python not found. Please install Python 3.9+
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do echo   [OK] Python found: %%i
)

node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   [FAIL] Node.js not found. Please install Node.js 16+
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('node --version 2^>^&1') do echo   [OK] Node.js found: %%i
)

echo   [INFO] Ensure PostgreSQL is running and database is accessible
echo.

REM ============================================================
REM STEP 2: Backend Setup
REM ============================================================
echo [STEP 2] Setting up Backend...
echo.

cd /d "%BACKEND_DIR%"

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo   Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo   [FAIL] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo   [OK] Virtual environment created
) else (
    echo   [OK] Virtual environment already exists
)

REM Activate virtual environment and install dependencies
echo   Installing Python dependencies...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo   [WARN] Could not activate venv. Continuing anyway...
)

python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r requirements.txt
if %errorlevel% neq 0 (
    echo   [FAIL] Failed to install dependencies
    pause
    exit /b 1
)
echo   [OK] Dependencies installed

REM Check for .env file
if not exist ".env" (
    echo   [WARN] .env file not found. Creating from defaults...
    (
        echo # Database Configuration
        echo DATABASE_URL=postgresql://cedos_user:cedos_pass@localhost/cedos_db
        echo.
        echo # Security
        echo SECRET_KEY=your-secret-key-change-in-production-use-random-string
        echo.
        echo # CORS - JSON array format
        echo BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
    ) > .env
    echo   [OK] .env file created
    echo   Please update .env with your database credentials if needed
) else (
    echo   [OK] .env file exists
    echo   Checking .env file format...
    findstr /C:"BACKEND_CORS_ORIGINS" .env >nul
    if %errorlevel% equ 0 (
        REM Check if it's in wrong format and fix it
        powershell -Command "(Get-Content .env) -replace 'BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:8000', 'BACKEND_CORS_ORIGINS=[\"http://localhost:3000\",\"http://localhost:8000\"]' | Set-Content .env"
        echo   [OK] Fixed .env file format
    )
)

REM Run database migrations
echo   Running database migrations...
alembic upgrade head
if %errorlevel% neq 0 (
    echo   [WARN] Migration failed. Ensure database is running and accessible.
    echo   You can run migrations manually later: alembic upgrade head
)

echo.

REM ============================================================
REM STEP 3: Create Default Users
REM ============================================================
echo [STEP 3] Creating Default Users...
echo.

python create_default_users.py
if %errorlevel% neq 0 (
    echo   [WARN] User creation had issues. You can create users manually later.
)

echo.

REM ============================================================
REM STEP 4: Frontend Setup
REM ============================================================
echo [STEP 4] Setting up Frontend...
echo.

cd /d "%FRONTEND_DIR%"

if not exist "node_modules" (
    echo   Installing Node.js dependencies...
    call npm install
    if %errorlevel% neq 0 (
        echo   [FAIL] Failed to install frontend dependencies
        pause
        exit /b 1
    )
    echo   [OK] Frontend dependencies installed
) else (
    echo   [OK] Frontend dependencies already installed
)

echo.

REM ============================================================
REM STEP 5: Display Login Credentials
REM ============================================================
echo [STEP 5] Login Credentials
echo.
echo ============================================================
echo   DEFAULT USER CREDENTIALS
echo ============================================================
echo.
echo   ADMIN ^(Full Access^):
echo     Username: admin
echo     Password: admin123
echo     Email: admin@cedos.com
echo.
echo   ENGINEER:
echo     Username: engineer
echo     Password: engineer123
echo     Email: engineer@cedos.com
echo.
echo   SENIOR ENGINEER:
echo     Username: senior
echo     Password: senior123
echo     Email: senior@cedos.com
echo.
echo   PROJECT MANAGER:
echo     Username: manager
echo     Password: manager123
echo     Email: manager@cedos.com
echo.
echo   QUANTITY SURVEYOR:
echo     Username: qs
echo     Password: qs123
echo     Email: qs@cedos.com
echo.
echo   AUDITOR:
echo     Username: auditor
echo     Password: auditor123
echo     Email: auditor@cedos.com
echo.
echo   GOVERNMENT OFFICER:
echo     Username: govt
echo     Password: govt123
echo     Email: govt@cedos.com
echo.
echo ============================================================
echo.

REM ============================================================
REM STEP 6: Start Servers
REM ============================================================
echo [STEP 6] Starting Servers...
echo.
echo   Backend will start at: http://localhost:8000
echo   Frontend will start at: http://localhost:3000
echo.
echo   API Documentation: http://localhost:8000/api/docs
echo.
echo   Press Ctrl+C in each window to stop the servers
echo.

REM Start backend in new window
echo   Starting Backend Server...
cd /d "%BACKEND_DIR%"
start "CEDOS Backend" cmd /k "venv\Scripts\activate.bat && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a bit for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend in new window
echo   Starting Frontend Server...
cd /d "%FRONTEND_DIR%"
start "CEDOS Frontend" cmd /k "npm run dev"

echo.
echo ============================================================
echo   [SUCCESS] Servers are starting!
echo ============================================================
echo.
echo   Backend: http://localhost:8000
echo   Frontend: http://localhost:3000
echo.
echo   Login with any of the credentials above!
echo.
echo   To stop servers, close the Command Prompt windows or press Ctrl+C
echo.

cd /d "%PROJECT_ROOT%"
pause
