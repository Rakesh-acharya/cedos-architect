@echo off
REM Force Railway to redeploy with latest code

echo ============================================================
echo   Force Railway Redeploy
echo ============================================================
echo.

cd /d "%~dp0backend"

echo This will trigger a redeploy in Railway...
echo.

REM Make a small change to force redeploy
echo # Force redeploy > .railway_trigger
git add .railway_trigger
git commit -m "Force Railway redeploy - fix Alembic configparser issue"
git push

echo.
echo ============================================================
echo   Done!
echo ============================================================
echo.
echo Railway should now:
echo 1. Pull latest code (with fixed alembic/env.py)
echo 2. Build fresh (no cache)
echo 3. Run migrations successfully
echo 4. Deploy successfully
echo.
echo Check Railway dashboard for deployment status.
echo.

pause
