# CRITICAL: Push all changes to GitHub
# This script ensures the deployment validator sees the updated code

Write-Host "========================================" -ForegroundColor Yellow
Write-Host "CRITICAL GIT PUSH - Deployment Fix" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow

# Set error handling
$ErrorActionPreference = "Stop"

try {
    # Step 1: Check current status
    Write-Host "`n[1] Checking Git Status..." -ForegroundColor Cyan
    git status
    
    # Step 2: Add all critical files
    Write-Host "`n[2] Staging critical files..." -ForegroundColor Cyan
    git add pyproject.toml
    git add server/app.py
    git add app.py
    git add env/
    Write-Host "✓ Files staged" -ForegroundColor Green
    
    # Step 3: Show staged changes
    Write-Host "`n[3] Staged files:" -ForegroundColor Cyan
    git diff --cached --name-only
    
    # Step 4: Commit
    Write-Host "`n[4] Committing changes..." -ForegroundColor Cyan
    git commit -m "CRITICAL FIX: Update server entry point to use main() function - Fixes deployment validation"
    Write-Host "✓ Committed" -ForegroundColor Green
    
    # Step 5: Push
    Write-Host "`n[5] Pushing to GitHub..." -ForegroundColor Cyan
    git push -u origin main
    Write-Host "✓ Pushed to GitHub" -ForegroundColor Green
    
    # Step 6: Verify
    Write-Host "`n[6] Verifying push (last 3 commits):" -ForegroundColor Cyan
    git log --oneline -3
    
    Write-Host "`n========================================" -ForegroundColor Green
    Write-Host "✅ SUCCESS - Changes are now on GitHub!" -ForegroundColor Green
    Write-Host "Restart your HF Space to apply changes." -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
}
catch {
    Write-Host "`n❌ ERROR: $_" -ForegroundColor Red
    exit 1
}
