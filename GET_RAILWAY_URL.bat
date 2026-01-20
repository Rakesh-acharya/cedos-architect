@echo off
REM Get Railway Public URL

echo ============================================================
echo   Get Railway Public URL
echo ============================================================

cd /d "%~dp0backend"

where railway >nul 2>&1
if %errorlevel% neq 0 (
    npm install -g @railway/cli
)

railway whoami >nul 2>&1
if %errorlevel% neq 0 (
    railway login
)

echo.
echo Getting Railway public URL...
railway domain

echo.
echo ============================================================
echo   Your API is Live!
echo ============================================================
echo.
echo Copy the URL above and use it to access your API:
echo.
echo   API Base: https://your-url.railway.app
echo   API Docs: https://your-url.railway.app/api/docs
echo   Health:   https://your-url.railway.app/health
echo.
pause
