import os
import sys
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

def check_migration_needed():
    """Check if migrations need to be run by comparing current vs head revision"""
    try:
        from alembic.config import Config
        from alembic.script import ScriptDirectory
        from alembic.runtime.migration import MigrationContext
        from sqlalchemy import create_engine
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        alembic_ini_path = os.path.join(base_dir, "alembic.ini")
        alembic_cfg = Config(alembic_ini_path)
        alembic_cfg.set_main_option("script_location", os.path.join(base_dir, "alembic"))
        
        # Get database URL
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            database_url = alembic_cfg.get_main_option("sqlalchemy.url")
        
        # Fix postgres:// to postgresql+psycopg://
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql+psycopg://", 1)
        elif database_url.startswith("postgresql://"):
            database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)
        
        engine = create_engine(database_url)
        
        # Get current revision from database
        with engine.connect() as conn:
            context = MigrationContext.configure(conn)
            current_rev = context.get_current_revision()
        
        # Get head revision from scripts
        script = ScriptDirectory.from_config(alembic_cfg)
        head_rev = script.get_current_head()
        
        logger.info(f"📊 Current DB revision: {current_rev or 'None (fresh database)'}")
        logger.info(f"📊 Latest available revision: {head_rev}")
        
        return current_rev != head_rev, current_rev, head_rev
        
    except Exception as e:
        logger.warning(f"⚠️ Could not check migration status: {e}")
        return True, None, None  # Assume migration needed if we can't check

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    logger.info("=" * 60)
    logger.info("� FASTAPI TODO APP - STARTUP")
    logger.info("=" * 60)
    logger.info(f"📍 Environment: {'Production' if os.getenv('DATABASE_URL') else 'Development'}")
    logger.info(f"🐍 Python version: {sys.version.split()[0]}")
    
    logger.info("\n" + "=" * 60)
    logger.info("�🔄 Checking database migrations...")
    logger.info("=" * 60)

    try:
        # Check if migration is actually needed
        needs_migration, current_rev, head_rev = check_migration_needed()
        
        if not needs_migration:
            logger.info("✅ Database is up to date (no migrations needed)")
        else:
            logger.info("🚀 Applying database migrations...")
            
            from alembic.config import Config
            from alembic import command

            # Get the directory where main.py is located
            base_dir = os.path.dirname(os.path.abspath(__file__))
            alembic_ini_path = os.path.join(base_dir, "alembic.ini")

            alembic_cfg = Config(alembic_ini_path)
            alembic_cfg.set_main_option("script_location", os.path.join(base_dir, "alembic"))

            # Run migration
            command.upgrade(alembic_cfg, "head")

            logger.info("=" * 60)
            logger.info("✅ Database migrations completed successfully!")
            logger.info("=" * 60)

    except Exception as e:
        logger.error(f"❌ Migration error: {type(e).__name__}: {str(e)}")
        logger.warning("⚠️  Attempting automatic database recovery...")
        
        # For fresh database, create tables using SQLAlchemy
        try:
            from models import Base
            from database import engine
            
            logger.info("🛠️  Creating database tables from models...")
            Base.metadata.create_all(bind=engine)
            logger.info("✅ Tables created successfully!")
            
            # Now try migrations again
            try:
                from alembic.config import Config
                from alembic import command
                base_dir = os.path.dirname(os.path.abspath(__file__))
                alembic_ini_path = os.path.join(base_dir, "alembic.ini")
                alembic_cfg = Config(alembic_ini_path)
                alembic_cfg.set_main_option("script_location", os.path.join(base_dir, "alembic"))
                
                # Stamp the database as being at the latest revision
                command.stamp(alembic_cfg, "head")
                logger.info("✅ Database stamped with current migration version")
            except Exception as stamp_error:
                logger.warning(f"⚠️  Could not stamp database: {stamp_error}")
            
        except Exception as create_error:
            logger.error(f"❌ Table creation failed: {create_error}")
            
            # Fallback: run manual database fix
            try:
                from fix_database import fix_database
                logger.info("🔧 Running manual schema fix...")
                fix_database()
                logger.info("✅ Manual database fix completed successfully!")
            except Exception as fix_error:
                logger.error(f"❌ Manual fix also failed: {fix_error}")
                logger.error("⚠️  Database may not be fully initialized - app will continue but may have errors")

    try:
        check_database_connection()
        logger.info("✅ Database connection successful!")
    except Exception as e:
        logger.error(f"⚠️ Database connection check failed: {e}")

    import asyncio
    logger.info("⏳ Waiting for database to stabilize...")
    await asyncio.sleep(3)

    try:
        await notification_scheduler.start()
        logger.info("✅ WhatsApp notification scheduler started")
    except Exception as e:
        logger.warning(f"⚠️ Notification scheduler failed: {e}")

    logger.info("\n" + "=" * 60)
    logger.info("✅ STARTUP COMPLETE - Application Ready!")
    logger.info("=" * 60 + "\n")

    yield  # Application runs

    # Shutdown
    logger.info("\n" + "=" * 60)
    logger.info("👋 SHUTTING DOWN...")
    logger.info("=" * 60)
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

