@echo off
echo ╔══════════════════════════════════════════════════════╗
echo ║  🚀 DEPLOY TO RENDER - AUTO MIGRATION ENABLED       ║
echo ╚══════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo [1/3] Checking git status...
git status --short
echo.

echo [2/3] Adding all changes...
git add .
echo.

echo [3/3] Committing changes...
set /p commit_message="Enter commit message (or press Enter for default): "
if "%commit_message%"=="" set commit_message=Deploy with automatic migration

git commit -m "%commit_message%"
echo.

echo ════════════════════════════════════════════════════════
echo Ready to push to GitHub (Render will auto-deploy)
echo ════════════════════════════════════════════════════════
echo.
echo What will happen:
echo   1. Code pushed to GitHub
echo   2. Render detects push
echo   3. Render builds your app
echo   4. App starts
echo   5. 🔄 Migrations run AUTOMATICALLY
echo   6. ✅ App ready with database set up!
echo.
set /p confirm="Push to GitHub and deploy? (y/n): "

if /i "%confirm%"=="y" (
    echo.
    echo Pushing to GitHub...
    git push origin main
    echo.
    echo ════════════════════════════════════════════════════════
    echo ✅ Push complete!
    echo ════════════════════════════════════════════════════════
    echo.
    echo 📊 Track deployment:
    echo    https://dashboard.render.com
    echo.
    echo 📋 View logs:
    echo    Dashboard → Your Service → Logs
    echo.
    echo 🔍 Look for:
    echo    "🔄 Running database migrations..."
    echo    "✅ Database migrations completed!"
    echo.
    echo ⏱️  Deployment takes ~3-5 minutes
    echo.
) else (
    echo.
    echo ❌ Deployment cancelled
    echo    You can deploy later with: git push origin main
    echo.
)

pause
