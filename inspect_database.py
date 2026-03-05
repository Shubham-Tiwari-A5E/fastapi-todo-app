#!/usr/bin/env python3
"""
Database Schema Inspector
Checks current database schema and migration status
"""

import os
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from sqlalchemy import create_engine, text, inspect

def get_database_url():
    """Get database URL from environment"""
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        # Build from components
        host = os.getenv("DATABASE_HOST", "localhost")
        user = os.getenv("DATABASE_USER", "root")
        password = os.getenv("DATABASE_PASSWORD", "")
        database = os.getenv("DATABASE_NAME", "todos")
        
        database_url = f"mysql+pymysql://{user}:{password}@{host}/{database}"
    
    # Fix postgres URL
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql+psycopg://", 1)
    elif database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    
    return database_url

def check_database_schema():
    """Check and display current database schema"""
    try:
        database_url = get_database_url()
        db_type = "PostgreSQL" if "postgresql" in database_url else "MySQL"
        
        print("\n" + "=" * 60)
        print(f"🔍 DATABASE SCHEMA INSPECTOR ({db_type})")
        print("=" * 60)
        
        engine = create_engine(database_url)
        inspector = inspect(engine)
        
        # Get all tables
        tables = inspector.get_table_names()
        print(f"\n📊 Tables found: {len(tables)}")
        
        for table_name in tables:
            print(f"\n📋 Table: {table_name}")
            print("-" * 60)
            
            # Get columns
            columns = inspector.get_columns(table_name)
            print(f"   Columns ({len(columns)}):")
            for col in columns:
                nullable = "NULL" if col['nullable'] else "NOT NULL"
                default = f" DEFAULT {col['default']}" if col['default'] else ""
                print(f"      • {col['name']:<25} {str(col['type']):<20} {nullable}{default}")
            
            # Get primary keys
            pk = inspector.get_pk_constraint(table_name)
            if pk and pk['constrained_columns']:
                print(f"   Primary Key: {', '.join(pk['constrained_columns'])}")
            
            # Get foreign keys
            fks = inspector.get_foreign_keys(table_name)
            if fks:
                print(f"   Foreign Keys ({len(fks)}):")
                for fk in fks:
                    print(f"      • {fk['constrained_columns']} → {fk['referred_table']}.{fk['referred_columns']}")
        
        # Check migration version
        print("\n" + "=" * 60)
        print("📌 MIGRATION STATUS")
        print("=" * 60)
        
        if 'alembic_version' in tables:
            with engine.connect() as conn:
                result = conn.execute(text("SELECT version_num FROM alembic_version"))
                version = result.fetchone()
                if version:
                    print(f"\n✅ Current Version: {version[0]}")
                else:
                    print("\n⚠️  alembic_version table exists but is empty")
        else:
            print("\n❌ alembic_version table not found (migrations never run)")
        
        print("\n" + "=" * 60)
        print("✅ INSPECTION COMPLETE")
        print("=" * 60 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_specific_columns():
    """Check for specific columns that were causing issues"""
    try:
        database_url = get_database_url()
        engine = create_engine(database_url)
        inspector = inspect(engine)
        
        print("\n" + "=" * 60)
        print("🔎 CHECKING NOTIFICATION COLUMNS")
        print("=" * 60)
        
        if 'todos' not in inspector.get_table_names():
            print("\n❌ 'todos' table not found!")
            return False
        
        columns = inspector.get_columns('todos')
        column_names = [col['name'] for col in columns]
        
        required = ['notification_sent', 'notification_enabled']
        
        print("\nRequired columns:")
        for col_name in required:
            if col_name in column_names:
                col_info = next(c for c in columns if c['name'] == col_name)
                print(f"   ✅ {col_name:<25} {col_info['type']}")
            else:
                print(f"   ❌ {col_name:<25} MISSING!")
        
        print("\n" + "=" * 60 + "\n")
        
        return all(col in column_names for col in required)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def main():
    """Main function"""
    print("\n🔧 FastAPI Todo App - Database Inspector")
    
    if not check_database_schema():
        sys.exit(1)
    
    if not check_specific_columns():
        print("⚠️  Some required columns are missing!")
        print("💡 Run: python run_migrations.py")
        sys.exit(1)
    
    print("✅ All checks passed!")
    sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏸️  Interrupted by user")
        sys.exit(130)
