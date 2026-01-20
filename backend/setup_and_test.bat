@echo off
REM CEDOS Setup and Test Script for Windows

echo ============================================================
echo CEDOS - Setup and Test Script
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt
pip install pytest pytest-cov requests

REM Check for .env file
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Please create .env file with your database credentials.
    echo Example:
    echo DATABASE_URL=postgresql://postgres:PASSWORD@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres
    echo SECRET_KEY=your-secret-key
    echo.
    pause
    exit /b 1
)

REM Run migrations
echo.
echo Running database migrations...
alembic upgrade head

REM Run tests
echo.
echo Running comprehensive tests...
python test_and_run.py

echo.
echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo To start the server:
echo   uvicorn app.main:app --reload
echo.
pause
