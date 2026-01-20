@echo off
REM ============================================================
REM   DEPLOY EVERYTHING - Web + Mobile APK
REM   Single script - Complete solution!
REM ============================================================

echo.
echo ============================================================
echo   CEDOS - Complete Deployment
echo ============================================================
echo.
echo Deploying:
echo   - Frontend (Web Browser) to Vercel
echo   - Mobile APK (Android) via Expo
echo   - Both connected to Railway backend
echo.
pause

REM Step 1: Get Railway URL
echo.
echo ============================================================
echo   Step 1: Get Railway Backend URL
echo ============================================================
echo.

cd /d "%~dp0backend"

where railway >nul 2>&1
if %errorlevel% neq 0 (
    npm install -g @railway/cli
)

railway whoami >nul 2>&1
if %errorlevel% neq 0 (
    railway login
)

echo Getting Railway URL...
railway domain

echo.
set /p RAILWAY_URL="Enter Railway URL (from above): "

if "%RAILWAY_URL%"=="" (
    echo [ERROR] Railway URL required!
    pause
    exit /b 1
)

set RAILWAY_URL=%RAILWAY_URL:http://=%
set RAILWAY_URL=%RAILWAY_URL:https://=%
set RAILWAY_URL=https://%RAILWAY_URL%

echo.
echo Using: %RAILWAY_URL%
echo.

REM Step 2: Update Frontend
echo ============================================================
echo   Step 2: Configure Frontend
echo ============================================================
echo.

cd /d "%~dp0frontend"

REM Update API client
(
echo import axios from 'axios';
echo.
echo const API_BASE_URL = '%RAILWAY_URL%';
echo.
echo const apiClient = axios.create({
echo   baseURL: API_BASE_URL,
echo   headers: { 'Content-Type': 'application/json' },
echo });
echo.
echo apiClient.interceptors.request.use(
echo   \(config\) =^> {
echo     const token = localStorage.getItem\('token'\);
echo     if \(token\) config.headers.Authorization = `Bearer ${token}`;
echo     return config;
echo   }
echo );
echo.
echo export default apiClient;
) > src\api\client.ts

echo [OK] Frontend configured

echo Building...
call npm run build

echo.
echo ============================================================
echo   Step 3: Deploy Frontend to Vercel
echo ============================================================
echo.

where vercel >nul 2>&1
if %errorlevel% neq 0 (
    npm install -g vercel
)

vercel whoami >nul 2>&1
if %errorlevel% neq 0 (
    start https://vercel.com/login
    vercel login
)

vercel --prod --yes

cd /d "%~dp0"

REM Step 4: Mobile App
echo.
echo ============================================================
echo   Step 4: Setup Mobile App
echo ============================================================
echo.

if not exist "cedos-mobile" (
    mkdir cedos-mobile
    cd cedos-mobile
    npx create-expo-app@latest . --template blank-typescript --yes
    npm install axios @react-navigation/native @react-navigation/native-stack react-native-paper @react-native-async-storage/async-storage
) else (
    cd cedos-mobile
)

if not exist "src\config" mkdir src\config

(
echo export const API_BASE_URL = '%RAILWAY_URL%/api/v1';
) > src\config\api.ts

if not exist "app.json" (
    (
    echo {"expo":{"name":"CEDOS","slug":"cedos-mobile","version":"1.0.0","android":{"package":"com.cedos.app"}}}
    ) > app.json
)

if not exist "eas.json" (
    (
    echo {"build":{"production":{"android":{"buildType":"apk"}}}}
    ) > eas.json
)

echo [OK] Mobile configured

echo.
echo ============================================================
echo   Step 5: Build APK
echo ============================================================
echo.

npm install -g eas-cli

eas whoami >nul 2>&1
if %errorlevel% neq 0 (
    start https://expo.dev/login
    eas login
)

echo Building APK (10-15 minutes)...
eas build --platform android --profile production --non-interactive

cd /d "%~dp0"

echo.
echo ============================================================
echo   COMPLETE!
echo ============================================================
echo.
echo Frontend: Deployed to Vercel
echo Backend: %RAILWAY_URL%
echo Mobile: APK building
echo.
echo All connected to Railway backend!
echo.
pause
