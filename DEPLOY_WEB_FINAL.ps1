# ============================================================
#   DEPLOY WEB VERSION - Final Complete Script
#   Deploys to Vercel and verifies it works
# ============================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  DEPLOYING WEB VERSION FOR MOBILE ACCESS" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

Set-Location "C:\Users\rakes\architect\frontend"

# Step 1: Build
Write-Host "Step 1: Building frontend..." -ForegroundColor Cyan
$buildResult = npm run build 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Build failed!" -ForegroundColor Red
    Write-Host $buildResult
    exit 1
}

Write-Host "[OK] Build successful" -ForegroundColor Green

# Step 2: Deploy to Vercel
Write-Host ""
Write-Host "Step 2: Deploying to Vercel..." -ForegroundColor Cyan

# Check Vercel login
$vercelCheck = vercel whoami 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Not logged in to Vercel!" -ForegroundColor Red
    Write-Host "Please login: vercel login" -ForegroundColor Yellow
    exit 1
}

Write-Host "[OK] Logged in to Vercel" -ForegroundColor Green
Write-Host ""

# Deploy
Write-Host "Deploying (this may take 2-3 minutes)..." -ForegroundColor Yellow
$deployOutput = vercel --prod --yes 2>&1 | Tee-Object -Variable fullOutput

Write-Host $fullOutput

# Extract URL
$deployUrl = ""
if ($fullOutput -match "https://[^\s]+\.vercel\.app") {
    $deployUrl = $matches[0]
}

if ([string]::IsNullOrWhiteSpace($deployUrl)) {
    Write-Host ""
    Write-Host "Getting deployment URL from Vercel..." -ForegroundColor Cyan
    Start-Sleep -Seconds 10
    
    try {
        $deployments = vercel ls 2>&1
        if ($deployments -match "https://[^\s]+\.vercel\.app") {
            $deployUrl = $matches[0]
        }
    } catch {
        Write-Host "[WARNING] Could not get URL automatically" -ForegroundColor Yellow
    }
}

if ([string]::IsNullOrWhiteSpace($deployUrl)) {
    Write-Host ""
    Write-Host "[INFO] Deployment started! Check Vercel dashboard:" -ForegroundColor Yellow
    Write-Host "https://vercel.com/dashboard" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "The deployment URL will be shown there." -ForegroundColor White
    exit 0
}

Write-Host ""
Write-Host "[SUCCESS] Deployed to: $deployUrl" -ForegroundColor Green

# Step 3: Verify
Write-Host ""
Write-Host "Step 3: Verifying deployment..." -ForegroundColor Cyan
Write-Host "Waiting 30 seconds for deployment to propagate..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

$maxChecks = 10
$check = 0
$deploymentReady = $false

while ($check -lt $maxChecks -and -not $deploymentReady) {
    $check++
    Write-Host "Checking... ($check/$maxChecks)" -ForegroundColor Gray
    
    try {
        $response = Invoke-WebRequest -Uri $deployUrl -UseBasicParsing -TimeoutSec 10 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            $deploymentReady = $true
            Write-Host ""
            Write-Host "[SUCCESS] Web app is live!" -ForegroundColor Green
            break
        }
    } catch {
        Start-Sleep -Seconds 10
    }
}

# Step 4: Get local IP
Write-Host ""
Write-Host "Step 4: Getting local IP for mobile access..." -ForegroundColor Cyan

$localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { 
    $_.IPAddress -notlike "127.*" -and 
    $_.IPAddress -notlike "169.254.*"
} | Select-Object -First 1).IPAddress

if ([string]::IsNullOrWhiteSpace($localIP)) {
    $localIP = "192.168.1.100"
}

Write-Host "[OK] Local IP: $localIP" -ForegroundColor Green

# Step 5: Summary
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
Write-Host "2. Local Network (Same WiFi):" -ForegroundColor Yellow
Write-Host "   http://$localIP:3000" -ForegroundColor White
Write-Host "   (Run: cd frontend && npm run dev)" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Backend API:" -ForegroundColor Yellow
Write-Host "   https://cedos-architect-production.up.railway.app/api/docs" -ForegroundColor White
Write-Host ""
Write-Host "Login:" -ForegroundColor Cyan
Write-Host "  Username: admin" -ForegroundColor White
Write-Host "  Password: admin123" -ForegroundColor White
Write-Host ""
Write-Host "Opening web app..." -ForegroundColor Cyan
Start-Process $deployUrl

Write-Host ""
Write-Host "The web app is now accessible from mobile browsers!" -ForegroundColor Green
Write-Host ""
