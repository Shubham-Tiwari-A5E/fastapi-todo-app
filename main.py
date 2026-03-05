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
    print("=" * 60)
    print("🔄 Running database migrations...")
    print("=" * 60)

    try:
        from alembic.config import Config
        from alembic import command

        # Get the directory where main.py is located
        base_dir = os.path.dirname(os.path.abspath(__file__))
        alembic_ini_path = os.path.join(base_dir, "alembic.ini")

        print(f"📁 Base directory: {base_dir}")
        print(f"📁 Alembic config: {alembic_ini_path}")

        # Create Alembic config
        alembic_cfg = Config(alembic_ini_path)

        # Set the script location
        alembic_cfg.set_main_option("script_location", os.path.join(base_dir, "alembic"))

        print("🚀 Starting migration...")

        # Run migrations
        command.upgrade(alembic_cfg, "head")

        print("=" * 60)
        print("✅ Database migrations completed successfully!")
        print("=" * 60)

    except Exception as e:
        print("=" * 60)
        print(f"❌ Migration error: {type(e).__name__}")
        print(f"❌ Error details: {str(e)}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        print("=" * 60)
        print("⚠️  App will continue but database may not be ready")
        print("⚠️  Check DATABASE_URL environment variable is set")
        print("=" * 60)

    # Check database connection
    try:
        check_database_connection()
        print("✅ Database connection successful!")
    except Exception as e:
        print(f"⚠️ Database connection check failed: {e}")

    # Small delay to ensure database is fully ready after migrations
    import asyncio
    await asyncio.sleep(2)

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

