"""
WhatsApp Notification Service using Twilio
Get free trial account at: https://www.twilio.com/try-twilio
Free trial includes $15 credit for testing
"""

import os
from datetime import datetime

# Try to import Twilio - gracefully handle if not available (e.g., Python 3.14 compatibility)
try:
    from twilio.rest import Client
    TWILIO_AVAILABLE = True
except (ImportError, AttributeError) as e:
    print(f"⚠️ Twilio not available: {e}")
    print("ℹ️ WhatsApp notifications will be disabled")
    TWILIO_AVAILABLE = False
    Client = None

class WhatsAppService:
    def __init__(self):
        # Get credentials from environment variables
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.whatsapp_from = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")  # Twilio sandbox

        # Initialize client if credentials are available
        self.client = None
        self.enabled = False

        if not TWILIO_AVAILABLE:
            print("ℹ️ WhatsApp service disabled (Twilio not available)")
            return

        if self.account_sid and self.auth_token:
            try:
                self.client = Client(self.account_sid, self.auth_token)
                self.enabled = True
                print("✅ WhatsApp service initialized")
            except Exception as e:
                print(f"⚠️ WhatsApp service initialization failed: {e}")
                self.enabled = False
        else:
            print("ℹ️ WhatsApp service disabled (no credentials)")

    def send_welcome_message(self, phone_number: str, user_name: str) -> bool:
        """
        Send beautiful welcome message to new user
        Phone number must be in format: +919876543210
        """
        if not self.enabled:
            print("⚠️ WhatsApp service not enabled")
            return False

        if not phone_number:
            print("⚠️ No phone number provided")
            return False

        try:
            # Format phone number for WhatsApp
            if not phone_number.startswith("whatsapp:"):
                phone_number = f"whatsapp:{phone_number}"

            message = f"""🎉 *Welcome to Shubham's Todo App!*

Hello *{user_name}*! 👋

We're thrilled to have you on board! 🚀

━━━━━━━━━━━━━━━━━━━━━━
✨ *What Makes Us Special?*
━━━━━━━━━━━━━━━━━━━━━━

📝 *Smart Task Management*
   Create, organize, and track your tasks effortlessly

⏰ *Never Miss Important Things*
   Get WhatsApp reminders 10 minutes before each task

🔔 *Stay On Top of Your Life*
   We'll keep you reminded of what matters most

✅ *Track Your Progress*
   Mark tasks complete and see your achievements

🎯 *Priority System*
   Focus on what's important with our 5-level priority system

━━━━━━━━━━━━━━━━━━━━━━
💡 *Pro Tip:*
━━━━━━━━━━━━━━━━━━━━━━

Set task times to receive automatic WhatsApp notifications! We'll remind you 10 minutes before so you never miss important tasks.

━━━━━━━━━━━━━━━━━━━━━━

🌟 Ready to boost your productivity?
Let's make every task count!

_Start managing your tasks now and experience the power of staying organized!_

━━━━━━━━━━━━━━━━━━━━━━
With love from Shubham's Team ❤️
━━━━━━━━━━━━━━━━━━━━━━"""

            result = self.client.messages.create(
                body=message,
                from_=self.whatsapp_from,
                to=phone_number
            )

            print(f"✅ Welcome message sent to {phone_number}: {result.sid}")
            return True

        except Exception as e:
            print(f"❌ Failed to send welcome message: {e}")
            return False

    def send_task_reminder(self, phone_number: str, task_title: str, task_description: str, task_time: datetime, user_name: str, priority: int) -> bool:
        """
        Send beautiful task reminder 10 minutes before task time with full details
        Note: task_time is already in local time (not UTC) as per our timezone fix
        """
        if not self.enabled:
            print("⚠️ WhatsApp service not enabled")
            return False

        if not phone_number:
            print("⚠️ No phone number provided")
            return False

        try:
            # Format phone number for WhatsApp
            if not phone_number.startswith("whatsapp:"):
                phone_number = f"whatsapp:{phone_number}"

            # Format task time (task_time is in local time, not UTC)
            time_str = task_time.strftime("%I:%M %p")
            date_str = task_time.strftime("%B %d, %Y")
            day_str = task_time.strftime("%A")

            # Priority emoji
            priority_emojis = {
                1: "🟢",  # Lowest
                2: "🟡",  # Low
                3: "🟠",  # Medium
                4: "🔴",  # High
                5: "🔥"   # Highest
            }
            priority_emoji = priority_emojis.get(priority, "⭐")

            # Build message with description if available
            message = f"""⏰ *TASK REMINDER!*

Hi *{user_name}*! 

🔔 Your task is coming up in *10 minutes*

━━━━━━━━━━━━━━━━━━━━━━
📋 *TASK DETAILS*
━━━━━━━━━━━━━━━━━━━━━━

{priority_emoji} *Title:* {task_title}

📅 *Date:* {day_str}, {date_str}
⏰ *Time:* {time_str}
🎯 *Priority:* Level {priority}"""

            if task_description:
                message += f"""

📝 *Description:*
{task_description}"""

            message += """

━━━━━━━━━━━━━━━━━━━━━━

✅ Don't forget to complete it!
💪 You've got this!

━━━━━━━━━━━━━━━━━━━━━━
_From Shubham's Todo App_
━━━━━━━━━━━━━━━━━━━━━━

_Reply STOP to unsubscribe from reminders_"""

            result = self.client.messages.create(
                body=message,
                from_=self.whatsapp_from,
                to=phone_number
            )

            print(f"✅ Task reminder sent to {phone_number}: {result.sid}")
            return True

        except Exception as e:
            print(f"❌ Failed to send task reminder: {e}")
            return False

    def send_test_message(self, phone_number: str) -> bool:
        """
        Send test message to verify WhatsApp connection
        """
        if not self.enabled:
            return False

        try:
            if not phone_number.startswith("whatsapp:"):
                phone_number = f"whatsapp:{phone_number}"

            message = "✅ Your WhatsApp is connected! You'll now receive task reminders."

            result = self.client.messages.create(
                body=message,
                from_=self.whatsapp_from,
                to=phone_number
            )

            print(f"✅ Test message sent: {result.sid}")
            return True

        except Exception as e:
            print(f"❌ Test message failed: {e}")
            return False


# Global instance
whatsapp_service = WhatsAppService()


