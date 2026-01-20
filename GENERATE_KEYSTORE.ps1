# ============================================================
#   GENERATE KEYSTORE FOR EXPO
# ============================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  Generating Android Keystore" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

Set-Location "C:\Users\rakes\architect\cedos-mobile"

# Check for Java
$javaFound = $false
$keytoolPath = $null

# Check common Java locations
$javaLocations = @(
    "C:\Program Files\Java\*\bin\keytool.exe",
    "C:\Program Files (x86)\Java\*\bin\keytool.exe",
    "$env:JAVA_HOME\bin\keytool.exe"
)

foreach ($pattern in $javaLocations) {
    $found = Get-ChildItem -Path $pattern -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($found) {
        $keytoolPath = $found.FullName
        $javaBin = Split-Path $keytoolPath
        $env:PATH = $javaBin + ";" + $env:PATH
        $javaFound = $true
        Write-Host "[OK] Found Java Keytool at: $keytoolPath" -ForegroundColor Green
        break
    }
}

# Also check if keytool is in PATH
if (-not $javaFound) {
    $keytoolCheck = Get-Command keytool -ErrorAction SilentlyContinue
    if ($keytoolCheck) {
        $keytoolPath = $keytoolCheck.Source
        $javaFound = $true
        Write-Host "[OK] Found Java Keytool in PATH" -ForegroundColor Green
    }
}

if (-not $javaFound) {
    Write-Host ""
    Write-Host "[ERROR] Java JDK not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Java JDK:" -ForegroundColor Yellow
    Write-Host "  1. Download from: https://www.oracle.com/java/technologies/downloads/#java21" -ForegroundColor Cyan
    Write-Host "  2. Install Java JDK" -ForegroundColor White
    Write-Host "  3. Run this script again" -ForegroundColor White
    Write-Host ""
    Write-Host "Opening download page..." -ForegroundColor Cyan
    Start-Process "https://www.oracle.com/java/technologies/downloads/#java21"
    exit 1
}

# Generate keystore
Write-Host ""
Write-Host "Generating Android Keystore..." -ForegroundColor Cyan
Write-Host ""

$keystorePath = Join-Path (Get-Location) "cedos-keystore.jks"
$keystorePassword = "Cedos@123456"
$keyAlias = "cedos-key"
$keyPassword = "Cedos@123456"

if (Test-Path $keystorePath) {
    Write-Host "[INFO] Keystore already exists: $keystorePath" -ForegroundColor Yellow
    Write-Host "Using existing keystore..." -ForegroundColor Gray
} else {
    Write-Host "Creating new keystore..." -ForegroundColor Cyan
    Write-Host "  File: $keystorePath" -ForegroundColor Gray
    Write-Host "  Keystore Password: $keystorePassword" -ForegroundColor Gray
    Write-Host "  Key Alias: $keyAlias" -ForegroundColor Gray
    Write-Host "  Key Password: $keyPassword" -ForegroundColor Gray
    Write-Host ""
    
    $keytoolArgs = @(
        "-genkeypair",
        "-v",
        "-storetype", "JKS",
        "-keystore", $keystorePath,
        "-alias", $keyAlias,
        "-keyalg", "RSA",
        "-keysize", "2048",
        "-validity", "9125",
        "-storepass", $keystorePassword,
        "-keypass", $keyPassword,
        "-dname", "CN=CEDOS, OU=Mobile, O=CEDOS, L=City, ST=State, C=US"
    )
    
    & keytool $keytoolArgs
    
    if (Test-Path $keystorePath) {
        Write-Host ""
        Write-Host "[SUCCESS] Keystore created!" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "[ERROR] Failed to create keystore!" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  KEYSTORE READY!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Keystore Details:" -ForegroundColor Cyan
Write-Host "  File: $keystorePath" -ForegroundColor White
Write-Host "  Keystore Password: $keystorePassword" -ForegroundColor White
Write-Host "  Key Alias: $keyAlias" -ForegroundColor White
Write-Host "  Key Password: $keyPassword" -ForegroundColor White
Write-Host ""
Write-Host "Now upload this keystore to Expo:" -ForegroundColor Yellow
Write-Host "  1. Go to: https://expo.dev/accounts/rakeshacherya/projects/cedos-mobile/credentials/android" -ForegroundColor Cyan
Write-Host "  2. Click 'Upload Keystore' or 'Set up credentials'" -ForegroundColor White
Write-Host "  3. Upload file: $keystorePath" -ForegroundColor White
Write-Host "  4. Enter:" -ForegroundColor White
Write-Host "     - Keystore Password: $keystorePassword" -ForegroundColor Gray
Write-Host "     - Key Alias: $keyAlias" -ForegroundColor Gray
Write-Host "     - Key Password: $keyPassword" -ForegroundColor Gray
Write-Host "  5. Click 'Save'" -ForegroundColor White
Write-Host ""
Write-Host "Opening credentials page..." -ForegroundColor Cyan
Start-Process "https://expo.dev/accounts/rakeshacherya/projects/cedos-mobile/credentials/android"

Write-Host ""
Write-Host "After uploading, run: .\BUILD_APK.ps1" -ForegroundColor Green
Write-Host ""
