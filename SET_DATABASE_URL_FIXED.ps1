# Set DATABASE_URL in Railway with proper URL encoding
# This handles passwords with special characters

Write-Host ""
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host "  Set Railway DATABASE_URL (URL-Encoded)" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host ""

# Change to backend directory
Set-Location -Path "$PSScriptRoot\backend"

# Get Supabase password
Write-Host "Enter your Supabase password:" -ForegroundColor Cyan
Write-Host "(Special characters will be automatically URL-encoded)" -ForegroundColor Gray
Write-Host ""
$password = Read-Host "Supabase Password" -AsSecureString
$passwordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($password))

if ([string]::IsNullOrWhiteSpace($passwordPlain)) {
    Write-Host ""
    Write-Host "[ERROR] Password required!" -ForegroundColor Red
    pause
    exit 1
}

# URL encode the password
Add-Type -AssemblyName System.Web
$passwordEncoded = [System.Web.HttpUtility]::UrlEncode($passwordPlain)

Write-Host ""
Write-Host "Password URL-encoded successfully" -ForegroundColor Green
Write-Host ""

# Construct DATABASE_URL
$databaseUrl = "postgresql://postgres:$passwordEncoded@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres"

Write-Host "Setting DATABASE_URL in Railway..." -ForegroundColor Cyan
Write-Host ""

# Set the variable in Railway
railway variables set DATABASE_URL="$databaseUrl"

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "[OK] DATABASE_URL set successfully!" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "Verifying variables..." -ForegroundColor Cyan
    railway variables
    Write-Host ""
    
    Write-Host "Redeploying..." -ForegroundColor Cyan
    railway up
    Write-Host ""
    
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host "  Done! Railway will auto-redeploy" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "The DATABASE_URL has been set with proper URL encoding." -ForegroundColor White
    Write-Host "Special characters in password are now properly encoded." -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "[ERROR] Failed to set DATABASE_URL" -ForegroundColor Red
    Write-Host ""
    Write-Host "Try manually in Railway dashboard:" -ForegroundColor Yellow
    Write-Host "1. Go to Railway dashboard" -ForegroundColor Gray
    Write-Host "2. Your service - Variables tab" -ForegroundColor Gray
    Write-Host "3. Add: DATABASE_URL" -ForegroundColor Gray
    Write-Host "4. Value: $databaseUrl" -ForegroundColor Gray
    Write-Host ""
}

pause
