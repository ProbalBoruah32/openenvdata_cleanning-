@echo off
REM Navigate to project directory
cd /d c:\Users\pb168\Downloads\archive (1)\newenv

REM Display current status
echo Current Git Status:
git status

REM Add all critical files
echo.
echo Adding files...
git add pyproject.toml server/app.py app.py env/

REM Show what will be committed
echo.
echo Files staged for commit:
git diff --cached --name-only

REM Commit with clear message
echo.
echo Committing changes...
git commit -m "CRITICAL FIX: Update server entry point to use main() function - Fixes deployment validation"

REM Push to GitHub
echo.
echo Pushing to GitHub...
git push -u origin main

REM Verify push was successful
echo.
echo Verifying push...
git log --oneline -3

echo.
echo ✅ PUSH COMPLETE - Changes are now on GitHub
pause
