# ============================================================
#   FINAL APK BUILD - Complete Automation
# ============================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  FINAL APK BUILD - Complete Automation" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

Set-Location "C:\Users\rakes\architect\cedos-mobile"

# Check and set up credentials via web
Write-Host "Step 1: Setting up credentials..." -ForegroundColor Cyan
Write-Host ""

$credUrl = "https://expo.dev/accounts/rakeshacherya/projects/cedos-mobile/credentials/android"
Write-Host "Opening credentials page..." -ForegroundColor Yellow
Start-Process $credUrl

Write-Host ""
Write-Host "IMPORTANT: Please set up credentials in the browser:" -ForegroundColor Yellow
Write-Host "  1. Click 'Set up credentials' or 'Generate credentials'" -ForegroundColor White
Write-Host "  2. Select 'Let Expo manage credentials'" -ForegroundColor White
Write-Host "  3. Click 'Save' or 'Generate'" -ForegroundColor White
Write-Host ""
Write-Host "Waiting 180 seconds for credential setup..." -ForegroundColor Cyan
Start-Sleep -Seconds 180

# Try build with retries
Write-Host ""
Write-Host "Step 2: Building APK..." -ForegroundColor Cyan
Write-Host ""

$maxAttempts = 10
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
    } elseif ($fullOutput -match "credentials" -or $fullOutput -match "Keystore") {
        Write-Host "[WARNING] Credentials not ready yet..." -ForegroundColor Yellow
        Write-Host "Waiting 30 seconds before retry..." -ForegroundColor Gray
        Start-Sleep -Seconds 30
    } else {
        Write-Host "[ERROR] Build failed" -ForegroundColor Red
        Write-Host $fullOutput
        Start-Sleep -Seconds 10
    }
}

if (-not $buildStarted) {
    Write-Host ""
    Write-Host "[ERROR] Could not start build!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please ensure credentials are set up at:" -ForegroundColor Yellow
    Write-Host $credUrl -ForegroundColor Cyan
    Write-Host ""
    exit 1
}

# Wait for build and download
Write-Host ""
Write-Host "Step 3: Waiting for build to complete..." -ForegroundColor Cyan
Write-Host "This will take 10-15 minutes..." -ForegroundColor Yellow
Write-Host ""

if ([string]::IsNullOrWhiteSpace($buildId)) {
    Write-Host "Getting latest build ID..." -ForegroundColor Cyan
    Start-Sleep -Seconds 10
    $buildList = eas build:list --platform android --limit 1 --json 2>&1 | ConvertFrom-Json
    if ($buildList -and $buildList.Count -gt 0) {
        $buildId = $buildList[0].id
    }
}

if ([string]::IsNullOrWhiteSpace($buildId)) {
    Write-Host "[WARNING] Could not get build ID. Check status at:" -ForegroundColor Yellow
    Write-Host "https://expo.dev/accounts/rakeshacherya/projects/cedos-mobile/builds" -ForegroundColor Cyan
    exit 0
}

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

if (-not $buildComplete) {
    Write-Host ""
    Write-Host "[WARNING] Build still in progress. Check status at:" -ForegroundColor Yellow
    Write-Host "https://expo.dev/accounts/rakeshacherya/projects/cedos-mobile/builds/$buildId" -ForegroundColor Cyan
    exit 0
}

# Download APK
Write-Host ""
Write-Host "Step 4: Downloading APK..." -ForegroundColor Cyan
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
        Write-Host "Copy this APK to your phone and install it!" -ForegroundColor Green
        Write-Host ""
        Write-Host "The app is configured to connect to:" -ForegroundColor Yellow
        Write-Host "  https://cedos-architect-production.up.railway.app/api/v1" -ForegroundColor Cyan
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

Write-Host "============================================================" -ForegroundColor Green
Write-Host "  COMPLETE!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
