# ============================================================
#   DEPLOY WEB VIA GITHUB - Vercel Dashboard
#   Opens Vercel dashboard for GitHub deployment
# ============================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  DEPLOY WEB VERSION VIA GITHUB" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

Set-Location "C:\Users\rakes\architect\frontend"

# Build first
Write-Host "Step 1: Building frontend..." -ForegroundColor Cyan
npm run build 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Build successful" -ForegroundColor Green
} else {
    Write-Host "[WARNING] Build had issues, but continuing..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Step 2: Opening Vercel dashboard..." -ForegroundColor Cyan
Write-Host ""

Write-Host "INSTRUCTIONS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Click 'Add New Project' or 'Import Project'" -ForegroundColor White
Write-Host "2. Select GitHub repository: cedos-architect" -ForegroundColor White
Write-Host "3. Configure:" -ForegroundColor White
Write-Host "   - Root Directory: frontend" -ForegroundColor Cyan
Write-Host "   - Framework Preset: Vite" -ForegroundColor Cyan
Write-Host "   - Build Command: npm run build" -ForegroundColor Cyan
Write-Host "   - Output Directory: dist" -ForegroundColor Cyan
Write-Host "4. Add Environment Variable:" -ForegroundColor White
Write-Host "   - Name: VITE_API_URL" -ForegroundColor Cyan
Write-Host "   - Value: https://cedos-architect-production.up.railway.app" -ForegroundColor Cyan
Write-Host "5. Click 'Deploy'" -ForegroundColor White
Write-Host ""

Start-Process "https://vercel.com/dashboard"

Write-Host "Vercel dashboard opened!" -ForegroundColor Green
Write-Host ""
Write-Host "After deployment, your web app will be accessible globally!" -ForegroundColor Cyan
Write-Host ""
