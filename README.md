# 📝 FastAPI Todo Application

A modern, production-ready task management application built with FastAPI, featuring real-time WhatsApp notifications, user authentication, and a beautiful responsive interface.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.128+-green.svg)](https://fastapi.tiangolo.com)

## ✨ Features

- 🔐 Secure Authentication - JWT-based with bcrypt
- 📱 WhatsApp Notifications - Automated task reminders  
- 🎨 Modern UI - Responsive design
- ⚡ Real-time Updates - No page reload needed
- 🔔 Smart Reminders - 10-minute advance notifications
- 📊 Task Analytics - Visual statistics
- 🗄️ Database Agnostic - MySQL/PostgreSQL/SQLite
- 🚀 Production Ready - Auto migrations & health checks

## 🚀 Quick Start

### Installation

```bash
# Clone and navigate
cd Todos

# Create virtual environment  
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Start application
python start.py
```

Access at: http://127.0.0.1:8000

## 📋 Environment Setup

Create `.env` file:

```env
# Database
DATABASE_HOST=localhost
DATABASE_USER=root
DATABASE_PASSWORD=yourpass
DATABASE_NAME=todos

# Production: DATABASE_URL=postgresql+psycopg://...

# Security
SECRET_KEY=generate-with-openssl-rand-hex-32

# Twilio WhatsApp (optional)
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_WHATSAPP_NUMBER=+14155238886
```

## 🎯 Usage

```bash
# Development (hot-reload)
python start.py

# Production
python start_prod.py

# Direct uvicorn
uvicorn main:app --reload
```

## 📁 Structure

```
Todos/
├── alembic/         # Database migrations
├── services/        # Core services
├── routes/          # API endpoints
├── static/          # CSS/JS assets
├── templates/       # HTML templates  
├── main.py          # App entry point
├── models.py        # Database models
└── start.py         # Start script
```

## 🔑 API Endpoints

**Auth**
- POST `/register` - Register user
- POST `/token` - Login
- GET `/me` - Current user
- PUT `/me` - Update profile

**Todos**
- GET `/todos` - List todos
- POST `/todos` - Create todo
- PUT `/todos/{id}` - Update todo
- DELETE `/todos/{id}` - Delete todo

## 🧪 Testing

```bash
pytest                    # Run all tests
pytest --cov             # With coverage
```

## 🚀 Deployment

**Render.com:**
- Build: `pip install -r requirements.txt`
- Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## 🔧 Database Migrations

```bash
alembic upgrade head                          # Apply migrations
alembic revision --autogenerate -m "message" # Create migration
alembic downgrade -1                         # Rollback
```

## 📝 License

MIT License - See LICENSE file

---

Made with ❤️ using FastAPI
