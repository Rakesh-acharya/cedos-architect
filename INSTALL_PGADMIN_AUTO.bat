@echo off
REM ============================================================
REM   Auto Install & Configure pgAdmin for CEDOS
REM   pgAdmin is 100% FREE and Open Source!
REM ============================================================

echo.
echo ============================================================
echo   CEDOS - Auto Install pgAdmin
echo ============================================================
echo.
echo pgAdmin is 100%% FREE and Open Source!
echo It's the best GUI tool for PostgreSQL (like phpMyAdmin)
echo.
pause

REM Check if pgAdmin is already installed
where pgAdmin4 >nul 2>&1
if %errorlevel% equ 0 (
    echo.
    echo [OK] pgAdmin is already installed!
    echo.
    goto :configure
)

echo.
echo ============================================================
echo   Step 1: Download pgAdmin
echo ============================================================
echo.

set PGADMIN_URL=https://www.pgadmin.org/download/pgadmin-4-windows/
set DOWNLOAD_DIR=%TEMP%\pgadmin_installer.exe

echo Downloading pgAdmin installer...
echo.
echo This may take a few minutes...
echo.

REM Try to download using PowerShell
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://www.pgadmin.org/static/packages_pgadmin_org/pgadmin4/v8.0/windows/pgadmin4-8.0-x64.exe' -OutFile '%DOWNLOAD_DIR%'}" 2>nul

if exist "%DOWNLOAD_DIR%" (
    echo [OK] Download complete!
    echo.
    echo ============================================================
    echo   Step 2: Install pgAdmin
    echo ============================================================
    echo.
    echo The installer will now open.
    echo.
    echo IMPORTANT: During installation:
    echo   1. Click "Next" through the wizard
    echo   2. Choose installation directory (default is fine)
    echo   3. Click "Install"
    echo   4. Wait for installation to complete
    echo   5. Click "Finish"
    echo.
    pause
    
    echo.
    echo Starting installer...
    start /wait "" "%DOWNLOAD_DIR%"
    
    REM Clean up installer
    del "%DOWNLOAD_DIR%" 2>nul
    
    echo.
    echo [OK] Installation complete!
    echo.
) else (
    echo.
    echo [WARNING] Automatic download failed.
    echo.
    echo Please download manually:
    echo   1. Go to: https://www.pgadmin.org/download/
    echo   2. Download pgAdmin 4 for Windows
    echo   3. Run the installer
    echo   4. Then run this script again
    echo.
    echo Opening download page...
    start https://www.pgadmin.org/download/
    pause
    exit /b 1
)

:configure
echo.
echo ============================================================
echo   Step 3: Configure PostgreSQL Database
echo ============================================================
echo.

REM Check if PostgreSQL is installed
where psql >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] PostgreSQL not found!
    echo.
    echo Please install PostgreSQL first:
    echo   1. Download: https://www.postgresql.org/download/windows/
    echo   2. Install with default settings
    echo   3. Run this script again
    echo.
    pause
    exit /b 1
)

echo [OK] PostgreSQL found!
echo.

REM Get PostgreSQL password
echo Enter PostgreSQL postgres user password:
set /p POSTGRES_PASSWORD="Password: "

if "%POSTGRES_PASSWORD%"=="" (
    echo [ERROR] Password required!
    pause
    exit /b 1
)

echo.
echo Creating database and user...
echo.

REM Set PGPASSWORD environment variable
set PGPASSWORD=%POSTGRES_PASSWORD%

REM Create database
psql -U postgres -c "CREATE DATABASE cedos_db;" 2>nul
if %errorlevel% equ 0 (
    echo [OK] Database 'cedos_db' created
) else (
    echo [INFO] Database 'cedos_db' may already exist
)

REM Create user
psql -U postgres -c "CREATE USER cedos_user WITH PASSWORD 'cedos_pass';" 2>nul
if %errorlevel% equ 0 (
    echo [OK] User 'cedos_user' created
) else (
    echo [INFO] User 'cedos_user' may already exist
)

REM Grant privileges
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE cedos_db TO cedos_user;" 2>nul
if %errorlevel% equ 0 (
    echo [OK] Privileges granted
)

REM Create .env file
cd /d "%~dp0backend"
if exist ".env" (
    echo.
    echo [INFO] .env file already exists
    echo.
    choice /C YN /M "Do you want to update it with local PostgreSQL settings"
    if errorlevel 2 goto :skip_env
)

(
echo DATABASE_URL=postgresql://cedos_user:cedos_pass@localhost:5432/cedos_db
echo SECRET_KEY=cedos-secret-key-change-in-production-12345
echo BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
) > .env

echo [OK] .env file created/updated!

:skip_env
echo.
echo ============================================================
echo   Step 4: pgAdmin Configuration Guide
echo ============================================================
echo.

REM Create configuration guide file
(
echo ============================================================
echo   pgAdmin Configuration Guide
echo ============================================================
echo.
echo pgAdmin is 100%% FREE and Open Source!
echo.
echo ============================================================
echo   Connect to PostgreSQL in pgAdmin
echo ============================================================
echo.
echo 1. Launch pgAdmin (from Start Menu or Desktop)
echo.
echo 2. When pgAdmin opens, you'll see "Servers" in left sidebar
echo.
echo 3. Right-click "Servers" ^> "Create" ^> "Server"
echo.
echo 4. General Tab:
echo    - Name: CEDOS Local
echo.
echo 5. Connection Tab:
echo    - Host name/address: localhost
echo    - Port: 5432
echo    - Maintenance database: postgres
echo    - Username: postgres
echo    - Password: %POSTGRES_PASSWORD%
echo    - [Check] Save password
echo.
echo 6. Click "Save"
echo.
echo ============================================================
echo   View Your Database
echo ============================================================
echo.
echo 1. Expand "CEDOS Local" ^> "Databases"
echo.
echo 2. You should see "cedos_db" database
echo.
echo 3. Expand "cedos_db" ^> "Schemas" ^> "public" ^> "Tables"
echo    - Tables will appear after running migrations
echo.
echo ============================================================
echo   Run SQL Queries
echo ============================================================
echo.
echo 1. Right-click "cedos_db" ^> "Query Tool"
echo.
echo 2. Write SQL queries in the editor
echo.
echo 3. Click "Execute" (F5) to run queries
echo.
echo ============================================================
echo   View/Edit Data
echo ============================================================
echo.
echo 1. Right-click any table ^> "View/Edit Data" ^> "All Rows"
echo.
echo 2. You can view and edit data in a spreadsheet-like interface
echo.
echo ============================================================
echo   Database Connection Info
echo ============================================================
echo.
echo Database: cedos_db
echo User: cedos_user
echo Password: cedos_pass
echo Host: localhost
echo Port: 5432
echo.
echo ============================================================
echo   Next Steps
echo ============================================================
echo.
echo 1. Run database migrations:
echo    cd backend
echo    alembic upgrade head
echo.
echo 2. Start the server:
echo    uvicorn app.main:app --reload
echo.
echo 3. Access API:
echo    http://localhost:8000/api/docs
echo.
echo ============================================================
) > PGADMIN_CONFIG_GUIDE.txt

echo [OK] Configuration guide created: PGADMIN_CONFIG_GUIDE.txt
echo.

echo ============================================================
echo   Setup Complete!
echo ============================================================
echo.
echo pgAdmin is installed and configured!
echo.
echo Database Info:
echo   Database: cedos_db
echo   User: cedos_user
echo   Password: cedos_pass
echo   Host: localhost
echo   Port: 5432
echo.
echo Next Steps:
echo   1. Launch pgAdmin from Start Menu
echo   2. Connect using the settings above
echo   3. See PGADMIN_CONFIG_GUIDE.txt for detailed instructions
echo.
echo ============================================================
echo   Launch pgAdmin?
echo ============================================================
echo.
choice /C YN /M "Do you want to launch pgAdmin now"

if errorlevel 2 goto :end

echo.
echo Launching pgAdmin...
start pgAdmin4

:end
echo.
echo Opening configuration guide...
start notepad PGADMIN_CONFIG_GUIDE.txt

echo.
echo Done! pgAdmin is ready to use!
echo.
pause
