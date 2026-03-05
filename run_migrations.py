#!/usr/bin/env python3
"""
Manual Migration Runner
Run this script to manually apply pending database migrations
Usage: python run_migrations.py
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  python-dotenv not installed")

def check_migration_status():
    """Check and display current migration status"""
    try:
        from alembic.config import Config
        from alembic.script import ScriptDirectory
        from alembic.runtime.migration import MigrationContext
        from sqlalchemy import create_engine
        
        print("\n" + "=" * 60)
        print("📊 CHECKING MIGRATION STATUS")
        print("=" * 60)
        
        alembic_ini_path = project_root / "alembic.ini"
        alembic_cfg = Config(str(alembic_ini_path))
        alembic_cfg.set_main_option("script_location", str(project_root / "alembic"))
        
        # Get database URL
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            database_url = alembic_cfg.get_main_option("sqlalchemy.url")
        
        print(f"🔗 Database: {database_url.split('@')[1] if '@' in database_url else 'localhost'}")
        
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
        
        print(f"\n📌 Current DB Revision: {current_rev or '❌ None (fresh database)'}")
        print(f"📌 Latest Available:    {head_rev}")
        
        if current_rev == head_rev:
            print("\n✅ Database is UP TO DATE - No migrations needed!")
            return False
        else:
            print("\n⚠️  Database is OUTDATED - Migrations pending!")
            
            # List pending migrations
            print("\n📋 Pending migrations:")
            for rev in script.iterate_revisions(head_rev, current_rev or "base"):
                if rev.revision != current_rev:
                    print(f"   • {rev.revision[:8]}: {rev.doc or 'No description'}")
            
            return True
        
    except Exception as e:
        print(f"\n❌ Error checking migration status: {e}")
        import traceback
        traceback.print_exc()
        return None

def run_migrations():
    """Run pending migrations"""
    try:
        from alembic.config import Config
        from alembic import command
        
        print("\n" + "=" * 60)
        print("🚀 RUNNING MIGRATIONS")
        print("=" * 60 + "\n")
        
        alembic_ini_path = project_root / "alembic.ini"
        alembic_cfg = Config(str(alembic_ini_path))
        alembic_cfg.set_main_option("script_location", str(project_root / "alembic"))
        
        # Run upgrade to head
        command.upgrade(alembic_cfg, "head")
        
        print("\n" + "=" * 60)
        print("✅ MIGRATIONS COMPLETED SUCCESSFULLY!")
        print("=" * 60 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    print("\n" + "=" * 60)
    print("🔧 FASTAPI TODO APP - MIGRATION TOOL")
    print("=" * 60)
    
    # Check status first
    needs_migration = check_migration_status()
    
    if needs_migration is None:
        print("\n❌ Cannot proceed - status check failed")
        sys.exit(1)
    
    if not needs_migration:
        print("\n✅ No action needed")
        sys.exit(0)
    
    # Ask for confirmation
    print("\n" + "-" * 60)
    response = input("Do you want to run migrations now? (yes/no): ").strip().lower()
    
    if response in ['yes', 'y']:
        success = run_migrations()
        
        if success:
            # Check status again to confirm
            print("\n🔍 Verifying migration status...")
            check_migration_status()
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        print("\n⏸️  Migration cancelled")
        sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏸️  Interrupted by user")
        sys.exit(130)
