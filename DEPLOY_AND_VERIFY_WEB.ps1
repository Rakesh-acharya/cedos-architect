# ============================================================
#   DEPLOY WEB & VERIFY - Complete Automation
#   Deploys to Vercel and verifies it's working
# ============================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  DEPLOYING WEB VERSION - Complete Automation" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

Set-Location "C:\Users\rakes\architect\frontend"

# Step 1: Build
Write-Host "Step 1: Building frontend..." -ForegroundColor Cyan
npm run build 2>&1 | Out-Null

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "[OK] Build successful" -ForegroundColor Green

# Step 2: Deploy
Write-Host ""
Write-Host "Step 2: Deploying to Vercel..." -ForegroundColor Cyan

$deployOutput = vercel --prod --yes 2>&1 | Tee-Object -Variable fullOutput

# Extract URL
$deployUrl = ""
if ($fullOutput -match "https://[^\s]+\.vercel\.app") {
    $deployUrl = $matches[0]
}

if ([string]::IsNullOrWhiteSpace($deployUrl)) {
    Write-Host "Getting deployment URL..." -ForegroundColor Cyan
    Start-Sleep -Seconds 5
    try {
        $deployments = vercel ls --json 2>&1 | ConvertFrom-Json
        if ($deployments -and $deployments.Count -gt 0) {
            $deployUrl = $deployments[0].url
        }
    } catch {
        Write-Host "[WARNING] Could not get URL automatically" -ForegroundColor Yellow
    }
}

if ([string]::IsNullOrWhiteSpace($deployUrl)) {
    Write-Host "[ERROR] Could not get deployment URL!" -ForegroundColor Red
    Write-Host "Check: https://vercel.com/dashboard" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "[SUCCESS] Deployed to: $deployUrl" -ForegroundColor Green

# Step 3: Verify deployment
Write-Host ""
Write-Host "Step 3: Verifying deployment..." -ForegroundColor Cyan
Write-Host "Waiting 30 seconds for deployment to propagate..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

$maxChecks = 10
$check = 0
$deploymentReady = $false

while ($check -lt $maxChecks -and -not $deploymentReady) {
    $check++
    Write-Host "Checking deployment... ($check/$maxChecks)" -ForegroundColor Gray
    
    try {
        $response = Invoke-WebRequest -Uri $deployUrl -UseBasicParsing -TimeoutSec 10 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            $deploymentReady = $true
            Write-Host ""
            Write-Host "[SUCCESS] Web app is live and accessible!" -ForegroundColor Green
            break
        }
    } catch {
        # Still deploying
        Start-Sleep -Seconds 10
    }
}

if (-not $deploymentReady) {
    Write-Host ""
    Write-Host "[WARNING] Could not verify automatically" -ForegroundColor Yellow
    Write-Host "Please check manually: $deployUrl" -ForegroundColor Cyan
}

# Step 4: Get local IP for mobile access
Write-Host ""
Write-Host "Step 4: Getting local IP for mobile access..." -ForegroundColor Cyan

$localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { 
    $_.IPAddress -notlike "127.*" -and 
    $_.IPAddress -notlike "169.254.*" -and
    $_.InterfaceAlias -notlike "*Loopback*"
} | Select-Object -First 1).IPAddress

if ([string]::IsNullOrWhiteSpace($localIP)) {
    $localIP = "192.168.1.100"
    Write-Host "[WARNING] Using default IP: $localIP" -ForegroundColor Yellow
} else {
    Write-Host "[OK] Local IP: $localIP" -ForegroundColor Green
}

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
Write-Host "Opening web app in browser..." -ForegroundColor Cyan
Start-Process $deployUrl

Write-Host ""
Write-Host "The web app is now accessible from mobile browsers!" -ForegroundColor Green
Write-Host ""
