@echo off
REM ============================================================
REM   Deploy Web + Build Mobile APK - Complete Solution
REM ============================================================

echo.
echo ============================================================
echo   CEDOS - Deploy Web + Mobile APK
echo ============================================================
echo.
echo This will:
echo   1. Deploy frontend to Vercel (Web browser)
echo   2. Build mobile APK (Android)
echo   3. Both connected to Railway backend
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
    railway login
)

echo Getting Railway URL...
railway domain

echo.
set /p RAILWAY_URL="Enter Railway URL (from above, e.g., https://xxx.railway.app): "

if "%RAILWAY_URL%"=="" (
    echo [ERROR] Railway URL required!
    echo Get it from: https://railway.app/dashboard
    pause
    exit /b 1
)

REM Ensure https://
set RAILWAY_URL=%RAILWAY_URL:http://=%
set RAILWAY_URL=%RAILWAY_URL:https://=%
set RAILWAY_URL=https://%RAILWAY_URL%

echo.
echo Using: %RAILWAY_URL%
echo.

echo ============================================================
echo   Step 2: Deploy Frontend to Vercel
echo ============================================================
echo.

cd /d "%~dp0frontend"

REM Create API config
if not exist "src\api" mkdir src\api

(
echo import axios from 'axios';
echo.
echo const API_BASE_URL = '%RAILWAY_URL%';
echo.
echo const apiClient = axios.create({
echo   baseURL: API_BASE_URL,
echo });
echo.
echo apiClient.interceptors.request.use(
echo   \(config\) =^> {
echo     const token = localStorage.getItem\('token'\);
echo     if \(token\) {
echo       config.headers.Authorization = `Bearer ${token}`;
echo     }
echo     return config;
echo   }
echo );
echo.
echo export default apiClient;
) > src\api\client.ts

echo [OK] Frontend API configured

REM Update all axios calls to use apiClient
echo.
echo Updating frontend files to use API client...
powershell -Command "(Get-Content src\pages\Login.tsx) -replace 'import axios from ''axios'';', 'import apiClient from ''../api/client'';' -replace 'axios\.', 'apiClient.' | Set-Content src\pages\Login.tsx"
powershell -Command "(Get-Content src\pages\Dashboard.tsx) -replace 'import axios from ''axios'';', 'import apiClient from ''../api/client'';' -replace 'axios\.', 'apiClient.' | Set-Content src\pages\Dashboard.tsx"
powershell -Command "(Get-Content src\pages\Projects.tsx) -replace 'import axios from ''axios'';', 'import apiClient from ''../api/client'';' -replace 'axios\.', 'apiClient.' | Set-Content src\pages\Projects.tsx"
powershell -Command "(Get-Content src\pages\NewProject.tsx) -replace 'import axios from ''axios'';', 'import apiClient from ''../api/client'';' -replace 'axios\.', 'apiClient.' | Set-Content src\pages\NewProject.tsx"
powershell -Command "(Get-Content src\pages\Calculator.tsx) -replace 'import axios from ''axios'';', 'import apiClient from ''../api/client'';' -replace 'axios\.', 'apiClient.' | Set-Content src\pages\Calculator.tsx"
powershell -Command "(Get-Content src\pages\ProjectWorkspace.tsx) -replace 'import axios from ''axios'';', 'import apiClient from ''../api/client'';' -replace 'axios\.', 'apiClient.' | Set-Content src\pages\ProjectWorkspace.tsx"
powershell -Command "(Get-Content src\pages\ARVisualization.tsx) -replace 'import axios from ''axios'';', 'import apiClient from ''../api/client'';' -replace 'axios\.', 'apiClient.' | Set-Content src\pages\ARVisualization.tsx"

echo [OK] Frontend files updated

echo.
echo Building frontend...
call npm run build

echo.
echo Deploying to Vercel...
where vercel >nul 2>&1
if %errorlevel% neq 0 (
    npm install -g vercel
)

vercel whoami >nul 2>&1
if %errorlevel% neq 0 (
    vercel login
)

vercel --prod

echo.
echo ============================================================
echo   Step 3: Build Mobile APK
echo ============================================================
echo.

cd /d "%~dp0"

REM Check if mobile app exists
if not exist "cedos-mobile" (
    echo Mobile app directory not found. Creating...
    mkdir cedos-mobile
    cd cedos-mobile
    
    echo Initializing Expo project...
    npx create-expo-app@latest . --template blank-typescript --yes
    
    echo Installing dependencies...
    npm install axios @react-navigation/native @react-navigation/native-stack react-native-paper @react-native-async-storage/async-storage
) else (
    cd cedos-mobile
)

echo.
echo Configuring mobile app for Railway backend...

REM Create API config
if not exist "src\config" mkdir src\config

(
echo export const API_BASE_URL = '%RAILWAY_URL%/api/v1';
echo.
echo export default API_BASE_URL;
) > src\config\api.ts

echo [OK] Mobile API configured

REM Create app.json if not exists
if not exist "app.json" (
    (
    echo {
    echo   "expo": {
    echo     "name": "CEDOS",
    echo     "slug": "cedos-mobile",
    echo     "version": "1.0.0",
    echo     "orientation": "portrait",
    echo     "icon": "./assets/icon.png",
    echo     "splash": {
    echo       "image": "./assets/splash.png",
    echo       "resizeMode": "contain",
    echo       "backgroundColor": "#1976d2"
    echo     },
    echo     "android": {
    echo       "package": "com.cedos.app",
    echo       "adaptiveIcon": {
    echo         "foregroundImage": "./assets/adaptive-icon.png",
    echo         "backgroundColor": "#1976d2"
    echo       }
    echo     }
    echo   }
    echo }
    ) > app.json
)

echo.
echo Building APK with EAS...
npm install -g eas-cli

eas whoami >nul 2>&1
if %errorlevel% neq 0 (
    echo Please login to Expo...
    start https://expo.dev/login
    eas login
)

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
echo This will take 10-15 minutes...
echo.
eas build --platform android --profile production

cd /d "%~dp0"

echo.
echo ============================================================
echo   DEPLOYMENT COMPLETE!
echo ============================================================
echo.
echo Frontend: Deployed to Vercel
echo Backend: %RAILWAY_URL%
echo Mobile: APK building (check Expo dashboard)
echo.
echo All connected to same Railway backend!
echo.
pause
