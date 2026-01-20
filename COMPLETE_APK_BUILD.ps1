# ============================================================
#   COMPLETE APK BUILD - From Keystore to APK
# ============================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  COMPLETE APK BUILD - Automated" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

Set-Location "C:\Users\rakes\architect\cedos-mobile"

# Keystore details
$keystorePath = Join-Path (Get-Location) "cedos-keystore.jks"
$keystorePassword = "Cedos@123456"
$keyAlias = "cedos-key"
$keyPassword = "Cedos@123456"

Write-Host "Step 1: Keystore Information" -ForegroundColor Cyan
Write-Host ""
Write-Host "Keystore File: $keystorePath" -ForegroundColor White
Write-Host "Keystore Password: $keystorePassword" -ForegroundColor White
Write-Host "Key Alias: $keyAlias" -ForegroundColor White
Write-Host "Key Password: $keyPassword" -ForegroundColor White
Write-Host ""

if (-not (Test-Path $keystorePath)) {
    Write-Host "[ERROR] Keystore not found! Creating..." -ForegroundColor Red
    
    # Check for Java
    $keytool = Get-Command keytool -ErrorAction SilentlyContinue
    if (-not $keytool) {
        Write-Host "[ERROR] Java Keytool not found!" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "Creating keystore..." -ForegroundColor Cyan
    keytool -genkeypair -v -storetype JKS -keystore $keystorePath -alias $keyAlias -keyalg RSA -keysize 2048 -validity 9125 -storepass $keystorePassword -keypass $keyPassword -dname "CN=CEDOS, OU=Mobile, O=CEDOS, L=City, ST=State, C=US" 2>&1 | Out-Null
    
    if (-not (Test-Path $keystorePath)) {
        Write-Host "[ERROR] Failed to create keystore!" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "[OK] Keystore created!" -ForegroundColor Green
}

Write-Host ""
Write-Host "Step 2: Upload Keystore to Expo" -ForegroundColor Cyan
Write-Host ""
Write-Host "Opening credentials page..." -ForegroundColor Yellow
Start-Process "https://expo.dev/accounts/rakeshacherya/projects/cedos-mobile/credentials/android"

Write-Host ""
Write-Host "IMPORTANT: Upload the keystore file:" -ForegroundColor Yellow
Write-Host "  1. Click 'Upload Keystore' or 'Set up credentials'" -ForegroundColor White
Write-Host "  2. Upload file: $keystorePath" -ForegroundColor White
Write-Host "  3. Enter:" -ForegroundColor White
Write-Host "     - Keystore Password: $keystorePassword" -ForegroundColor Gray
Write-Host "     - Key Alias: $keyAlias" -ForegroundColor Gray
Write-Host "     - Key Password: $keyPassword" -ForegroundColor Gray
Write-Host "  4. Click 'Save'" -ForegroundColor White
Write-Host ""
Write-Host "Waiting 180 seconds for upload..." -ForegroundColor Cyan
Start-Sleep -Seconds 180

# Step 3: Initialize EAS Project
Write-Host ""
Write-Host "Step 3: Initializing EAS Project" -ForegroundColor Cyan
Write-Host ""

$easInit = eas init --force --non-interactive 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[WARNING] EAS init had issues, but continuing..." -ForegroundColor Yellow
} else {
    Write-Host "[OK] EAS project initialized" -ForegroundColor Green
}

# Update eas.json
$easJsonPath = Join-Path (Get-Location) "eas.json"
$easJsonContent = @{
    build = @{
        production = @{
            android = @{
                buildType = "apk"
            }
        }
    }
    cli = @{
        appVersionSource = "remote"
    }
}
$easJsonContent | ConvertTo-Json -Depth 10 | Set-Content -Path $easJsonPath

Write-Host "[OK] EAS configuration updated" -ForegroundColor Green

# Step 4: Build APK
Write-Host ""
Write-Host "Step 4: Building APK" -ForegroundColor Cyan
Write-Host ""

$maxAttempts = 15
$attempt = 0
$buildStarted = $false
$buildId = ""

while ($attempt -lt $maxAttempts -and -not $buildStarted) {
    $attempt++
    Write-Host "Build attempt $attempt of $maxAttempts..." -ForegroundColor Yellow
    
    $buildOutput = eas build --platform android --profile production --non-interactive 2>&1 | Tee-Object -Variable fullOutput
    
    Write-Host $fullOutput
    
    if ($LASTEXITCODE -eq 0 -or $fullOutput -match "Build ID" -or $fullOutput -match "build ID" -or $fullOutput -match "Started build" -or $fullOutput -match "Queued") {
        Write-Host ""
        Write-Host "[SUCCESS] Build started!" -ForegroundColor Green
        
        # Extract build ID
        if ($fullOutput -match "build ID: (\w+)") {
            $buildId = $matches[1]
        } elseif ($fullOutput -match "Build ID: (\w+)") {
            $buildId = $matches[1]
        }
        
        $buildStarted = $true
        break
    } else {
        Write-Host "[WARNING] Build not started yet, retrying in 20 seconds..." -ForegroundColor Yellow
        Start-Sleep -Seconds 20
    }
}

if (-not $buildStarted) {
    Write-Host ""
    Write-Host "[ERROR] Could not start build!" -ForegroundColor Red
    Write-Host "Please ensure keystore is uploaded at:" -ForegroundColor Yellow
    Write-Host "https://expo.dev/accounts/rakeshacherya/projects/cedos-mobile/credentials/android" -ForegroundColor Cyan
    Write-Host ""
    exit 1
}

# Step 5: Wait for build and download
Write-Host ""
Write-Host "Step 5: Waiting for Build Completion" -ForegroundColor Cyan
Write-Host "This will take 10-15 minutes..." -ForegroundColor Yellow
Write-Host ""

if ([string]::IsNullOrWhiteSpace($buildId)) {
    Write-Host "Getting latest build ID..." -ForegroundColor Cyan
    Start-Sleep -Seconds 15
    try {
        $buildList = eas build:list --platform android --limit 1 --json 2>&1 | ConvertFrom-Json
        if ($buildList -and $buildList.Count -gt 0) {
            $buildId = $buildList[0].id
            Write-Host "Found build ID: $buildId" -ForegroundColor Green
        }
    } catch {
        Write-Host "[WARNING] Could not get build ID automatically" -ForegroundColor Yellow
    }
}

if (-not [string]::IsNullOrWhiteSpace($buildId)) {
    Write-Host "Monitoring build: $buildId" -ForegroundColor Cyan
    Write-Host ""
    
    $maxChecks = 120
    $check = 0
    $buildComplete = $false
    $downloadUrl = ""
    
    while ($check -lt $maxChecks -and -not $buildComplete) {
        $check++
        Start-Sleep -Seconds 10
        
        if ($check % 6 -eq 0) {
            Write-Host "Checking build status... ($check/$maxChecks)" -ForegroundColor Gray
        }
        
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
                Write-Host "Check: https://expo.dev/accounts/rakeshacherya/projects/cedos-mobile/builds/$buildId" -ForegroundColor Yellow
                exit 1
            }
        } catch {
            # Build still in progress
        }
    }
    
    if ($buildComplete -and -not [string]::IsNullOrWhiteSpace($downloadUrl)) {
        # Step 6: Download APK
        Write-Host ""
        Write-Host "Step 6: Downloading APK" -ForegroundColor Cyan
        Write-Host ""
        
        Set-Location ".."
        $apkPath = Join-Path (Get-Location) "cedos.apk"
        
        Write-Host "Download URL: $downloadUrl" -ForegroundColor Cyan
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
                Write-Host "Copy this APK to your phone and install it!" -ForegroundColor Green
                Write-Host ""
                Write-Host "The app is configured to connect to:" -ForegroundColor Yellow
                Write-Host "  https://cedos-architect-production.up.railway.app/api/v1" -ForegroundColor Cyan
                Write-Host ""
                Write-Host "Login credentials:" -ForegroundColor Yellow
                Write-Host "  Username: admin" -ForegroundColor White
                Write-Host "  Password: admin123" -ForegroundColor White
                Write-Host ""
            } else {
                Write-Host "[ERROR] APK download failed!" -ForegroundColor Red
                Write-Host "Download manually from: $downloadUrl" -ForegroundColor Yellow
                exit 1
            }
        } catch {
            Write-Host "[ERROR] Download failed: $_" -ForegroundColor Red
            Write-Host "Download manually from: $downloadUrl" -ForegroundColor Yellow
            exit 1
        }
    } else {
        Write-Host ""
        Write-Host "[INFO] Build still in progress. Check status at:" -ForegroundColor Yellow
        Write-Host "https://expo.dev/accounts/rakeshacherya/projects/cedos-mobile/builds/$buildId" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Once build completes, download the APK from the link above." -ForegroundColor Yellow
    }
} else {
    Write-Host ""
    Write-Host "[INFO] Build started! Check status at:" -ForegroundColor Yellow
    Write-Host "https://expo.dev/accounts/rakeshacherya/projects/cedos-mobile/builds" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Once build completes, download the APK from the Expo dashboard." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  COMPLETE!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
