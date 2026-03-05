@echo off
echo ============================================================
echo   FASTAPI TODO APP - COMPLETE SETUP AND FIX
echo ============================================================
echo.

cd /d C:\Users\A5E\Python\FastAPI\Todos

echo Step 1: Installing required packages...
echo ----------------------------------------
..\fastapienv\Scripts\pip install python-dotenv twilio pymysql
echo.

echo Step 2: Fixing database schema...
echo ----------------------------------
..\fastapienv\Scripts\python fix_database.py
echo.

echo Step 3: Checking environment variables...
echo ------------------------------------------
if exist .env (
    echo ✅ .env file found
    echo.
    echo Current .env content:
    type .env
    echo.
) else (
    echo ❌ .env file NOT found!
    echo.
    echo Creating .env.example for you to copy...
    (
        echo # Twilio WhatsApp Configuration
        echo TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        echo TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        echo TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
        echo.
        echo # Database Configuration
        echo DATABASE_HOST=localhost
        echo DATABASE_PORT=3306
        echo DATABASE_USER=root
        echo DATABASE_PASSWORD=raj1234
        echo DATABASE_NAME=todos
    ) > .env.example
    echo.
    echo ⚠️  ACTION REQUIRED:
    echo    1. Get Twilio credentials from: https://console.twilio.com
    echo    2. Copy .env.example to .env
    echo    3. Replace the XXX values with your actual Twilio credentials
    echo.
)

echo Step 4: Testing Twilio connection...
echo --------------------------------------
..\fastapienv\Scripts\python -c "import os; from dotenv import load_dotenv; load_dotenv(); sid = os.getenv('TWILIO_ACCOUNT_SID'); token = os.getenv('TWILIO_AUTH_TOKEN'); print('TWILIO_ACCOUNT_SID:', 'SET ✅' if sid and not sid.startswith('AC') == False else 'NOT SET ❌'); print('TWILIO_AUTH_TOKEN:', 'SET ✅' if token and len(token) == 32 else 'NOT SET ❌'); print('TWILIO_WHATSAPP_NUMBER:', os.getenv('TWILIO_WHATSAPP_NUMBER', 'NOT SET ❌'))"
echo.

echo Step 5: Verifying database...
echo ------------------------------
..\fastapienv\Scripts\python -c "import pymysql; conn = pymysql.connect(host='localhost', user='root', password='raj1234', database='todos'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM users'); print(f'Total users: {cursor.fetchone()[0]}'); cursor.execute('SELECT COUNT(*) FROM todos'); print(f'Total todos: {cursor.fetchone()[0]}'); cursor.close(); conn.close(); print('✅ Database connected successfully')"
echo.

echo ============================================================
echo   SETUP COMPLETE!
echo ============================================================
echo.
echo 🚀 To start the server:
echo    ..\fastapienv\Scripts\uvicorn main:app --reload
echo.
echo 📖 For Twilio setup guide:
echo    Open: TWILIO_COMPLETE_SETUP.md
echo.
echo ⚠️  If WhatsApp is still not working:
echo    1. Get credentials from https://console.twilio.com
echo    2. Join WhatsApp sandbox (+1 415 523 8886)
echo    3. Update .env file with your credentials
echo    4. Restart the server
echo.
pause
