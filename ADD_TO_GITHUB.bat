@echo off
REM Complete GitHub Setup Script
REM This will initialize git, create repo, and push to GitHub

echo ============================================================
echo   Adding CEDOS Project to GitHub
echo ============================================================
echo.

cd /d "%~dp0"

echo Step 1: Checking Git installation...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git is not installed!
    echo Please install Git from: https://git-scm.com/downloads
    pause
    exit /b 1
)

echo [OK] Git is installed
echo.

echo Step 2: Initializing Git repository...
if exist .git (
    echo [INFO] Git repository already exists
) else (
    git init
    echo [OK] Git repository initialized
)

echo.
echo Step 3: Configuring Git...
git config user.name >nul 2>&1
if %errorlevel% neq 0 (
    echo Please enter your Git username (for commits):
    set /p GIT_USERNAME="Username: "
    if "%GIT_USERNAME%"=="" set GIT_USERNAME="CEDOS Developer"
    git config user.name "%GIT_USERNAME%"
    echo [OK] Git username set
) else (
    echo [OK] Git username already configured
)

git config user.email >nul 2>&1
if %errorlevel% neq 0 (
    echo Please enter your Git email (for commits):
    set /p GIT_EMAIL="Email: "
    if "%GIT_EMAIL%"=="" (
        echo [WARN] No email provided, using default
        git config user.email "cedos@example.com"
    ) else (
        git config user.email "%GIT_EMAIL%"
    )
    echo [OK] Git email set
) else (
    echo [OK] Git email already configured
)

echo.
echo Step 4: Adding all files...
git add .
if %errorlevel% neq 0 (
    echo [ERROR] Failed to add files
    pause
    exit /b 1
)

echo [OK] Files added
echo.

echo Step 5: Creating initial commit...
git commit -m "Initial commit: CEDOS - Civil Engineering Digital Operating System"
if %errorlevel% neq 0 (
    echo [WARN] Commit failed - might be no changes or already committed
)

echo.
echo Step 6: Creating GitHub repository...
echo.
echo Please choose one:
echo.
echo Option A: Create repo via GitHub website (Recommended)
echo   1. Go to: https://github.com/new
echo   2. Repository name: cedos-architect (or any name)
echo   3. Description: CEDOS - Civil Engineering Digital Operating System
echo   4. Choose: Public or Private
echo   5. DO NOT initialize with README (we already have one)
echo   6. Click "Create repository"
echo   7. Copy the repository URL
echo.
echo Option B: Use GitHub CLI (if installed)
echo   Run: gh repo create cedos-architect --public --source=. --remote=origin --push
echo.
pause

echo.
echo Step 7: Adding remote repository...
echo.
echo Please enter your GitHub repository URL:
echo Example: https://github.com/yourusername/cedos-architect.git
set /p REPO_URL="Repository URL: "

if "%REPO_URL%"=="" (
    echo [ERROR] Repository URL is required!
    echo.
    echo Please:
    echo 1. Create repository on GitHub: https://github.com/new
    echo 2. Copy the repository URL
    echo 3. Run this script again and paste the URL
    pause
    exit /b 1
)

git remote add origin "%REPO_URL%" 2>nul
if %errorlevel% neq 0 (
    git remote set-url origin "%REPO_URL%"
    echo [INFO] Remote updated
) else (
    echo [OK] Remote added
)

echo.
echo Step 8: Pushing to GitHub...
echo This will upload all your files to GitHub...
echo.
git branch -M main
git push -u origin main

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Push failed!
    echo.
    echo Common issues:
    echo 1. Authentication required - GitHub may ask for credentials
    echo 2. Use GitHub CLI: gh auth login
    echo 3. Or use Personal Access Token
    echo.
    echo Try again with:
    echo   git push -u origin main
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   SUCCESS! Project is now on GitHub!
echo ============================================================
echo.
echo Your repository: %REPO_URL%
echo.
echo Next steps:
echo 1. Go to Railway: https://railway.app/new
echo 2. Add GitHub Repo
echo 3. Select this repository
echo 4. Select 'backend' folder
echo 5. Deploy!
echo.
pause
