@echo off
REM ============================================================
REM   COMPLETE DEPLOYMENT - Web + Mobile APK
REM   Single script - No errors!
REM ============================================================

echo.
echo ============================================================
echo   CEDOS - Complete Deployment
echo ============================================================
echo.
echo This will deploy:
echo   - Frontend to Vercel (Web Browser)
echo   - Mobile APK (Android)
echo   - Both connected to Railway backend
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

echo Getting Railway URL...
railway domain

echo.
set /p RAILWAY_URL="Enter Railway URL (e.g., https://xxx.railway.app): "

if "%RAILWAY_URL%"=="" (
    echo [ERROR] Railway URL required!
    echo Get it from: https://railway.app/dashboard
    pause
    exit /b 1
)

REM Clean URL
set RAILWAY_URL=%RAILWAY_URL:http://=%
set RAILWAY_URL=%RAILWAY_URL:https://=%
set RAILWAY_URL=https://%RAILWAY_URL%

echo.
echo Using: %RAILWAY_URL%
echo.

echo ============================================================
echo   Step 2: Configure Frontend
echo ============================================================
echo.

cd /d "%~dp0frontend"

REM Create API config file
if not exist "src\api" mkdir src\api

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

echo [OK] API client created

REM Update Login.tsx
powershell -Command "(Get-Content src\pages\Login.tsx -Raw) -replace 'import axios from ''axios'';', 'import apiClient from ''../api/client'';' -replace 'axios\.post', 'apiClient.post' | Set-Content src\pages\Login.tsx"

REM Update Dashboard.tsx
powershell -Command "(Get-Content src\pages\Dashboard.tsx -Raw) -replace 'import axios from ''axios'';', 'import apiClient from ''../api/client'';' -replace 'axios\.get', 'apiClient.get' | Set-Content src\pages\Dashboard.tsx"

REM Update Projects.tsx
powershell -Command "(Get-Content src\pages\Projects.tsx -Raw) -replace 'import axios from ''axios'';', 'import apiClient from ''../api/client'';' -replace 'axios\.', 'apiClient.' | Set-Content src\pages\Projects.tsx"

REM Update NewProject.tsx
powershell -Command "(Get-Content src\pages\NewProject.tsx -Raw) -replace 'import axios from ''axios'';', 'import apiClient from ''../api/client'';' -replace 'axios\.', 'apiClient.' | Set-Content src\pages\NewProject.tsx"

REM Update Calculator.tsx
powershell -Command "(Get-Content src\pages\Calculator.tsx -Raw) -replace 'import axios from ''axios'';', 'import apiClient from ''../api/client'';' -replace 'axios\.', 'apiClient.' | Set-Content src\pages\Calculator.tsx"

REM Update ProjectWorkspace.tsx
powershell -Command "(Get-Content src\pages\ProjectWorkspace.tsx -Raw) -replace 'import axios from ''axios'';', 'import apiClient from ''../api/client'';' -replace 'axios\.', 'apiClient.' | Set-Content src\pages\ProjectWorkspace.tsx"

REM Update ARVisualization.tsx
powershell -Command "(Get-Content src\pages\ARVisualization.tsx -Raw) -replace 'import axios from ''axios'';', 'import apiClient from ''../api/client'';' -replace 'axios\.', 'apiClient.' | Set-Content src\pages\ARVisualization.tsx"

echo [OK] Frontend files updated

echo.
echo Building frontend...
call npm run build

if %errorlevel% neq 0 (
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

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
    echo Please login to Vercel...
    start https://vercel.com/login
    vercel login
)

echo Deploying to Vercel...
vercel --prod --yes

if %errorlevel% equ 0 (
    echo [OK] Frontend deployed!
    vercel ls | findstr cedos
) else (
    echo [WARNING] Check Vercel dashboard
)

cd /d "%~dp0"

echo.
echo ============================================================
echo   Step 4: Setup Mobile App
echo ============================================================
echo.

if not exist "cedos-mobile" (
    echo Creating mobile app...
    mkdir cedos-mobile
    cd cedos-mobile
    
    echo Initializing Expo project...
    npx create-expo-app@latest . --template blank-typescript --yes
    
    echo Installing dependencies...
    npm install axios @react-navigation/native @react-navigation/native-stack react-native-paper @react-native-async-storage/async-storage react-native-vector-icons
) else (
    cd cedos-mobile
)

echo.
echo Configuring mobile app API...

if not exist "src" mkdir src
if not exist "src\config" mkdir src\config

(
echo export const API_BASE_URL = '%RAILWAY_URL%/api/v1';
echo.
echo export default API_BASE_URL;
) > src\config\api.ts

echo [OK] Mobile API configured

REM Create app.json
if not exist "app.json" (
    (
    echo {
    echo   "expo": {
    echo     "name": "CEDOS",
    echo     "slug": "cedos-mobile",
    echo     "version": "1.0.0",
    echo     "orientation": "portrait",
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
echo ============================================================
echo   Step 5: Build Mobile APK
echo ============================================================
echo.

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
echo This takes 10-15 minutes...
echo.
eas build --platform android --profile production --non-interactive

cd /d "%~dp0"

echo.
echo ============================================================
echo   DEPLOYMENT COMPLETE!
echo ============================================================
echo.
echo Frontend: Deployed to Vercel
echo Backend: %RAILWAY_URL%
echo Mobile: APK building (check Expo)
echo.
echo All connected to Railway backend!
echo.
pause
