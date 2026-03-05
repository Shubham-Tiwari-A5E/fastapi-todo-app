@echo off
echo Installing python-dotenv...
C:\Users\A5E\Python\FastAPI\fastapienv\Scripts\python.exe -m pip install python-dotenv
echo.
echo Testing...
C:\Users\A5E\Python\FastAPI\fastapienv\Scripts\python.exe -c "from dotenv import load_dotenv; print('SUCCESS: dotenv works!')"
echo.
pause
