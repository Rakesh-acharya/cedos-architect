@echo off
REM Simple script to set DATABASE_URL using Python (most reliable)

echo ============================================================
echo   Set Railway DATABASE_URL (URL-Encoded)
echo ============================================================
echo.

cd /d "%~dp0"

python SET_DATABASE_URL.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Python script failed!
    echo.
    echo Alternative: Use PowerShell script:
    echo   .\SET_DATABASE_URL_FIXED.ps1
    echo.
    pause
)
