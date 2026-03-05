"""
Script to fix user passwords that are in wrong hash format
Run this if you have existing users with pbkdf2_sha256 passwords
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

from database import SessionLocal
from models import User
from auth import get_password_hash

def fix_user_passwords():
    """
    This script helps reset passwords for users created with old hash format.
    It will prompt you to set new passwords for each user.
    """
    db = SessionLocal()

    try:
        users = db.query(User).all()

        if not users:
            print("No users found in database.")
            return

        print(f"\n Found {len(users)} user(s) in database.\n")
        print("="*60)
        print("This script will help you reset passwords for users")
        print("who may have incompatible password hashes.")
        print("="*60)

        for user in users:
            print(f"\n📧 User: {user.email}")
            print(f"   Name: {user.name}")

            response = input(f"\n   Reset password for this user? (y/n): ").lower()

            if response == 'y':
                while True:
                    new_password = input("   Enter new password: ")
                    confirm_password = input("   Confirm password: ")

                    if new_password != confirm_password:
                        print("   ❌ Passwords don't match. Try again.")
                        continue

                    if len(new_password) < 6:
                        print("   ❌ Password too short. Minimum 6 characters.")
                        continue

                    # Hash the new password
                    user.password_hash = get_password_hash(new_password)
                    db.commit()

                    print(f"   ✅ Password updated for {user.email}")
                    break
            else:
                print("   ⏭️  Skipped")

        print("\n" + "="*60)
        print("✅ Password reset complete!")
        print("="*60)

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  Password Reset Tool")
    print("="*60)

    response = input("\n⚠️  This will allow you to reset user passwords.\n   Continue? (y/n): ").lower()

    if response == 'y':
        fix_user_passwords()
    else:
        print("\n❌ Cancelled.")
