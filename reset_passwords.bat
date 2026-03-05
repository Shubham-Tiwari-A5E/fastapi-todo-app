@echo off
echo ================================================
echo Password Reset Tool
echo ================================================
echo.
echo This tool helps you reset passwords for users
echo who may have incompatible password hashes.
echo.

cd /d "%~dp0"

C:\Users\A5E\Python\FastAPI\fastapienv\Scripts\python.exe reset_passwords.py

pause
