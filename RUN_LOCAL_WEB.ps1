# ============================================================
#   RUN WEB LOCALLY FOR MOBILE ACCESS
#   Runs dev server accessible via local IP
# ============================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  RUNNING WEB APP LOCALLY FOR MOBILE ACCESS" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

Set-Location "C:\Users\rakes\architect\frontend"

# Get local IP
Write-Host "Getting local IP address..." -ForegroundColor Cyan
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

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  STARTING DEV SERVER" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Access from:" -ForegroundColor Cyan
Write-Host "  - Desktop: http://localhost:3000" -ForegroundColor White
Write-Host "  - Mobile (same WiFi): http://$localIP:3000" -ForegroundColor White
Write-Host ""
Write-Host "Backend API: https://cedos-architect-production.up.railway.app" -ForegroundColor Cyan
Write-Host ""
Write-Host "Login:" -ForegroundColor Yellow
Write-Host "  Username: admin" -ForegroundColor White
Write-Host "  Password: admin123" -ForegroundColor White
Write-Host ""
Write-Host "Starting dev server..." -ForegroundColor Cyan
Write-Host ""

# Update vite config to allow external access
$viteConfig = Get-Content "vite.config.ts" -Raw
if ($viteConfig -notmatch "host.*true") {
    $viteConfig = $viteConfig -replace "server:\s*\{", "server: {`n    host: '0.0.0.0',"
    Set-Content -Path "vite.config.ts" -Value $viteConfig
    Write-Host "[OK] Updated Vite config for external access" -ForegroundColor Green
}

# Start dev server
npm run dev
