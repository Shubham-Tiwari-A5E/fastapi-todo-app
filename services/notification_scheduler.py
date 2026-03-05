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
        print(f"🔄 Reminder check loop started - will check every 60 seconds")
        check_count = 0

        while self.running:
            try:
                check_count += 1
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"🔍 Check #{check_count} at {current_time}")
                await self._check_and_send_reminders()
            except Exception as e:
                print(f"❌ Error in reminder check: {e}")
                import traceback
                traceback.print_exc()

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

            print(f"⏰ Current time: {now.strftime('%H:%M:%S')}")
            print(f"🔍 Looking for tasks between {reminder_start.strftime('%H:%M:%S')} and {reminder_end.strftime('%H:%M:%S')}")

            # Find todos that:
            # 1. Are not completed
            # 2. Have task_time set
            # 3. Have notifications enabled
            # 4. Notification not already sent
            # 5. task_time is between 9.5 and 10.5 minutes from now
            # 6. User has phone number

            todos_to_notify = db.query(Todo).join(User).filter(
                Todo.isCompleted == False,
                Todo.task_time.isnot(None),
                Todo.notification_enabled == True,
                Todo.notification_sent == False,  # Only send once
                Todo.task_time >= reminder_start,
                Todo.task_time <= reminder_end,
                User.phone_number.isnot(None)
            ).all()

            # Also log all upcoming tasks (for debugging)
            all_upcoming = db.query(Todo).join(User).filter(
                Todo.isCompleted == False,
                Todo.task_time.isnot(None),
                Todo.task_time >= now,
                User.phone_number.isnot(None)
            ).all()

            if all_upcoming:
                print(f"📋 Total upcoming tasks with phone numbers: {len(all_upcoming)}")
                for task in all_upcoming[:5]:  # Show first 5
                    minutes_until = (task.task_time - now).total_seconds() / 60
                    print(f"   - '{task.title}' at {task.task_time.strftime('%H:%M')} (in {minutes_until:.1f} min) | Notify: {task.notification_enabled} | Sent: {task.notification_sent}")

            if todos_to_notify:
                print(f"📬 Found {len(todos_to_notify)} todos needing reminders NOW!")

            for todo in todos_to_notify:
                print(f"📤 Sending reminder for: {todo.title} (scheduled at {todo.task_time.strftime('%H:%M')})")

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
                    # Mark notification as sent
                    todo.notification_sent = True
                    db.commit()
                    print(f"✅ Reminder sent for task: {todo.title}")
                else:
                    print(f"⚠️ Failed to send reminder for task: {todo.title}")

                # Small delay between messages to avoid rate limiting
                await asyncio.sleep(1)

            if not todos_to_notify and not all_upcoming:
                print("💤 No tasks with reminders scheduled")

        except Exception as e:
            print(f"❌ Error checking reminders: {e}")
            import traceback
            traceback.print_exc()

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
