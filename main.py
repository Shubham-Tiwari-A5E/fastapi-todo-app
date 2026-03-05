import os
import logging
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    logger.warning("python-dotenv not installed, using environment variables only")

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from database import check_database_connection
from routes.todoRoutes import router as todo_router
from users import router as user_router
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from services.notification_scheduler import notification_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    logger.info("=" * 60)
    logger.info("🔄 Running database migrations...")
    logger.info("=" * 60)

    try:
        from alembic.config import Config
        from alembic import command

        # Get the directory where main.py is located
        base_dir = os.path.dirname(os.path.abspath(__file__))
        alembic_ini_path = os.path.join(base_dir, "alembic.ini")

        logger.info(f"📁 Base directory: {base_dir}")
        logger.info(f"📁 Alembic config: {alembic_ini_path}")

        alembic_cfg = Config(alembic_ini_path)
        alembic_cfg.set_main_option("script_location", os.path.join(base_dir, "alembic"))

        logger.info("🚀 Starting migration...")
        command.upgrade(alembic_cfg, "head")

        logger.info("=" * 60)
        logger.info("✅ Database migrations completed successfully!")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"❌ Migration error: {type(e).__name__}: {str(e)}")
        logger.warning("⚠️  App will continue but database may not be ready")

    try:
        check_database_connection()
        logger.info("✅ Database connection successful!")
    except Exception as e:
        logger.error(f"⚠️ Database connection check failed: {e}")

    import asyncio
    logger.info("⏳ Waiting for database to stabilize...")
    await asyncio.sleep(5)

    try:
        await notification_scheduler.start()
        logger.info("✅ WhatsApp notification scheduler started")
    except Exception as e:
        logger.warning(f"⚠️ Notification scheduler failed: {e}")

    yield  # Application runs

    # Shutdown
    logger.info("👋 Shutting down...")
    await notification_scheduler.stop()
    logger.info("✅ Cleanup complete")

# Create FastAPI app with lifespan
app = FastAPI(
    title="FastAPI Todo App",
    description="Production-ready Todo application with authentication and WhatsApp reminders",
    version="3.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure based on your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Gzip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "type": type(exc).__name__}
    )

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user_router)
app.include_router(todo_router)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    try:
        check_database_connection()
        db_status = "connected"
    except:
        db_status = "disconnected"
    
    return {
        "status": "healthy" if db_status == "connected" else "degraded",
        "service": "FastAPI Todo App",
        "version": "3.0.0",
        "database": db_status
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

