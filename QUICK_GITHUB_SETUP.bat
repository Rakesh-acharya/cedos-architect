@echo off
REM Quick GitHub Setup - Minimal Steps

echo ============================================================
echo   Quick GitHub Setup
echo ============================================================
echo.

cd /d "%~dp0"

echo Step 1: Setting Git user info...
echo.
set /p GIT_NAME="Enter your name (for Git commits): "
if "%GIT_NAME%"=="" set GIT_NAME="CEDOS Developer"

set /p GIT_EMAIL="Enter your email (for Git commits): "
if "%GIT_EMAIL%"=="" set GIT_EMAIL="cedos@example.com"

git config user.name "%GIT_NAME%"
git config user.email "%GIT_EMAIL%"

echo.
echo Step 2: Creating commit...
git add .
git commit -m "Initial commit: CEDOS - Civil Engineering Digital Operating System"

echo.
echo Step 3: Create GitHub repository...
echo.
echo Please:
echo 1. Go to: https://github.com/new
echo 2. Repository name: cedos-architect
echo 3. DO NOT initialize with README
echo 4. Click "Create repository"
echo 5. Copy the repository URL
echo.
pause

echo.
echo Step 4: Enter your GitHub repository URL:
echo Example: https://github.com/yourusername/cedos-architect.git
set /p REPO_URL="Repository URL: "

if "%REPO_URL%"=="" (
    echo [ERROR] URL required!
    pause
    exit /b 1
)

echo.
echo Step 5: Adding remote and pushing...
git remote add origin "%REPO_URL%" 2>nul
if %errorlevel% neq 0 git remote set-url origin "%REPO_URL%"

git branch -M main
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ============================================================
    echo   SUCCESS! Project is on GitHub!
    echo ============================================================
    echo.
    echo Repository: %REPO_URL%
    echo.
    echo Next: Deploy to Railway using DEPLOY_WEB_COMPLETE.md
    echo.
) else (
    echo.
    echo [ERROR] Push failed!
    echo.
    echo Try GitHub CLI:
    echo   gh auth login
    echo   git push -u origin main
    echo.
)

pause
