"""
Manual Database Fix Script
Run this if migrations fail on production
"""

import os
import sys
from sqlalchemy import create_engine, text

def fix_database():
    """Add missing columns to production database"""
    
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL not set")
        return False
    
    # Fix postgres:// to postgresql+psycopg://
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql+psycopg://", 1)
    elif database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    
    print(f"🔗 Connecting to database...")
    
    try:
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Check if notification_sent column exists
            check_query = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='todos' AND column_name='notification_sent'
            """)
            
            result = conn.execute(check_query)
            exists = result.fetchone()
            
            if not exists:
                print("⚠️  notification_sent column missing, adding it...")
                
                # Add the column with default value
                add_column_query = text("""
                    ALTER TABLE todos 
                    ADD COLUMN IF NOT EXISTS notification_sent BOOLEAN NOT NULL DEFAULT FALSE
                """)
                
                conn.execute(add_column_query)
                conn.commit()
                print("✅ Added notification_sent column")
            else:
                print("✅ notification_sent column already exists")
            
            # Verify notification_enabled column
            check_enabled = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='todos' AND column_name='notification_enabled'
            """)
            
            result = conn.execute(check_enabled)
            enabled_exists = result.fetchone()
            
            if enabled_exists:
                print("✅ notification_enabled column exists")
            else:
                print("⚠️  notification_enabled column missing, adding it...")
                add_enabled_query = text("""
                    ALTER TABLE todos 
                    ADD COLUMN IF NOT EXISTS notification_enabled BOOLEAN NOT NULL DEFAULT TRUE
                """)
                conn.execute(add_enabled_query)
                conn.commit()
                print("✅ Added notification_enabled column")
        
        print("\n✅ Database fix complete!")
        return True
        
    except Exception as e:
        print(f"❌ Database fix error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        fix_database()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
