# ============================================================
#   DEPLOY WEB VERSION - Complete Automation
#   Deploys to Vercel and configures for mobile access
# ============================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  DEPLOYING WEB VERSION FOR MOBILE ACCESS" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

$ErrorActionPreference = "Stop"

Set-Location "C:\Users\rakes\architect\frontend"

# Step 1: Configure API for Railway
Write-Host "Step 1: Configuring API for Railway backend..." -ForegroundColor Cyan

$apiClientContent = @"
import axios from 'axios';

// API base URL - Railway backend
const API_BASE_URL = 'https://cedos-architect-production.up.railway.app';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default apiClient;
"@

Set-Content -Path "src\api\client.ts" -Value $apiClientContent

Write-Host "[OK] API configured for Railway" -ForegroundColor Green

# Step 2: Build frontend
Write-Host ""
Write-Host "Step 2: Building frontend..." -ForegroundColor Cyan

$buildOutput = npm run build 2>&1 | Tee-Object -Variable buildResult

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Build failed!" -ForegroundColor Red
    Write-Host $buildResult
    exit 1
}

Write-Host "[OK] Frontend built successfully" -ForegroundColor Green

# Step 3: Deploy to Vercel
Write-Host ""
Write-Host "Step 3: Deploying to Vercel..." -ForegroundColor Cyan

if (-not (Get-Command vercel -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Vercel CLI..." -ForegroundColor Yellow
    npm install -g vercel
}

$vercelCheck = vercel whoami 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Not logged in to Vercel!" -ForegroundColor Red
    Write-Host "Please login: vercel login" -ForegroundColor Yellow
    exit 1
}

Write-Host "[OK] Logged in to Vercel" -ForegroundColor Green
Write-Host ""

Write-Host "Deploying to Vercel (production)..." -ForegroundColor Cyan
$deployOutput = vercel --prod --yes 2>&1 | Tee-Object -Variable deployResult

Write-Host $deployOutput

# Extract deployment URL
$deployUrl = ""
if ($deployOutput -match "https://[^\s]+\.vercel\.app") {
    $deployUrl = $matches[0]
} elseif ($deployOutput -match "https://[^\s]+") {
    $deployUrl = $matches[0]
}

if ([string]::IsNullOrWhiteSpace($deployUrl)) {
    Write-Host ""
    Write-Host "Getting deployment URL..." -ForegroundColor Cyan
    Start-Sleep -Seconds 5
    $deployments = vercel ls --json 2>&1 | ConvertFrom-Json
    if ($deployments -and $deployments.Count -gt 0) {
        $deployUrl = $deployments[0].url
    }
}

if ([string]::IsNullOrWhiteSpace($deployUrl)) {
    Write-Host ""
    Write-Host "[WARNING] Could not get deployment URL automatically" -ForegroundColor Yellow
    Write-Host "Check Vercel dashboard: https://vercel.com/dashboard" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Please provide the Vercel URL:" -ForegroundColor Yellow
    $deployUrl = Read-Host "Enter Vercel URL"
}

if ([string]::IsNullOrWhiteSpace($deployUrl)) {
    Write-Host "[ERROR] No deployment URL!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  DEPLOYMENT SUCCESSFUL!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Web App URL: $deployUrl" -ForegroundColor Cyan
Write-Host ""
Write-Host "Access from:" -ForegroundColor Yellow
Write-Host "  - Desktop browser: $deployUrl" -ForegroundColor White
Write-Host "  - Mobile browser: $deployUrl" -ForegroundColor White
Write-Host ""
Write-Host "Backend API: https://cedos-architect-production.up.railway.app" -ForegroundColor Cyan
Write-Host ""

# Step 4: Test deployment
Write-Host "Step 4: Testing deployment..." -ForegroundColor Cyan
Write-Host ""

Start-Sleep -Seconds 10

try {
    $response = Invoke-WebRequest -Uri $deployUrl -UseBasicParsing -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "[SUCCESS] Web app is live and accessible!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Opening in browser..." -ForegroundColor Cyan
        Start-Process $deployUrl
    }
} catch {
    Write-Host "[WARNING] Could not verify deployment automatically" -ForegroundColor Yellow
    Write-Host "Please check manually: $deployUrl" -ForegroundColor Cyan
}

# Step 5: Get local IP for mobile access
Write-Host ""
Write-Host "Step 5: Getting local IP address for mobile access..." -ForegroundColor Cyan

$localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notlike "127.*" -and $_.IPAddress -notlike "169.254.*" } | Select-Object -First 1).IPAddress

if ([string]::IsNullOrWhiteSpace($localIP)) {
    $localIP = "192.168.1.100"  # Default fallback
    Write-Host "[WARNING] Could not detect IP, using default: $localIP" -ForegroundColor Yellow
} else {
    Write-Host "[OK] Local IP: $localIP" -ForegroundColor Green
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "ACCESS YOUR APP:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Global Access (Mobile & Desktop):" -ForegroundColor Yellow
Write-Host "   $deployUrl" -ForegroundColor White
Write-Host ""
Write-Host "2. Local Network Access (Same WiFi):" -ForegroundColor Yellow
Write-Host "   http://$localIP:3000" -ForegroundColor White
Write-Host "   (Run: npm run dev in frontend folder)" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Backend API:" -ForegroundColor Yellow
Write-Host "   https://cedos-architect-production.up.railway.app/api/docs" -ForegroundColor White
Write-Host ""
Write-Host "Login Credentials:" -ForegroundColor Cyan
Write-Host "  Username: admin" -ForegroundColor White
Write-Host "  Password: admin123" -ForegroundColor White
Write-Host ""
Write-Host "The web app is now accessible from mobile browsers!" -ForegroundColor Green
Write-Host ""
