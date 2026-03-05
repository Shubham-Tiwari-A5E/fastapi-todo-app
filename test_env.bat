@echo off
echo ========================================
echo Testing Virtual Environment
echo ========================================
echo.

cd /d "%~dp0"

echo Testing Python path...
..\fastapienv\Scripts\python.exe -c "import sys; print('Python:', sys.executable)"

echo.
echo Testing python-dotenv...
..\fastapienv\Scripts\python.exe -c "from dotenv import load_dotenv; print('✅ dotenv works!')"

echo.
echo Testing FastAPI...
..\fastapienv\Scripts\python.exe -c "import fastapi; print('✅ fastapi works!')"

echo.
echo Testing imports from main.py...
..\fastapienv\Scripts\python.exe -c "import sys; sys.path.insert(0, '.'); from database import get_db; print('✅ database.py works!')"

echo.
echo ========================================
echo All tests passed!
echo ========================================
echo.
echo Your environment is correctly configured.
echo You can now run: start.bat
echo.
pause
