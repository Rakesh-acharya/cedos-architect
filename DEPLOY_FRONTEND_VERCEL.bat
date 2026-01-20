@echo off
REM Deploy Frontend to Vercel (FREE)

echo ============================================================
echo   Deploy Frontend to Vercel (FREE)
echo ============================================================
echo.

cd /d "%~dp0frontend"

REM Check if Vercel CLI is installed
where vercel >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Vercel CLI...
    npm install -g vercel
)

echo Logging in to Vercel...
vercel login

echo.
echo Deploying frontend...
echo.
echo When asked:
echo   - Set up and deploy? Y
echo   - Which scope? [Your account]
echo   - Link to existing project? N
echo   - Project name? cedos-frontend
echo   - Directory? ./
echo.
pause

vercel --prod

echo.
echo [OK] Frontend deployed!
echo.
echo Your app is live at: https://cedos-frontend.vercel.app
echo (Check the URL shown above)
echo.
pause
