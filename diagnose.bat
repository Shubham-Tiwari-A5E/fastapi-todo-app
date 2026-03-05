@echo off
echo ========================================
echo Python Environment Diagnostic
echo ========================================
echo.

cd /d "%~dp0"

echo [1] System Python:
where python
python --version
echo.

echo [2] Virtual Environment Python:
echo Location: %~dp0..\fastapienv\Scripts\python.exe
..\fastapienv\Scripts\python.exe --version
echo.

echo [3] Testing python-dotenv in venv:
..\fastapienv\Scripts\python.exe -c "import sys; print('Executable:', sys.executable); from dotenv import load_dotenv; print('✅ dotenv imported successfully!')"
echo.

echo [4] Listing installed packages:
..\fastapienv\Scripts\pip.exe list | findstr dotenv
echo.

echo [5] Python sys.path in venv:
..\fastapienv\Scripts\python.exe -c "import sys; print('\n'.join(sys.path))"
echo.

echo ========================================
echo Diagnostic Complete
echo ========================================
pause
