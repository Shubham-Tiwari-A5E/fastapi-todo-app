@echo off
echo ========================================
echo Installing All Dependencies
echo ========================================
echo.

cd /d "%~dp0"

echo Installing python-dotenv...
..\fastapienv\Scripts\python.exe -m pip install python-dotenv==1.2.1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install python-dotenv
    pause
    exit /b 1
)

echo.
echo Installing all requirements...
..\fastapienv\Scripts\python.exe -m pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install requirements
    pause
    exit /b 1
)

echo.
echo ========================================
echo Testing installation...
echo ========================================
..\fastapienv\Scripts\python.exe -c "from dotenv import load_dotenv; print('✅ python-dotenv: OK')"
..\fastapienv\Scripts\python.exe -c "import fastapi; print('✅ fastapi: OK')"
..\fastapienv\Scripts\python.exe -c "import uvicorn; print('✅ uvicorn: OK')"

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo You can now start the server with:
echo   start.bat
echo.
pause
