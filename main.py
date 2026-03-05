import os

# Try to load .env file for local development (optional)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  python-dotenv not installed, using environment variables only")
    pass

from fastapi import FastAPI, Request
from database import check_database_connection
from routes.todoRoutes import router as todo_router
from users import router as user_router
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from services.notification_scheduler import notification_scheduler

app = FastAPI(
    title="FastAPI Todo App with WhatsApp Notifications",
    description="Production-ready Todo application with authentication and WhatsApp reminders",
    version="2.0.0"
)

@app.on_event("startup")
async def startup_event():
    # Run database migrations automatically on startup
    print("🔄 Running database migrations...")
    try:
        from alembic.config import Config
        from alembic import command

        # Get the directory where main.py is located
        base_dir = os.path.dirname(os.path.abspath(__file__))
        alembic_cfg = Config(os.path.join(base_dir, "alembic.ini"))

        # Set the script location to the alembic directory
        alembic_cfg.set_main_option("script_location", os.path.join(base_dir, "alembic"))

        # Run migrations
        command.upgrade(alembic_cfg, "head")
        print("✅ Database migrations completed successfully!")
    except Exception as e:
        print(f"⚠️ Migration error: {e}")
        print("⚠️ Continuing anyway - tables may already exist")

    # Check database connection
    try:
        check_database_connection()
        print("✅ Database connection successful!")
    except Exception as e:
        print(f"⚠️ Database connection failed: {e}")
        print("⚠️ App will start but database operations will fail")

    # Start notification scheduler
    try:
        await notification_scheduler.start()
        print("✅ WhatsApp notification scheduler started")
    except Exception as e:
        print(f"⚠️ Notification scheduler failed to start: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    # Stop notification scheduler
    await notification_scheduler.stop()
    print("👋 App shutting down...")

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user_router)
app.include_router(todo_router)

# Health check endpoint for Render
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "FastAPI Todo App",
        "database": os.getenv("DATABASE_HOST", "localhost")
    }

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/dashboard")
async def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

