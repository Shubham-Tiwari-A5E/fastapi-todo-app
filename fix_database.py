"""
Database Fix Script - Adds phone_number, task_time, and notification_enabled fields
Run this if migrations didn't apply properly
"""

import pymysql
import sys

# Database configuration
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "raj1234"
DB_NAME = "todos"

def fix_database():
    print("🔧 Fixing database schema...")

    try:
        # Connect to database
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()

        print(f"✅ Connected to database: {DB_NAME}")

        # Check and add phone_number to users table
        print("\n📱 Checking users table...")
        cursor.execute("SHOW COLUMNS FROM users LIKE 'phone_number'")
        if not cursor.fetchone():
            print("  Adding phone_number column...")
            cursor.execute("ALTER TABLE users ADD COLUMN phone_number VARCHAR(20) NULL")
            print("  ✅ phone_number column added!")
        else:
            print("  ✅ phone_number column already exists")

        # Check and add task_time to todos table
        print("\n⏰ Checking todos table for task_time...")
        cursor.execute("SHOW COLUMNS FROM todos LIKE 'task_time'")
        if not cursor.fetchone():
            print("  Adding task_time column...")
            cursor.execute("ALTER TABLE todos ADD COLUMN task_time DATETIME NULL")
            print("  ✅ task_time column added!")
        else:
            print("  ✅ task_time column already exists")

        # Check and add notification_enabled to todos table
        print("\n🔔 Checking todos table for notification_enabled...")
        cursor.execute("SHOW COLUMNS FROM todos LIKE 'notification_enabled'")
        if not cursor.fetchone():
            print("  Adding notification_enabled column...")
            cursor.execute("ALTER TABLE todos ADD COLUMN notification_enabled BOOLEAN DEFAULT TRUE")
            print("  ✅ notification_enabled column added!")
        else:
            print("  ✅ notification_enabled column already exists")

        # Update existing todos to have notification_enabled = TRUE
        print("\n🔄 Updating existing todos...")
        cursor.execute("UPDATE todos SET notification_enabled = TRUE WHERE notification_enabled IS NULL")
        affected = cursor.rowcount
        print(f"  ✅ Updated {affected} todos with notification_enabled=TRUE")

        # Commit changes
        conn.commit()

        # Show final schema
        print("\n📊 Final Users Table Structure:")
        cursor.execute("DESCRIBE users")
        for col in cursor.fetchall():
            print(f"  - {col[0]}: {col[1]}")

        print("\n📊 Final Todos Table Structure:")
        cursor.execute("DESCRIBE todos")
        for col in cursor.fetchall():
            print(f"  - {col[0]}: {col[1]}")

        cursor.close()
        conn.close()

        print("\n✅ Database fix completed successfully!")
        print("\n🚀 You can now:")
        print("  1. Restart your FastAPI server")
        print("  2. Register with a phone number")
        print("  3. Receive WhatsApp notifications!")

        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease check:")
        print("  - MySQL is running")
        print("  - Database 'todos' exists")
        print("  - Credentials are correct")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("DATABASE FIX SCRIPT")
    print("=" * 60)

    success = fix_database()

    if not success:
        sys.exit(1)
