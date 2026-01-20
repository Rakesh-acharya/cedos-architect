@echo off
REM ============================================================
REM   Start Global Deployment - One-Click Deploy
REM ============================================================

echo.
echo ============================================================
echo   CEDOS - Global Deployment Starter
echo ============================================================
echo.
echo This will deploy your CEDOS app globally!
echo.
echo What will happen:
echo   1. Backend deployed to Railway (globally accessible)
echo   2. Database migrations run automatically
echo   3. Default users created
echo   4. API available worldwide
echo.
echo Total time: ~5-10 minutes
echo Cost: FREE (Railway free tier)
echo.
pause

echo.
echo Starting deployment...
echo.

call DEPLOY_TO_RAILWAY_COMPLETE.bat

echo.
echo ============================================================
echo   Deployment Complete!
echo ============================================================
echo.
echo Your CEDOS backend is now globally accessible!
echo.
echo Next: Deploy frontend to make it a complete web app
echo       Run: .\DEPLOY_FRONTEND_VERCEL.bat
echo.
pause
