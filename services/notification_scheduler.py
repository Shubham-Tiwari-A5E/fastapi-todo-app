"""
Background scheduler for sending WhatsApp reminders
Checks every minute for tasks that need reminders
"""

import asyncio
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Todo, User
from services.whatsapp_service import whatsapp_service


class NotificationScheduler:
    def __init__(self):
        self.running = False
        self.task = None

    async def start(self):
        """Start the background scheduler"""
        if self.running:
            print("⚠️ Scheduler already running")
            return

        self.running = True
        self.task = asyncio.create_task(self._check_reminders_loop())
        print("✅ Notification scheduler started")

    async def stop(self):
        """Stop the background scheduler"""
        if not self.running:
            return

        self.running = False
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        print("⏹️ Notification scheduler stopped")

    async def _check_reminders_loop(self):
        """Main loop that checks for reminders every minute"""
        while self.running:
            try:
                await self._check_and_send_reminders()
            except Exception as e:
                print(f"❌ Error in reminder check: {e}")

            # Wait 1 minute before next check
            await asyncio.sleep(60)

    async def _check_and_send_reminders(self):
        """Check database for tasks that need reminders"""
        db = SessionLocal()

        try:
            # Get current time (LOCAL TIME, not UTC since our tasks are stored in local time)
            now = datetime.now()

            # Get time 10 minutes from now (with 1-minute buffer)
            reminder_start = now + timedelta(minutes=9, seconds=30)
            reminder_end = now + timedelta(minutes=10, seconds=30)

            # Find todos that:
            # 1. Are not completed
            # 2. Have task_time set
            # 3. Have notifications enabled
            # 4. task_time is between 9.5 and 10.5 minutes from now
            # 5. User has phone number

            todos_to_notify = db.query(Todo).join(User).filter(
                Todo.isCompleted == False,
                Todo.task_time.isnot(None),
                Todo.notification_enabled == True,
                Todo.task_time >= reminder_start,
                Todo.task_time <= reminder_end,
                User.phone_number.isnot(None)
            ).all()

            if todos_to_notify:
                print(f"📬 Found {len(todos_to_notify)} todos needing reminders at {now.strftime('%Y-%m-%d %H:%M:%S')}")

            for todo in todos_to_notify:
                # Send WhatsApp reminder with full details
                success = whatsapp_service.send_task_reminder(
                    phone_number=todo.user.phone_number,
                    task_title=todo.title,
                    task_description=todo.description or "No description provided",
                    task_time=todo.task_time,
                    user_name=todo.user.name,
                    priority=todo.priority
                )

                if success:
                    print(f"✅ Reminder sent for task: {todo.title}")
                else:
                    print(f"⚠️ Failed to send reminder for task: {todo.title}")

                # Small delay between messages to avoid rate limiting
                await asyncio.sleep(1)

        except Exception as e:
            print(f"❌ Error checking reminders: {e}")

        finally:
            db.close()


# Global scheduler instance
notification_scheduler = NotificationScheduler()


# Helper function to send immediate welcome message
def send_welcome_message_async(phone_number: str, user_name: str):
    """Send welcome message (can be called from sync code)"""
    if phone_number:
        return whatsapp_service.send_welcome_message(phone_number, user_name)
    return False
