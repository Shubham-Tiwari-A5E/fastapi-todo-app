"""
WhatsApp Notification Service using Twilio
Get free trial account at: https://www.twilio.com/try-twilio
Free trial includes $15 credit for testing
"""

import os
from twilio.rest import Client
from datetime import datetime

class WhatsAppService:
    def __init__(self):
        # Get credentials from environment variables
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.whatsapp_from = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")  # Twilio sandbox

        # Initialize client if credentials are available
        self.client = None
        self.enabled = False

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
        Send welcome message to new user
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

            message = f"""🎉 *Welcome to FastAPI Todo App!*

Hi {user_name}! 👋

Your account has been created successfully. 

✨ Features you'll love:
• Create and manage tasks
• Set task times and get reminders
• Mark tasks complete
• Filter and organize todos

💡 *Enable Notifications:*
Add your WhatsApp number in profile settings to get reminders 10 minutes before your tasks!

Happy task managing! 🚀"""

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

    def send_task_reminder(self, phone_number: str, task_title: str, task_time: datetime, user_name: str) -> bool:
        """
        Send task reminder 10 minutes before task time
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

            # Format task time
            time_str = task_time.strftime("%I:%M %p")
            date_str = task_time.strftime("%B %d, %Y")

            message = f"""⏰ *Task Reminder!*

Hi {user_name}! 

🔔 Your task is coming up in 10 minutes:

📝 *{task_title}*
⏰ Scheduled for: {time_str}
📅 Date: {date_str}

Don't forget to complete it! ✅

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
