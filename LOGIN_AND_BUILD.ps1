# ============================================================
#   LOGIN TO EXPO AND BUILD APK
#   Complete automated build
# ============================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  CEDOS - Auto Login & Build APK" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

# Step 1: Login to Expo
Write-Host "Step 1: Logging in to Expo..." -ForegroundColor Cyan
Write-Host ""

$expoEmail = "rakeshacherya123@gmail.com"
$expoPassword = "Rakesh@123#$"

# Try to login
Write-Host "Attempting login..." -ForegroundColor Yellow
Write-Host "Email: $expoEmail" -ForegroundColor Gray
Write-Host ""

# Use expect-like approach or manual login
Write-Host "Please login manually (script will continue after login)..." -ForegroundColor Yellow
Write-Host "Opening Expo login..." -ForegroundColor Cyan

# Open browser for login
Start-Process "https://expo.dev/login"

# Run login command
Write-Host ""
Write-Host "In the terminal that opens, enter:" -ForegroundColor Yellow
Write-Host "  Email: $expoEmail" -ForegroundColor White
Write-Host "  Password: [your password]" -ForegroundColor White
Write-Host ""

# Try interactive login
$loginProcess = Start-Process -FilePath "eas" -ArgumentList "login" -NoNewWindow -Wait -PassThru

Start-Sleep -Seconds 3

# Check login status
$whoamiCheck = eas whoami 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[ERROR] Login failed or not completed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please run this command manually:" -ForegroundColor Yellow
    Write-Host "  eas login" -ForegroundColor White
    Write-Host ""
    Write-Host "Then run:" -ForegroundColor Yellow
    Write-Host "  powershell -ExecutionPolicy Bypass -File BUILD_APK.ps1" -ForegroundColor White
    Write-Host ""
    exit 1
}

$expoUser = eas whoami
Write-Host ""
Write-Host "[OK] Logged in as: $expoUser" -ForegroundColor Green
Write-Host ""

# Step 2: Run build script
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host "  Step 2: Building APK" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host ""

Write-Host "Running BUILD_APK.ps1..." -ForegroundColor Cyan
Write-Host ""

& ".\BUILD_APK.ps1"
