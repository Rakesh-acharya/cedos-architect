# ============================================================
#   CHECK WEB DEPLOYMENT STATUS
#   Verifies if web app is deployed and accessible
# ============================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  CHECKING WEB DEPLOYMENT STATUS" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

# Check Vercel deployments
Write-Host "Checking Vercel deployments..." -ForegroundColor Cyan

try {
    $deployments = vercel ls 2>&1
    
    if ($deployments -match "https://[^\s]+\.vercel\.app") {
        $deployUrl = $matches[0]
        Write-Host ""
        Write-Host "[FOUND] Deployment URL: $deployUrl" -ForegroundColor Green
        
        Write-Host ""
        Write-Host "Testing accessibility..." -ForegroundColor Cyan
        try {
            $response = Invoke-WebRequest -Uri $deployUrl -UseBasicParsing -TimeoutSec 10
            if ($response.StatusCode -eq 200) {
                Write-Host "[SUCCESS] Web app is live and accessible!" -ForegroundColor Green
                Write-Host ""
                Write-Host "Access from mobile: $deployUrl" -ForegroundColor Yellow
                Write-Host ""
                Write-Host "Opening in browser..." -ForegroundColor Cyan
                Start-Process $deployUrl
            }
        } catch {
            Write-Host "[WARNING] Could not verify accessibility" -ForegroundColor Yellow
            Write-Host "Please check manually: $deployUrl" -ForegroundColor Cyan
        }
    } else {
        Write-Host ""
        Write-Host "[INFO] No deployment found via CLI" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Check Vercel dashboard:" -ForegroundColor Cyan
        Write-Host "https://vercel.com/dashboard" -ForegroundColor White
        Write-Host ""
        Start-Process "https://vercel.com/dashboard"
    }
} catch {
    Write-Host "[INFO] Vercel CLI not configured" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Check Vercel dashboard:" -ForegroundColor Cyan
    Write-Host "https://vercel.com/dashboard" -ForegroundColor White
    Write-Host ""
    Start-Process "https://vercel.com/dashboard"
}

# Check backend
Write-Host ""
Write-Host "Checking backend API..." -ForegroundColor Cyan
$backendUrl = "https://cedos-architect-production.up.railway.app/api/docs"

try {
    $response = Invoke-WebRequest -Uri $backendUrl -UseBasicParsing -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "[SUCCESS] Backend is live!" -ForegroundColor Green
        Write-Host "Backend API: $backendUrl" -ForegroundColor Cyan
    }
} catch {
    Write-Host "[WARNING] Could not verify backend" -ForegroundColor Yellow
    Write-Host "Backend URL: $backendUrl" -ForegroundColor Cyan
}

# Get local IP
Write-Host ""
Write-Host "Getting local IP for mobile access..." -ForegroundColor Cyan
$localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { 
    $_.IPAddress -notlike "127.*" -and 
    $_.IPAddress -notlike "169.254.*"
} | Select-Object -First 1).IPAddress

if ([string]::IsNullOrWhiteSpace($localIP)) {
    $localIP = "192.168.1.100"
}

Write-Host "[OK] Local IP: $localIP" -ForegroundColor Green

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  SUMMARY" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Global Access: Check Vercel dashboard" -ForegroundColor Cyan
Write-Host "Local Access: http://$localIP:3000 (run RUN_LOCAL_WEB.ps1)" -ForegroundColor Cyan
Write-Host "Backend: https://cedos-architect-production.up.railway.app" -ForegroundColor Cyan
Write-Host ""
Write-Host "Login:" -ForegroundColor Yellow
Write-Host "  Username: admin" -ForegroundColor White
Write-Host "  Password: admin123" -ForegroundColor White
Write-Host ""
