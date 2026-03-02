from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
import os
from models import Base

# Use DATABASE_URL from environment (Render PostgreSQL provides this automatically)
# Falls back to local MySQL for development
database_url = os.getenv("DATABASE_URL")

if database_url:
    # Fix for Render's postgres:// URL (SQLAlchemy needs postgresql://)
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    print(f"🔗 Using external database")
else:
    # Local development fallback
    database_name = os.getenv("DATABASE_NAME", "todos")
    database_user = os.getenv("DATABASE_USER", "root")
    database_password = os.getenv("DATABASE_PASSWORD", "raj1234")
    database_host = os.getenv("DATABASE_HOST", "localhost")
    database_port = os.getenv("DATABASE_PORT", "3306")
    database_url = f"mysql+pymysql://{database_user}:{database_password}@{database_host}:{database_port}/{database_name}"
    print(f"🔗 Using local MySQL: {database_host}")

engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_database_if_not_exists():
    """Only works for MySQL local development"""
    if "mysql" in database_url:
        try:
            import pymysql
            connection = pymysql.connect(
                host=os.getenv("DATABASE_HOST", "localhost"),
                user=os.getenv("DATABASE_USER", "root"),
                password=os.getenv("DATABASE_PASSWORD", "raj1234")
            )
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('DATABASE_NAME', 'todos')}")
            connection.commit()
            cursor.close()
            connection.close()
            print(f"✅ Database '{os.getenv('DATABASE_NAME', 'todos')}' created or already exists.")
        except Exception as e:
            print(f"⚠️ Error creating database: {e}")
    else:
        print("ℹ️ Using external database (PostgreSQL), skipping database creation")

def check_database_connection():
    try:
        create_database_if_not_exists()
        Base.metadata.create_all(bind=engine)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            result.fetchone()
        print("✅ Database connection successful!")
    except OperationalError as e:
        print(f"❌ Database connection failed: {e}")
        raise
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise
