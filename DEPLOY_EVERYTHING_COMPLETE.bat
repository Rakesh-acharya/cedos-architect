@echo off
REM ============================================================
REM   COMPLETE DEPLOYMENT - Web + Mobile APK
REM   Single script to deploy everything!
REM ============================================================

echo.
echo ============================================================
echo   CEDOS - Complete Deployment
echo ============================================================
echo.
echo This will deploy:
echo   1. Frontend to Vercel (Web - Browser)
echo   2. Mobile APK (Android - Connected to Railway backend)
echo.
echo Both will connect to your Railway backend!
echo.
pause

REM Get Railway URL
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
    echo Please login to Railway...
    railway login
)

echo.
echo Getting Railway URL...
railway domain

echo.
set /p RAILWAY_URL="Enter your Railway URL (from above): "

if "%RAILWAY_URL%"=="" (
    echo.
    echo [ERROR] Railway URL required!
    echo.
    echo Get it from Railway dashboard:
    echo   https://railway.app/dashboard
    echo   Your service - Settings - Domains
    echo.
    pause
    exit /b 1
)

REM Remove http:// or https:// if present, then add https://
set RAILWAY_URL=%RAILWAY_URL:http://=%
set RAILWAY_URL=%RAILWAY_URL:https://=%
set RAILWAY_URL=https://%RAILWAY_URL%

echo.
echo Using Railway URL: %RAILWAY_URL%
echo.

echo ============================================================
echo   Step 2: Configure Frontend for Railway
echo ============================================================
echo.

cd /d "%~dp0frontend"

echo Creating API configuration file...

REM Create axios config with Railway URL
(
echo import axios from 'axios';
echo.
echo const API_BASE_URL = '%RAILWAY_URL%';
echo.
echo const apiClient = axios.create({
echo   baseURL: API_BASE_URL,
echo   headers: {
echo     'Content-Type': 'application/json',
echo   },
echo });
echo.
echo // Add token to requests
echo apiClient.interceptors.request.use(
echo   \(config\) =^> {
echo     const token = localStorage.getItem\('token'\);
echo     if \(token\) {
echo       config.headers.Authorization = `Bearer ${token}`;
echo     }
echo     return config;
echo   },
echo   \(error\) =^> Promise.reject\(error\)
echo );
echo.
echo export default apiClient;
) > src\api\client.ts

REM Create api directory if it doesn't exist
if not exist "src\api" mkdir src\api

echo [OK] Frontend API client created

echo.
echo Updating vite config for production...
(
echo import { defineConfig } from 'vite'
echo import react from '@vitejs/plugin-react'
echo.
echo export default defineConfig({
echo   plugins: [react()],
echo   server: {
echo     port: 3000,
echo     proxy: {
echo       '/api': {
echo         target: '%RAILWAY_URL%',
echo         changeOrigin: true,
echo       },
echo     },
echo   },
echo   define: {
echo     'import.meta.env.VITE_API_URL': JSON.stringify('%RAILWAY_URL%'),
echo   },
echo })
) > vite.config.ts

echo [OK] Vite config updated

echo.
echo ============================================================
echo   Step 3: Deploy Frontend to Vercel
echo ============================================================
echo.

where vercel >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Vercel CLI...
    npm install -g vercel
)

vercel whoami >nul 2>&1
if %errorlevel% neq 0 (
    echo Please login to Vercel...
    start https://vercel.com/login
    vercel login
)

echo.
echo Building frontend...
call npm run build

if %errorlevel% neq 0 (
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

echo.
echo Deploying to Vercel...
vercel --prod

if %errorlevel% equ 0 (
    echo.
    echo [OK] Frontend deployed to Vercel!
    echo.
    vercel ls | findstr cedos
    echo.
    set /p VERCEL_URL="Enter your Vercel URL (from above): "
) else (
    echo.
    echo [WARNING] Vercel deployment may have failed
    echo Check Vercel dashboard: https://vercel.com/dashboard
    set /p VERCEL_URL="Enter your Vercel URL (if deployed): "
)

cd /d "%~dp0"

echo.
echo ============================================================
echo   Step 4: Setup Mobile App
echo ============================================================
echo.

REM Check if mobile app directory exists
if not exist "cedos-mobile" (
    echo Creating mobile app directory...
    mkdir cedos-mobile
    cd cedos-mobile
    
    echo Initializing React Native Expo project...
    npx create-expo-app@latest . --template blank-typescript --yes
    
    echo.
    echo Installing dependencies...
    npm install axios react-native-paper react-native-vector-icons @react-navigation/native @react-navigation/native-stack @react-native-async-storage/async-storage
) else (
    cd cedos-mobile
)

echo.
echo Creating mobile app API configuration...

REM Create API config for mobile
(
echo export const API_BASE_URL = '%RAILWAY_URL%/api/v1';
echo.
echo export const API_CONFIG = {
echo   baseURL: API_BASE_URL,
echo   timeout: 30000,
echo };
) > src\config\api.ts

if not exist "src\config" mkdir src\config

echo [OK] Mobile API config created

echo.
echo ============================================================
echo   Step 5: Build Mobile APK
echo ============================================================
echo.

echo Installing Expo EAS CLI...
npm install -g eas-cli

echo.
echo Logging in to Expo...
eas whoami >nul 2>&1
if %errorlevel% neq 0 (
    echo Please login to Expo...
    start https://expo.dev/login
    eas login
)

echo.
echo Configuring EAS build...
if not exist "eas.json" (
    (
    echo {
    echo   "build": {
    echo     "production": {
    echo       "android": {
    echo         "buildType": "apk"
    echo       }
    echo     }
    echo   }
    echo }
    ) > eas.json
)

echo.
echo Starting APK build...
echo This may take 10-15 minutes...
echo.
eas build --platform android --profile production --non-interactive

if %errorlevel% equ 0 (
    echo.
    echo [OK] APK build started!
    echo.
    echo Check build status:
    echo   https://expo.dev/accounts/[your-account]/builds
    echo.
    echo Once build completes, download the APK!
) else (
    echo.
    echo [INFO] Build may require manual setup
    echo See BUILD_MOBILE_APK.md for details
)

cd /d "%~dp0"

echo.
echo ============================================================
echo   DEPLOYMENT COMPLETE!
echo ============================================================
echo.
echo Summary:
echo.
echo Frontend (Web):
if not "%VERCEL_URL%"=="" (
    echo   URL: %VERCEL_URL%
    echo   Status: Deployed
) else (
    echo   Status: Check Vercel dashboard
)
echo.
echo Backend (API):
echo   URL: %RAILWAY_URL%
echo   Status: Live
echo.
echo Mobile APK:
echo   Status: Building (check Expo dashboard)
echo   Download: https://expo.dev/accounts/[your-account]/builds
echo.
echo ============================================================
echo   Access Your App
echo ============================================================
echo.
if not "%VERCEL_URL%"=="" (
    echo Web App: %VERCEL_URL%
)
echo API Docs: %RAILWAY_URL%/api/docs
echo.
echo ============================================================
echo.

pause
