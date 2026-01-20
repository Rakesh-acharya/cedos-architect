# ============================================================
#   DEPLOY EVERYTHING - Web + Mobile APK
#   PowerShell version - Complete solution!
# ============================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  CEDOS - Complete Deployment" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Deploying:" -ForegroundColor Cyan
Write-Host "  - Frontend (Web Browser) to Vercel" -ForegroundColor White
Write-Host "  - Mobile APK (Android) via Expo" -ForegroundColor White
Write-Host "  - Both connected to Railway backend" -ForegroundColor White
Write-Host ""
Read-Host "Press Enter to continue"

# Step 1: Get Railway URL
Write-Host ""
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host "  Step 1: Get Railway Backend URL" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host ""

Set-Location "backend"

if (-not (Get-Command railway -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Railway CLI..." -ForegroundColor Cyan
    npm install -g @railway/cli
}

$railwayCheck = railway whoami 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Please login to Railway..." -ForegroundColor Yellow
    railway login
}

Write-Host "Getting Railway URL..." -ForegroundColor Cyan
railway domain

Write-Host ""
$RAILWAY_URL = Read-Host "Enter Railway URL (from above)"

if ([string]::IsNullOrWhiteSpace($RAILWAY_URL)) {
    Write-Host "[ERROR] Railway URL required!" -ForegroundColor Red
    Write-Host "Get it from: https://railway.app/dashboard" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

$RAILWAY_URL = $RAILWAY_URL -replace "http://", "" -replace "https://", ""
$RAILWAY_URL = "https://$RAILWAY_URL"

Write-Host ""
Write-Host "Using: $RAILWAY_URL" -ForegroundColor Green
Write-Host ""

# Step 2: Update Frontend
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host "  Step 2: Configure Frontend" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host ""

Set-Location "..\frontend"

# Create API client
if (-not (Test-Path "src\api")) {
    New-Item -ItemType Directory -Path "src\api" | Out-Null
}

$apiClientContent = @"
import axios from 'axios';

const API_BASE_URL = '$RAILWAY_URL';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
});

apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
  }
);

export default apiClient;
"@

Set-Content -Path "src\api\client.ts" -Value $apiClientContent

Write-Host "[OK] Frontend configured" -ForegroundColor Green

Write-Host "Building..." -ForegroundColor Cyan
npm run build

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Build failed!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host "  Step 3: Deploy Frontend to Vercel" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host ""

if (-not (Get-Command vercel -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Vercel CLI..." -ForegroundColor Cyan
    npm install -g vercel
}

$vercelCheck = vercel whoami 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Please login to Vercel..." -ForegroundColor Yellow
    Start-Process "https://vercel.com/login"
    vercel login
}

Write-Host "Deploying to Vercel..." -ForegroundColor Cyan
vercel --prod --yes

Set-Location ".."

# Step 4: Mobile App
Write-Host ""
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host "  Step 4: Setup Mobile App" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host ""

if (-not (Test-Path "cedos-mobile")) {
    Write-Host "Creating mobile app..." -ForegroundColor Cyan
    New-Item -ItemType Directory -Path "cedos-mobile" | Out-Null
    Set-Location "cedos-mobile"
    
    Write-Host "Initializing Expo project..." -ForegroundColor Cyan
    npx create-expo-app@latest . --template blank-typescript --yes
    
    Write-Host "Installing dependencies..." -ForegroundColor Cyan
    npm install axios @react-navigation/native @react-navigation/native-stack react-native-paper @react-native-async-storage/async-storage
} else {
    Set-Location "cedos-mobile"
}

if (-not (Test-Path "src\config")) {
    New-Item -ItemType Directory -Path "src\config" | Out-Null
}

$mobileApiConfig = "export const API_BASE_URL = '$RAILWAY_URL/api/v1';"
Set-Content -Path "src\config\api.ts" -Value $mobileApiConfig

if (-not (Test-Path "app.json")) {
    $appJson = @{
        expo = @{
            name = "CEDOS"
            slug = "cedos-mobile"
            version = "1.0.0"
            android = @{
                package = "com.cedos.app"
            }
        }
    }
    $appJson | ConvertTo-Json -Depth 10 | Set-Content -Path "app.json"
}

if (-not (Test-Path "eas.json")) {
    $easJson = @{
        build = @{
            production = @{
                android = @{
                    buildType = "apk"
                }
            }
        }
    }
    $easJson | ConvertTo-Json -Depth 10 | Set-Content -Path "eas.json"
}

Write-Host "[OK] Mobile configured" -ForegroundColor Green

Write-Host ""
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host "  Step 5: Build APK" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host ""

if (-not (Get-Command eas -ErrorAction SilentlyContinue)) {
    Write-Host "Installing EAS CLI..." -ForegroundColor Cyan
    npm install -g eas-cli
}

$easCheck = eas whoami 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Please login to Expo..." -ForegroundColor Yellow
    Start-Process "https://expo.dev/login"
    eas login
}

Write-Host "Building APK (10-15 minutes)..." -ForegroundColor Cyan
eas build --platform android --profile production --non-interactive

Set-Location ".."

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  COMPLETE!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Frontend: Deployed to Vercel" -ForegroundColor Cyan
Write-Host "Backend: $RAILWAY_URL" -ForegroundColor Cyan
Write-Host "Mobile: APK building" -ForegroundColor Cyan
Write-Host ""
Write-Host "All connected to Railway backend!" -ForegroundColor Green
Write-Host ""
Read-Host "Press Enter to exit"
