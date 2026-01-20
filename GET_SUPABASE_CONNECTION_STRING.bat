@echo off
REM ============================================================
REM   Get Correct Supabase Connection String
REM ============================================================

echo.
echo ============================================================
echo   Get Correct Supabase Connection String
echo ============================================================
echo.
echo Opening Supabase dashboard...
start https://supabase.com/dashboard

echo.
echo ============================================================
echo   Instructions
echo ============================================================
echo.
echo 1. In Supabase dashboard, click your project
echo.
echo 2. Go to: Settings - Database
echo.
echo 3. Look for "Connection string" section
echo.
echo 4. Find "Connection Pooling" tab
echo.
echo 5. Copy the "Connection string" (it will look like):
echo    postgres://postgres.PROJECT_REF:PASSWORD@pooler-host:6543/postgres
echo.
echo 6. The format should be:
echo    postgres://postgres.XXXXX:PASSWORD@aws-1-ap-south-1.pooler.supabase.com:6543/postgres
echo.
echo 7. Copy the ENTIRE connection string
echo.
echo 8. Use it in Railway DATABASE_URL
echo.
echo ============================================================
echo   Alternative: Direct Connection
echo ============================================================
echo.
echo If pooler doesn't work, try DIRECT connection:
echo.
echo 1. In Supabase dashboard - Settings - Database
echo 2. Find "Connection string" (not pooler)
echo 3. Copy the direct connection string
echo 4. Format: postgresql://postgres:PASSWORD@db.xxx.supabase.co:5432/postgres
echo.
echo ============================================================
echo.

pause
