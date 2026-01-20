@echo off
REM Start Backend Server Only

echo ============================================================
echo   Starting CEDOS Backend Server
echo ============================================================
echo.

cd /d "%~dp0backend"

if not exist "venv" (
    echo [ERROR] Virtual environment not found!
    echo Please run run_web_project.bat first to setup.
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting backend server...
echo Backend will be available at: http://localhost:8000
echo API docs at: http://localhost:8000/api/docs
echo.
echo Press Ctrl+C to stop the server
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
