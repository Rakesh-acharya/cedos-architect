# ============================================================
#   CREATE KEYSTORE AND BUILD APK - Complete Automation
# ============================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  Creating Keystore and Building APK" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

Set-Location "C:\Users\rakes\architect\cedos-mobile"

# Step 1: Check Java/Keytool
Write-Host "Step 1: Checking Java installation..." -ForegroundColor Cyan

$javaPath = Get-Command java -ErrorAction SilentlyContinue
if (-not $javaPath) {
    Write-Host "[ERROR] Java not found!" -ForegroundColor Red
    Write-Host "Installing Java..." -ForegroundColor Yellow
    
    # Try to find Java in common locations
    $javaLocations = @(
        "$env:JAVA_HOME\bin\java.exe",
        "C:\Program Files\Java\*\bin\java.exe",
        "C:\Program Files (x86)\Java\*\bin\java.exe"
    )
    
    $foundJava = $false
    foreach ($loc in $javaLocations) {
        if (Test-Path $loc) {
            $env:PATH = (Split-Path $loc) + ";" + $env:PATH
            $foundJava = $true
            Write-Host "[OK] Found Java at: $loc" -ForegroundColor Green
            break
        }
    }
    
    if (-not $foundJava) {
        Write-Host "[ERROR] Java not found. Please install Java JDK first." -ForegroundColor Red
        Write-Host "Download from: https://www.oracle.com/java/technologies/downloads/" -ForegroundColor Yellow
        exit 1
    }
}

$keytoolPath = Get-Command keytool -ErrorAction SilentlyContinue
if (-not $keytoolPath) {
    Write-Host "[ERROR] Keytool not found!" -ForegroundColor Red
    exit 1
}

Write-Host "[OK] Java and Keytool found" -ForegroundColor Green
Write-Host ""

# Step 2: Generate Keystore
Write-Host "Step 2: Generating Android Keystore..." -ForegroundColor Cyan

$keystorePath = Join-Path (Get-Location) "cedos-keystore.jks"
$keystorePassword = "Cedos@123456"
$keyAlias = "cedos-key"
$keyPassword = "Cedos@123456"

if (Test-Path $keystorePath) {
    Write-Host "[INFO] Keystore already exists, using existing one" -ForegroundColor Yellow
} else {
    Write-Host "Creating keystore..." -ForegroundColor Cyan
    Write-Host "Keystore Password: $keystorePassword" -ForegroundColor Gray
    Write-Host "Key Alias: $keyAlias" -ForegroundColor Gray
    Write-Host "Key Password: $keyPassword" -ForegroundColor Gray
    Write-Host ""
    
    # Create keystore with 25-year validity
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
    
    $keytoolProcess = Start-Process -FilePath "keytool" -ArgumentList $keytoolArgs -NoNewWindow -Wait -PassThru
    
    if ($keytoolProcess.ExitCode -ne 0) {
        Write-Host "[ERROR] Failed to create keystore!" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "[OK] Keystore created successfully!" -ForegroundColor Green
    Write-Host "Location: $keystorePath" -ForegroundColor Cyan
}

Write-Host ""

# Step 3: Configure EAS Credentials
Write-Host "Step 3: Configuring EAS credentials..." -ForegroundColor Cyan

Write-Host "Uploading keystore to Expo..." -ForegroundColor Yellow

# Use eas credentials to upload keystore
$credArgs = @(
    "--platform", "android",
    "--non-interactive"
)

# Create a credentials file or use eas credentials command
Write-Host "Setting up credentials..." -ForegroundColor Cyan

# Try to configure credentials
$env:EXPO_ANDROID_KEYSTORE_PATH = $keystorePath
$env:EXPO_ANDROID_KEYSTORE_PASSWORD = $keystorePassword
$env:EXPO_ANDROID_KEY_ALIAS = $keyAlias
$env:EXPO_ANDROID_KEY_PASSWORD = $keyPassword

# Upload keystore via eas credentials
Write-Host "Uploading keystore file..." -ForegroundColor Cyan

# Use eas credentials update command
$updateCreds = @(
    "credentials",
    "--platform", "android",
    "--non-interactive"
) | Out-String

Write-Host "[INFO] Keystore ready for upload" -ForegroundColor Yellow
Write-Host ""
Write-Host "Keystore Details:" -ForegroundColor Cyan
Write-Host "  File: $keystorePath" -ForegroundColor White
Write-Host "  Keystore Password: $keystorePassword" -ForegroundColor White
Write-Host "  Key Alias: $keyAlias" -ForegroundColor White
Write-Host "  Key Password: $keyPassword" -ForegroundColor White
Write-Host ""
Write-Host "Please upload this keystore file to Expo:" -ForegroundColor Yellow
Write-Host "  1. Go to: https://expo.dev/accounts/rakeshacherya/projects/cedos-mobile/credentials/android" -ForegroundColor Cyan
Write-Host "  2. Click 'Upload Keystore'" -ForegroundColor White
Write-Host "  3. Upload file: $keystorePath" -ForegroundColor White
Write-Host "  4. Enter Keystore Password: $keystorePassword" -ForegroundColor White
Write-Host "  5. Enter Key Alias: $keyAlias" -ForegroundColor White
Write-Host "  6. Enter Key Password: $keyPassword" -ForegroundColor White
Write-Host "  7. Click 'Save'" -ForegroundColor White
Write-Host ""
Write-Host "Opening credentials page..." -ForegroundColor Cyan
Start-Process "https://expo.dev/accounts/rakeshacherya/projects/cedos-mobile/credentials/android"

Write-Host ""
Write-Host "Waiting 120 seconds for keystore upload..." -ForegroundColor Yellow
Start-Sleep -Seconds 120

# Step 4: Build APK
Write-Host ""
Write-Host "Step 4: Building APK..." -ForegroundColor Cyan
Write-Host ""

$maxAttempts = 5
$attempt = 0
$buildStarted = $false
$buildId = ""

while ($attempt -lt $maxAttempts -and -not $buildStarted) {
    $attempt++
    Write-Host "Build attempt $attempt of $maxAttempts..." -ForegroundColor Yellow
    
    $buildOutput = eas build --platform android --profile production --non-interactive 2>&1 | Tee-Object -Variable fullOutput
    
    if ($LASTEXITCODE -eq 0 -or $fullOutput -match "Build ID" -or $fullOutput -match "build ID" -or $fullOutput -match "Started build") {
        Write-Host ""
        Write-Host "[SUCCESS] Build started!" -ForegroundColor Green
        Write-Host $fullOutput
        
        # Extract build ID
        if ($fullOutput -match "build ID: (\w+)") {
            $buildId = $matches[1]
        } elseif ($fullOutput -match "Build ID: (\w+)") {
            $buildId = $matches[1]
        }
        
        $buildStarted = $true
        break
    } else {
        Write-Host "[WARNING] Build failed, retrying..." -ForegroundColor Yellow
        Write-Host $fullOutput
        Start-Sleep -Seconds 30
    }
}

if (-not $buildStarted) {
    Write-Host ""
    Write-Host "[ERROR] Could not start build!" -ForegroundColor Red
    Write-Host "Please ensure keystore is uploaded at:" -ForegroundColor Yellow
    Write-Host "https://expo.dev/accounts/rakeshacherya/projects/cedos-mobile/credentials/android" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Keystore file: $keystorePath" -ForegroundColor Cyan
    exit 1
}

# Step 5: Wait for build and download
Write-Host ""
Write-Host "Step 5: Waiting for build to complete..." -ForegroundColor Cyan
Write-Host "This will take 10-15 minutes..." -ForegroundColor Yellow
Write-Host ""

if ([string]::IsNullOrWhiteSpace($buildId)) {
    Write-Host "Getting latest build ID..." -ForegroundColor Cyan
    Start-Sleep -Seconds 10
    try {
        $buildList = eas build:list --platform android --limit 1 --json 2>&1 | ConvertFrom-Json
        if ($buildList -and $buildList.Count -gt 0) {
            $buildId = $buildList[0].id
        }
    } catch {
        Write-Host "[WARNING] Could not get build ID automatically" -ForegroundColor Yellow
    }
}

if (-not [string]::IsNullOrWhiteSpace($buildId)) {
    Write-Host "Build ID: $buildId" -ForegroundColor Cyan
    Write-Host ""
    
    $maxChecks = 120
    $check = 0
    $buildComplete = $false
    $downloadUrl = ""
    
    while ($check -lt $maxChecks -and -not $buildComplete) {
        $check++
        Start-Sleep -Seconds 10
        
        Write-Host "Checking build status... ($check/$maxChecks)" -ForegroundColor Gray
        
        try {
            $buildInfo = eas build:view $buildId --json 2>&1 | ConvertFrom-Json
            
            if ($buildInfo.status -eq "finished") {
                $buildComplete = $true
                $downloadUrl = $buildInfo.artifacts.buildUrl
                Write-Host ""
                Write-Host "[SUCCESS] Build completed!" -ForegroundColor Green
                break
            } elseif ($buildInfo.status -eq "errored") {
                Write-Host ""
                Write-Host "[ERROR] Build failed!" -ForegroundColor Red
                exit 1
            }
        } catch {
            # Build still in progress
        }
    }
    
    if ($buildComplete -and -not [string]::IsNullOrWhiteSpace($downloadUrl)) {
        # Download APK
        Write-Host ""
        Write-Host "Step 6: Downloading APK..." -ForegroundColor Cyan
        Write-Host ""
        
        Set-Location ".."
        $apkPath = Join-Path (Get-Location) "cedos.apk"
        
        Write-Host "Downloading from: $downloadUrl" -ForegroundColor Cyan
        Write-Host "Saving to: $apkPath" -ForegroundColor Cyan
        Write-Host ""
        
        try {
            Invoke-WebRequest -Uri $downloadUrl -OutFile $apkPath -UseBasicParsing
            
            if (Test-Path $apkPath) {
                $fileSize = (Get-Item $apkPath).Length / 1MB
                Write-Host ""
                Write-Host "============================================================" -ForegroundColor Green
                Write-Host "  APK BUILD SUCCESSFUL!" -ForegroundColor Green
                Write-Host "============================================================" -ForegroundColor Green
                Write-Host ""
                Write-Host "APK Location: $apkPath" -ForegroundColor Cyan
                Write-Host "File Size: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Cyan
                Write-Host ""
                Write-Host "Keystore saved at: $keystorePath" -ForegroundColor Cyan
                Write-Host ""
                Write-Host "Copy this APK to your phone and install it!" -ForegroundColor Green
                Write-Host ""
                Write-Host "The app is configured to connect to:" -ForegroundColor Yellow
                Write-Host "  https://cedos-architect-production.up.railway.app/api/v1" -ForegroundColor Cyan
                Write-Host ""
            } else {
                Write-Host "[ERROR] APK download failed!" -ForegroundColor Red
                Write-Host "Download manually from: $downloadUrl" -ForegroundColor Yellow
            }
        } catch {
            Write-Host "[ERROR] Download failed: $_" -ForegroundColor Red
            Write-Host "Download manually from: $downloadUrl" -ForegroundColor Yellow
        }
    } else {
        Write-Host ""
        Write-Host "[INFO] Build in progress. Check status at:" -ForegroundColor Yellow
        Write-Host "https://expo.dev/accounts/rakeshacherya/projects/cedos-mobile/builds/$buildId" -ForegroundColor Cyan
    }
} else {
    Write-Host ""
    Write-Host "[INFO] Build started! Check status at:" -ForegroundColor Yellow
    Write-Host "https://expo.dev/accounts/rakeshacherya/projects/cedos-mobile/builds" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  COMPLETE!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
