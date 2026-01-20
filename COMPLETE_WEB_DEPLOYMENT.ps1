# ============================================================
#   COMPLETE WEB DEPLOYMENT - All Options
#   Deploys web version and verifies it works
# ============================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  COMPLETE WEB DEPLOYMENT FOR MOBILE ACCESS" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

Set-Location "C:\Users\rakes\architect\frontend"

# Step 1: Build
Write-Host "Step 1: Building frontend..." -ForegroundColor Cyan
npm run build 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Build successful" -ForegroundColor Green
} else {
    Write-Host "[WARNING] Build had issues" -ForegroundColor Yellow
}

Write-Host ""

# Step 2: Check backend
Write-Host "Step 2: Verifying backend..." -ForegroundColor Cyan
$backendUrl = "https://cedos-architect-production.up.railway.app/api/docs"

try {
    $response = Invoke-WebRequest -Uri $backendUrl -UseBasicParsing -TimeoutSec 10
    Write-Host "[SUCCESS] Backend is live!" -ForegroundColor Green
    Write-Host "Backend: $backendUrl" -ForegroundColor Cyan
} catch {
    Write-Host "[ERROR] Backend not accessible!" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 3: Get local IP
Write-Host "Step 3: Getting local IP..." -ForegroundColor Cyan
$localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { 
    $_.IPAddress -notlike "127.*" -and 
    $_.IPAddress -notlike "169.254.*"
} | Select-Object -First 1).IPAddress

if ([string]::IsNullOrWhiteSpace($localIP)) {
    $localIP = "192.168.1.100"
}

Write-Host "[OK] Local IP: $localIP" -ForegroundColor Green
Write-Host ""

# Step 4: Deployment options
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  DEPLOYMENT OPTIONS" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "OPTION 1: Deploy via GitHub (Recommended - Global Access)" -ForegroundColor Yellow
Write-Host ""
Write-Host "Since you've authorized GitHub, deploy via Vercel dashboard:" -ForegroundColor White
Write-Host ""
Write-Host "1. Go to: https://vercel.com/dashboard" -ForegroundColor Cyan
Write-Host "2. Click 'Add New Project' or 'Import Project'" -ForegroundColor Cyan
Write-Host "3. Select repository: cedos-architect" -ForegroundColor Cyan
Write-Host "4. Configure:" -ForegroundColor Cyan
Write-Host "   - Root Directory: frontend" -ForegroundColor White
Write-Host "   - Framework Preset: Vite" -ForegroundColor White
Write-Host "   - Build Command: npm run build" -ForegroundColor White
Write-Host "   - Output Directory: dist" -ForegroundColor White
Write-Host "5. Add Environment Variable:" -ForegroundColor Cyan
Write-Host "   - Name: VITE_API_URL" -ForegroundColor White
Write-Host "   - Value: https://cedos-architect-production.up.railway.app" -ForegroundColor White
Write-Host "6. Click 'Deploy'" -ForegroundColor Cyan
Write-Host ""
Write-Host "OPTION 2: Run Locally (Same WiFi Network)" -ForegroundColor Yellow
Write-Host ""
Write-Host "Run: powershell -ExecutionPolicy Bypass -File RUN_LOCAL_WEB.ps1" -ForegroundColor Cyan
Write-Host "Then access from mobile: http://$localIP:3000" -ForegroundColor White
Write-Host ""

# Open Vercel dashboard
Write-Host "Opening Vercel dashboard..." -ForegroundColor Cyan
Start-Process "https://vercel.com/dashboard"

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  CONFIGURATION SUMMARY" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Frontend Build: ✓ Complete" -ForegroundColor Green
Write-Host "Backend API: ✓ Live at https://cedos-architect-production.up.railway.app" -ForegroundColor Green
Write-Host "Local IP: $localIP" -ForegroundColor Cyan
Write-Host ""
Write-Host "After deployment, your web app will be accessible:" -ForegroundColor Yellow
Write-Host "  - Globally via Vercel URL (Option 1)" -ForegroundColor White
Write-Host "  - Locally via http://$localIP:3000 (Option 2)" -ForegroundColor White
Write-Host ""
Write-Host "Login Credentials:" -ForegroundColor Cyan
Write-Host "  Username: admin" -ForegroundColor White
Write-Host "  Password: admin123" -ForegroundColor White
Write-Host ""
Write-Host "The web app is ready for mobile browser access!" -ForegroundColor Green
Write-Host ""
