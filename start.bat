@echo off
echo ================================
echo FastAPI Todo App - Quick Start
echo ================================
echo.

cd /d "%~dp0"

set VENV_PYTHON=%~dp0..\fastapienv\Scripts\python.exe

echo Using Python: %VENV_PYTHON%
echo.

echo [1/3] Running database migrations...
%VENV_PYTHON% -m alembic upgrade head

echo.
echo [2/3] Testing environment...
%VENV_PYTHON% -c "from dotenv import load_dotenv; print('✅ Environment OK')"

echo.
echo [3/3] Starting FastAPI server...
echo.
echo ================================
echo Server starting on http://127.0.0.1:8000
echo API Docs: http://127.0.0.1:8000/docs
echo Press CTRL+C to stop the server
echo ================================
echo.

%VENV_PYTHON% run.py

pause
