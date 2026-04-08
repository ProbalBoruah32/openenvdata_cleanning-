# Force commit and push all critical changes
Write-Host "Adding critical files..." -ForegroundColor Cyan
git add pyproject.toml server/app.py app.py

Write-Host "Committing changes..." -ForegroundColor Cyan
git commit -m "Critical: Update entry point to server.app:main with proper main() function"

Write-Host "Pushing to GitHub..." -ForegroundColor Cyan
git push origin main

Write-Host "✅ Done! Changes pushed to GitHub" -ForegroundColor Green
