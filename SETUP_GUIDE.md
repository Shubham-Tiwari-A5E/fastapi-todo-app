# 🚀 FastAPI Todo App - Complete Setup Guide

## ✅ What's Been Fixed

1. **Database Issues**
   - Fixed `notification_enabled` field to always have a default value (TRUE)
   - Added proper database migrations
   - Support for both MySQL (local) and PostgreSQL (production)

2. **Authentication**
   - Updated to use `bcrypt` for password hashing
   - SECRET_KEY now loaded from environment variables
   - Fixed JWT token generation and validation

3. **Phone Number Saving**
   - Phone numbers are now properly saved during registration
   - WhatsApp welcome messages sent when phone number provided

4. **Code Cleanup**
   - Removed unnecessary documentation files
   - Fixed requirements.txt encoding issue
   - Added bcrypt dependency

## 🔧 Local Development Setup

### Step 1: Install Dependencies

```bash
cd C:\Users\A5E\Python\FastAPI
.\fastapienv\Scripts\activate
cd Todos
pip install -r requirements.txt
```

### Step 2: Configure Environment

Your `.env` file is already configured at `C:\Users\A5E\Python\FastAPI\Todos\.env`

**Current Configuration:**
- MySQL Database: `localhost:3306`
- Database Name: `todos`
- WhatsApp: Enabled with Twilio

### Step 3: Run Migrations

```bash
cd C:\Users\A5E\Python\FastAPI\Todos
..\fastapienv\Scripts\alembic.exe upgrade head
```

### Step 4: Start the Server

```bash
cd C:\Users\A5E\Python\FastAPI\Todos
..\fastapienv\Scripts\uvicorn.exe main:app --reload
```

Or from the parent directory:

```bash
cd C:\Users\A5E\Python\FastAPI
.\fastapienv\Scripts\uvicorn.exe Todos.main:app --reload
```

### Step 5: Access the Application

Open your browser and visit:
- **Home Page:** http://127.0.0.1:8000
- **Login:** http://127.0.0.1:8000/login
- **Register:** http://127.0.0.1:8000/register
- **API Docs:** http://127.0.0.1:8000/docs

## 📱 WhatsApp Setup

Your Twilio credentials are configured in `.env`. To test:

1. **Join Twilio Sandbox**
   - Go to: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
   - Send the join code to: +1 415 523 8886
   - Example: "join [your-code-here]"

2. **Test Welcome Message**
   - Register a new user with phone number: +919876543210 (your format)
   - You should receive a welcome message on WhatsApp

3. **Test Task Reminders**
   - Create a todo with a task time 11-12 minutes in the future
   - Enable notifications
   - You'll receive a WhatsApp reminder 10 minutes before

## 🗄️ Database Schema

### Users Table
- `id` (UUID)
- `name` (string)
- `email` (string, unique)
- `password_hash` (string)
- `phone_number` (string, optional)

### Todos Table
- `id` (UUID)
- `title` (string)
- `description` (string, optional)
- `priority` (1-5)
- `isCompleted` (boolean)
- `task_time` (datetime, optional)
- `notification_enabled` (boolean, default TRUE)
- `user_id` (foreign key)
- `created_at` (datetime)
- `completed_at` (datetime, optional)

## 🧪 Testing

Run all tests:

```bash
cd C:\Users\A5E\Python\FastAPI\Todos
..\fastapienv\Scripts\pytest.exe
```

Run specific test file:

```bash
..\fastapienv\Scripts\pytest.exe test/test_api.py -v
```

## 🌐 Deployment to Render

### Prerequisites
1. Push code to GitHub
2. Create Render account

### Steps

1. **Create PostgreSQL Database**
   - Dashboard → New → PostgreSQL
   - Name: `todos_db`
   - Copy the external database URL

2. **Create Web Service**
   - Dashboard → New → Web Service
   - Connect GitHub repository
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port 10000`

3. **Environment Variables**
   - `SECRET_KEY`: Generate a strong random key
   - `TWILIO_ACCOUNT_SID`: Your Twilio SID
   - `TWILIO_AUTH_TOKEN`: Your Twilio token
   - `TWILIO_WHATSAPP_NUMBER`: whatsapp:+14155238886
   - `DATABASE_URL`: (Auto-set by Render when you link the database)

4. **Deploy**
   - Push to GitHub
   - Render auto-deploys on every push

## 🔍 Troubleshooting

### Server Won't Start

```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process if needed
taskkill /PID <PID> /F
```

### Database Connection Issues

```bash
# Check MySQL is running
Get-Service -Name MySQL*

# Start MySQL if needed
Start-Service -Name MySQL80
```

### Import Errors

```bash
# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

### Migration Issues

```bash
# Check migration status
..\fastapienv\Scripts\alembic.exe current

# Reset to specific version
..\fastapienv\Scripts\alembic.exe downgrade <revision>

# Apply all migrations
..\fastapienv\Scripts\alembic.exe upgrade head
```

## 📝 API Testing with cURL

### Register User

```bash
curl -X POST "http://127.0.0.1:8000/register" ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Test User\",\"email\":\"test@example.com\",\"password\":\"Test123!\",\"phone_number\":\"+919876543210\"}"
```

### Login

```bash
curl -X POST "http://127.0.0.1:8000/token" ^
  -H "Content-Type: application/x-www-form-urlencoded" ^
  -d "username=test@example.com&password=Test123!"
```

### Get Todos (with token)

```bash
curl -X GET "http://127.0.0.1:8000/todos" ^
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Create Todo

```bash
curl -X POST "http://127.0.0.1:8000/todos" ^
  -H "Authorization: Bearer YOUR_TOKEN_HERE" ^
  -H "Content-Type: application/json" ^
  -d "{\"title\":\"Test Todo\",\"description\":\"Test Description\",\"priority\":3,\"task_time\":\"2026-03-05T15:00:00\",\"notification_enabled\":true}"
```

## 🎯 Key Features Implemented

✅ User registration with phone number  
✅ JWT authentication  
✅ WhatsApp welcome messages  
✅ Task creation with time  
✅ 10-minute WhatsApp reminders  
✅ Toggle notifications per task  
✅ Beautiful UI with Jinja2 templates  
✅ Complete CRUD operations  
✅ Priority-based task organization  
✅ Completed tasks tracking  
✅ Production-ready structure  
✅ Comprehensive testing  
✅ Database migrations with Alembic  
✅ MySQL (local) and PostgreSQL (production) support  

## 🔒 Security Notes

- Never commit `.env` file to Git
- Generate strong SECRET_KEY for production
- Keep Twilio credentials secure
- Use HTTPS in production
- Implement rate limiting for production

## 📞 Support

If you encounter issues:

1. Check the terminal for error messages
2. Verify all environment variables are set
3. Ensure MySQL is running (for local development)
4. Check Twilio account status for WhatsApp
5. Review logs at http://127.0.0.1:8000/docs for API testing

---

**Application is ready to use! 🎉**

Start the server and visit http://127.0.0.1:8000 to begin.
