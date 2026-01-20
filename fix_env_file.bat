@echo off
REM Fix .env file format for CORS origins

echo Fixing .env file format...
cd /d "%~dp0backend"

if not exist ".env" (
    echo .env file not found. Creating new one...
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
    echo [OK] Created .env file
) else (
    echo Updating existing .env file...
    powershell -Command "$content = Get-Content .env -Raw; $content = $content -replace 'BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:8000', 'BACKEND_CORS_ORIGINS=[\"http://localhost:3000\",\"http://localhost:8000\"]'; $content = $content -replace 'BACKEND_CORS_ORIGINS=.*', 'BACKEND_CORS_ORIGINS=[\"http://localhost:3000\",\"http://localhost:8000\"]'; Set-Content .env -Value $content"
    echo [OK] Fixed .env file format
)

echo.
echo You can now run: run_web_project.bat
pause
