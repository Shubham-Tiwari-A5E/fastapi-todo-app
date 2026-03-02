# 🚀 Render.com Deployment Guide

## Problem Encountered
Your app deployed successfully but can't connect to MySQL on `localhost` because Render doesn't provide a local MySQL server.

## ✅ Solution: Use External MySQL Database

### Option 1: Free MySQL Providers (Recommended for Testing)

#### 1. **Aiven** (Best Free Option)
- Website: https://aiven.io
- Free tier: 1GB storage, 1 vCPU
- Steps:
  1. Sign up for free account
  2. Create MySQL service
  3. Copy connection details
  4. Add to Render environment variables

#### 2. **PlanetScale** (Developer-Friendly)
- Website: https://planetscale.com
- Free tier: 5GB storage, 1 billion row reads/month
- Serverless MySQL compatible with standard MySQL clients

#### 3. **Railway** (MySQL + Hosting)
- Website: https://railway.app
- Free tier includes MySQL
- Alternative to Render

### Option 2: Use Render PostgreSQL (Recommended)

Render provides free PostgreSQL! Let me update your code to support PostgreSQL:

---

## 🔧 Updated Code (Already Applied)

Your code has been updated to use environment variables:

```python
# database.py now uses:
DATABASE_HOST=your-mysql-host.com
DATABASE_USER=your-username
DATABASE_PASSWORD=your-password
DATABASE_NAME=todos
DATABASE_PORT=3306
```

---

## 📝 Render Configuration

### Step 1: Add MySQL Database to Render

**Option A: Use External MySQL (Aiven/PlanetScale)**

1. **Get MySQL from Aiven** (Free):
   - Go to https://aiven.io
   - Sign up → Create Service → MySQL
   - Note connection details:
     - Host: `your-service.aivencloud.com`
     - Port: `12345`
     - User: `avnadmin`
     - Password: `your-password`
     - Database: `defaultdb`

2. **Add Environment Variables in Render**:
   - Go to your Render service
   - Click "Environment"
   - Add these variables:
     ```
     DATABASE_HOST=your-service.aivencloud.com
     DATABASE_PORT=12345
     DATABASE_USER=avnadmin
     DATABASE_PASSWORD=your-secure-password
     DATABASE_NAME=defaultdb
     ```

**Option B: Switch to PostgreSQL** (Render's Free Database)

1. **Add PostgreSQL in Render**:
   - Dashboard → New → PostgreSQL
   - Select Free plan
   - Copy Internal Database URL

2. **Update your code** (I'll help with this below)

---

## 🔄 Option B: Convert to PostgreSQL (Recommended)

Since Render provides free PostgreSQL, let's use that!

### 1. Update requirements.txt

```txt
# Replace pymysql with:
psycopg2-binary==2.9.9

# Keep everything else the same
fastapi==0.128.1
uvicorn==0.40.0
sqlalchemy==2.0.36
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.20
jinja2==3.1.5
alembic==1.14.0
pytest==9.0.2
httpx==0.28.1
requests==2.32.5
pydantic==2.12.5
pydantic-core==2.41.5
cryptography==44.0.0
```

### 2. Update database.py

```python
# Change from:
database_url = f"mysql+pymysql://..."

# To:
database_url = os.getenv("DATABASE_URL", "sqlite:///./todos.db")
# Render provides DATABASE_URL automatically for PostgreSQL
```

### 3. In Render Dashboard:
- Create PostgreSQL database (free)
- Copy the Internal Database URL
- It will automatically be available as `DATABASE_URL` env var

---

## 🛠️ Quick Fix Steps

### Immediate Solution (Keep MySQL):

1. **Get Free MySQL from Aiven**:
   ```
   https://aiven.io/free-mysql-database
   ```

2. **Set Environment Variables in Render**:
   ```
   DATABASE_HOST=xxx.aivencloud.com
   DATABASE_PORT=12345
   DATABASE_USER=avnadmin
   DATABASE_PASSWORD=your-password
   DATABASE_NAME=defaultdb
   ```

3. **Redeploy** (automatic after adding env vars)

### Better Solution (Use PostgreSQL):

1. **Create PostgreSQL in Render**:
   - New → PostgreSQL → Free plan
   - Name it `todos-db`
   - Copy Internal Database URL

2. **Update 2 files** (instructions below)

3. **Set DATABASE_URL in Render**:
   - Already auto-set by Render PostgreSQL
   - Just redeploy

---

## 📋 Files to Update for PostgreSQL

### File 1: requirements.txt
Remove: `pymysql==1.1.1`
Add: `psycopg2-binary==2.9.9`

### File 2: database.py
```python
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Use DATABASE_URL from environment (Render provides this)
database_url = os.getenv(
    "DATABASE_URL",
    "sqlite:///./todos.db"  # Local fallback
)

# Fix for Render's postgres:// URL (needs postgresql://)
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

### File 3: models.py
Change String lengths for PostgreSQL compatibility:
```python
# Change:
Column(String(36), ...)
# To:
Column(String(255), ...)  # PostgreSQL friendly
```

---

## 🚀 Deployment Checklist

### For MySQL (Current Setup):
- [ ] Get MySQL from Aiven/PlanetScale
- [ ] Add 5 environment variables to Render
- [ ] Redeploy app
- [ ] Check logs: Should see "✅ Database connection successful!"

### For PostgreSQL (Recommended):
- [ ] Create PostgreSQL in Render
- [ ] Update requirements.txt
- [ ] Update database.py
- [ ] Commit and push changes
- [ ] Render auto-deploys
- [ ] Check logs

---

## 🔍 Troubleshooting

### Check Logs in Render:
```bash
# Look for:
✅ Database connection successful!  # Good!
⚠️ Database connection failed: ...   # Problem
```

### Test Database Connection:
Visit: `https://your-app.onrender.com/health`

Should return:
```json
{
  "status": "healthy",
  "service": "FastAPI Todo App",
  "database": "your-db-host.com"
}
```

### Common Issues:

1. **"Connection refused"** - Missing env variables
   - Solution: Add DATABASE_HOST, DATABASE_USER, etc.

2. **"Authentication failed"** - Wrong password
   - Solution: Check password in Aiven/Render dashboard

3. **"Database not found"** - Wrong database name
   - Solution: Use exact name from provider

---

## 💡 Recommended Path Forward

**Best Option**: Use Render PostgreSQL (Free & Simple)

1. I'll update your code for PostgreSQL
2. You create PostgreSQL in Render
3. Push updated code
4. Done! ✅

**Alternative**: Keep MySQL with Aiven

1. Get free MySQL from Aiven
2. Add 5 environment variables
3. Redeploy
4. Done! ✅

---

## 📞 Need Help?

Reply with:
- "Use PostgreSQL" - I'll update all files
- "Use MySQL" - I'll guide you through Aiven setup
- "Show me env variables" - I'll list exact values needed

---

## 🎯 Quick Commands

### Check Render Logs:
```bash
# In Render dashboard → Logs tab
# Or use Render CLI:
render logs -t fastapi-deployement-915m
```

### Test Locally with Env Vars:
```bash
# Windows PowerShell
$env:DATABASE_HOST="your-host.com"
$env:DATABASE_USER="user"
$env:DATABASE_PASSWORD="pass"
$env:DATABASE_NAME="todos"
uvicorn main:app --reload
```

---

**Your app is running! It just needs a database connection. Let me know which option you prefer and I'll help you complete the setup!** 🚀
