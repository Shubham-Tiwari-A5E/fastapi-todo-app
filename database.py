from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
import pymysql
import os
from models import Base

# Use environment variables for production, fallback to local for development
database_name = os.getenv("DATABASE_NAME", "todos")
database_user = os.getenv("DATABASE_USER", "root")
database_password = os.getenv("DATABASE_PASSWORD", "raj1234")
database_host = os.getenv("DATABASE_HOST", "localhost")
database_port = os.getenv("DATABASE_PORT", "3306")

database_url = f"mysql+pymysql://{database_user}:{database_password}@{database_host}:{database_port}/{database_name}"
engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_database_if_not_exists():
    try:
        # Connect to MySQL without specifying database
        connection = pymysql.connect(host='localhost', user='root', password='raj1234')
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        connection.commit()
        cursor.close()
        connection.close()
        print(f"Database '{database_name}' created or already exists.")
    except Exception as e:
        print(f"Error creating database: {e}")

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created.")

def check_database_connection():
    create_database_if_not_exists()
    create_tables()
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("Database connection successful.")
        return True
    except OperationalError as e:
        print(f"Database connection failed: {e}")
        return False
