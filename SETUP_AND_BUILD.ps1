# ============================================================
#   COMPLETE APK BUILD - Auto Setup & Build
# ============================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  CEDOS - Complete APK Build Setup" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

Set-Location "C:\Users\rakes\architect\cedos-mobile"

# Check if credentials exist
Write-Host "Checking credentials..." -ForegroundColor Cyan
$credCheck = eas credentials --platform android 2>&1

if ($credCheck -match "No credentials" -or $credCheck -match "not set up") {
    Write-Host ""
    Write-Host "[INFO] Credentials need to be set up (one-time only)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Opening Expo dashboard..." -ForegroundColor Cyan
    Start-Process "https://expo.dev/accounts/rakeshacherya/projects/cedos-mobile/credentials/android"
    
    Write-Host ""
    Write-Host "Please:" -ForegroundColor Yellow
    Write-Host "  1. In the browser that opened, click 'Set up credentials'" -ForegroundColor White
    Write-Host "  2. Select 'Let Expo manage credentials'" -ForegroundColor White
    Write-Host "  3. Click 'Save'" -ForegroundColor White
    Write-Host ""
    Write-Host "Waiting 60 seconds for you to set up credentials..." -ForegroundColor Cyan
    Start-Sleep -Seconds 60
    
    Write-Host ""
    Write-Host "Checking credentials again..." -ForegroundColor Cyan
    $credCheck2 = eas credentials --platform android 2>&1
    if ($credCheck2 -match "No credentials" -or $credCheck2 -match "not set up") {
        Write-Host ""
        Write-Host "[WARNING] Credentials still not set up!" -ForegroundColor Red
        Write-Host "Please set them up manually, then run BUILD_APK.ps1" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host "[OK] Credentials configured!" -ForegroundColor Green
Write-Host ""

# Now run the build
Write-Host "Starting build..." -ForegroundColor Cyan
Set-Location ".."
& ".\BUILD_APK.ps1"
