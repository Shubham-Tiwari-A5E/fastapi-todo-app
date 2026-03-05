@echo off
cls
echo.
echo ================================================
echo    FastAPI Todo App - Simple Start (No Reload)
echo ================================================
echo.
echo Starting server without auto-reload...
echo (Restart manually to see code changes)
echo.

cd /d "%~dp0"

C:\Users\A5E\Python\FastAPI\fastapienv\Scripts\python.exe run_simple.py

pause
