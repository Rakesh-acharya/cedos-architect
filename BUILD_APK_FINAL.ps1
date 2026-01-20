# ============================================================
#   FINAL APK BUILD - Complete Automation
#   Keeps retrying until APK is generated
# ============================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  FINAL APK BUILD - Complete Automation" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

Set-Location "C:\Users\rakes\architect\cedos-mobile"

# Ensure EAS project is initialized
Write-Host "Initializing EAS project..." -ForegroundColor Cyan
eas init --force --non-interactive 2>&1 | Out-Null

# Update eas.json
$easJson = @{
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
$easJson | ConvertTo-Json -Depth 10 | Set-Content -Path "eas.json"

Write-Host "[OK] EAS configured" -ForegroundColor Green
Write-Host ""

# Show keystore info
$keystorePath = Join-Path (Get-Location) "cedos-keystore.jks"
Write-Host "Keystore Information:" -ForegroundColor Cyan
Write-Host "  File: $keystorePath" -ForegroundColor White
Write-Host "  Password: Cedos@123456" -ForegroundColor White
Write-Host "  Alias: cedos-key" -ForegroundColor White
Write-Host "  Key Password: Cedos@123456" -ForegroundColor White
Write-Host ""
Write-Host "Opening credentials page..." -ForegroundColor Yellow
Start-Process "https://expo.dev/accounts/rakeshacherya/projects/cedos-mobile/credentials/android"

Write-Host ""
Write-Host "Please upload the keystore file in the browser that opened." -ForegroundColor Yellow
Write-Host "Waiting 240 seconds for upload..." -ForegroundColor Cyan
Start-Sleep -Seconds 240

# Keep retrying build until success
Write-Host ""
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host "  Building APK - Will retry until success" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host ""

$attempt = 0
$buildStarted = $false
$buildId = ""

while (-not $buildStarted) {
    $attempt++
    Write-Host "Build attempt $attempt..." -ForegroundColor Yellow
    
    $buildOutput = eas build --platform android --profile production --non-interactive 2>&1 | Tee-Object -Variable fullOutput
    
    if ($LASTEXITCODE -eq 0 -or $fullOutput -match "Build ID" -or $fullOutput -match "build ID" -or $fullOutput -match "Started build" -or $fullOutput -match "Queued") {
        Write-Host ""
        Write-Host "[SUCCESS] Build started!" -ForegroundColor Green
        
        if ($fullOutput -match "build ID: (\w+)") {
            $buildId = $matches[1]
        } elseif ($fullOutput -match "Build ID: (\w+)") {
            $buildId = $matches[1]
        }
        
        $buildStarted = $true
        break
    } else {
        Write-Host "[INFO] Build not ready, waiting 30 seconds before retry..." -ForegroundColor Gray
        Start-Sleep -Seconds 30
    }
}

# Get build ID if not extracted
if ([string]::IsNullOrWhiteSpace($buildId)) {
    Write-Host "Getting build ID..." -ForegroundColor Cyan
    Start-Sleep -Seconds 15
    try {
        $buildList = eas build:list --platform android --limit 1 --json 2>&1 | ConvertFrom-Json
        if ($buildList -and $buildList.Count -gt 0) {
            $buildId = $buildList[0].id
        }
    } catch {}
}

# Wait for build completion
Write-Host ""
Write-Host "Waiting for build to complete (10-15 minutes)..." -ForegroundColor Cyan
Write-Host "Build ID: $buildId" -ForegroundColor Gray
Write-Host ""

$maxChecks = 180
$check = 0
$buildComplete = $false
$downloadUrl = ""

while ($check -lt $maxChecks -and -not $buildComplete) {
    $check++
    Start-Sleep -Seconds 10
    
    if ($check % 12 -eq 0) {
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
            exit 1
        }
    } catch {
        # Still building
    }
}

# Download APK
if ($buildComplete -and -not [string]::IsNullOrWhiteSpace($downloadUrl)) {
    Write-Host ""
    Write-Host "Downloading APK..." -ForegroundColor Cyan
    
    Set-Location ".."
    $apkPath = Join-Path (Get-Location) "cedos.apk"
    
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
        }
    } catch {
        Write-Host "[ERROR] Download failed. Get it from: $downloadUrl" -ForegroundColor Red
    }
} else {
    Write-Host ""
    Write-Host "[INFO] Build in progress. Check: https://expo.dev/accounts/rakeshacherya/projects/cedos-mobile/builds/$buildId" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  COMPLETE!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
