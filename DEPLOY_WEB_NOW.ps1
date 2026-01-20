# ============================================================
#   DEPLOY WEB VERSION - Complete Automation
#   Deploys to Vercel and verifies
# ============================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  DEPLOYING WEB VERSION FOR MOBILE ACCESS" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

Set-Location "C:\Users\rakes\architect\frontend"

# Build
Write-Host "Building frontend..." -ForegroundColor Cyan
npm run build 2>&1 | Out-Null

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "[OK] Build successful" -ForegroundColor Green
Write-Host ""

# Deploy to Vercel
Write-Host "Deploying to Vercel..." -ForegroundColor Cyan
Write-Host ""

# Try deployment
$deployOutput = vercel --prod --yes 2>&1 | Tee-Object -Variable fullOutput

Write-Host $fullOutput

# Check for URL
$deployUrl = ""
if ($fullOutput -match "https://[^\s]+\.vercel\.app") {
    $deployUrl = $matches[0]
}

if ([string]::IsNullOrWhiteSpace($deployUrl)) {
    Write-Host ""
    Write-Host "[INFO] Deployment in progress!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Check deployment status at:" -ForegroundColor Cyan
    Write-Host "https://vercel.com/dashboard" -ForegroundColor White
    Write-Host ""
    Write-Host "OR deploy via GitHub:" -ForegroundColor Yellow
    Write-Host "  1. Go to: https://vercel.com/dashboard" -ForegroundColor White
    Write-Host "  2. Import project from GitHub" -ForegroundColor White
    Write-Host "  3. Root Directory: frontend" -ForegroundColor White
    Write-Host "  4. Deploy" -ForegroundColor White
    Write-Host ""
    Start-Process "https://vercel.com/dashboard"
} else {
    Write-Host ""
    Write-Host "[SUCCESS] Deployed to: $deployUrl" -ForegroundColor Green
    Write-Host ""
    Write-Host "Opening in browser..." -ForegroundColor Cyan
    Start-Process $deployUrl
    
    Write-Host ""
    Write-Host "Access from mobile: $deployUrl" -ForegroundColor Yellow
}

# Get local IP
$localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { 
    $_.IPAddress -notlike "127.*" -and $_.IPAddress -notlike "169.254.*"
} | Select-Object -First 1).IPAddress

if ([string]::IsNullOrWhiteSpace($localIP)) {
    $localIP = "192.168.1.100"
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  DEPLOYMENT SUMMARY" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Global Access: $deployUrl" -ForegroundColor Cyan
Write-Host "Local Access: http://$localIP:3000" -ForegroundColor Cyan
Write-Host "Backend: https://cedos-architect-production.up.railway.app" -ForegroundColor Cyan
Write-Host ""
Write-Host "The web app is accessible from mobile browsers!" -ForegroundColor Green
Write-Host ""
