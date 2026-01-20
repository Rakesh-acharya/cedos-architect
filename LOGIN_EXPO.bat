@echo off
REM Quick Expo Login Helper

echo.
echo ============================================================
echo   Expo Login Helper
echo ============================================================
echo.
echo This will help you login to Expo.
echo.
echo When prompted, enter:
echo   Email: rakeshacherya123@gmail.com
echo   Password: Rakesh@123#$
echo.
pause

eas login

if %errorlevel% equ 0 (
    echo.
    echo [OK] Login successful!
    echo.
    echo Now run: .\BUILD_APK.ps1
    echo.
) else (
    echo.
    echo [ERROR] Login failed!
    echo.
)

pause
