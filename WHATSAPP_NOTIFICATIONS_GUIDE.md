# 📱 WhatsApp Notifications Feature - Complete Guide

## 🎉 New Features Added

### 1. **Phone Number in User Profile** ✅
- Users can add their WhatsApp number (with country code)
- Format: `+919876543210` (country code + number)
- Added in registration and profile update

### 2. **Task Time Scheduling** ✅
- Set specific date and time for each task
- Format: `2026-03-02T14:30:00`
- Optional field - tasks without time won't send reminders

### 3. **10-Minute Reminder Notifications** ✅
- Automatic WhatsApp message 10 minutes before task time
- Only sent if:
  - User has phone number
  - Task has task_time set
  - Task is not completed
  - Notifications are enabled for that task

### 4. **Notification Toggle** ✅
- Each task has `notification_enabled` checkbox
- Turn ON/OFF reminders per task
- Default: ON (enabled)

### 5. **Welcome Message** ✅
- Automatic WhatsApp welcome message on registration
- Only sent if user provides phone number during signup

---

## 🛠️ Setup Instructions

### Step 1: Get Twilio Account (FREE!)

1. **Sign up for Twilio:**
   - Go to: https://www.twilio.com/try-twilio
   - Create free account
   - Get $15 credit for testing (no credit card required!)

2. **Get Your Credentials:**
   - Dashboard → Account → Account Info
   - Copy:
     - **Account SID**: `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
     - **Auth Token**: `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

3. **Set up WhatsApp Sandbox:**
   - Go to: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
   - Follow instructions to join sandbox
   - Send `join <your-code>` to Twilio WhatsApp number
   - Example: Send `join happy-cat` to `+1 415 523 8886`

### Step 2: Set Environment Variables

#### For Local Development:
Create a `.env` file in `Todos/` directory:

```env
# Twilio WhatsApp Credentials
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Database (existing)
DATABASE_URL=mysql+pymysql://root:raj1234@localhost/todos
```

#### For Render Deployment:
Add in Render Dashboard → Environment:

```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

### Step 3: Install Dependencies

```bash
cd C:\Users\A5E\Python\FastAPI\Todos
..\fastapienv\Scripts\pip install twilio python-dotenv
```

### Step 4: Apply Database Migration

```bash
# Already done! But if needed:
alembic upgrade head
```

---

## 📊 Database Changes

### Users Table - New Column:
```sql
ALTER TABLE users ADD COLUMN phone_number VARCHAR(20) NULL;
```

### Todos Table - New Columns:
```sql
ALTER TABLE todos ADD COLUMN task_time DATETIME NULL;
ALTER TABLE todos ADD COLUMN notification_enabled BOOLEAN DEFAULT TRUE;
```

---

## 🔌 API Endpoints

### 1. Register with Phone Number

**POST** `/register`

```json
{
  "name": "Shubham Tiwari",
  "email": "shubham@example.com",
  "password": "SecurePass123",
  "phone_number": "+919876543210"
}
```

**Response:**
```json
{
  "id": "uuid",
  "name": "Shubham Tiwari",
  "email": "shubham@example.com",
  "phone_number": "+919876543210"
}
```

**WhatsApp:** Automatic welcome message sent! 🎉

### 2. Update Profile

**PUT** `/profile`

```json
{
  "name": "Updated Name",
  "phone_number": "+919876543210"
}
```

### 3. Get Profile

**GET** `/profile`

Headers: `Authorization: Bearer <token>`

### 4. Create Todo with Time & Notifications

**POST** `/todos`

```json
{
  "title": "Important Meeting",
  "description": "Discuss project timeline",
  "priority": 5,
  "isCompleted": false,
  "task_time": "2026-03-02T14:30:00",
  "notification_enabled": true
}
```

**Result:** 
- Todo created ✅
- Reminder scheduled for `2026-03-02T14:20:00` (10 minutes before)

### 5. Update Todo (Toggle Notifications)

**PUT** `/todos/{todo_id}`

```json
{
  "title": "Important Meeting",
  "description": "Updated description",
  "priority": 5,
  "isCompleted": false,
  "task_time": "2026-03-02T14:30:00",
  "notification_enabled": false
}
```

---

## 💬 WhatsApp Message Examples

### Welcome Message:
```
🎉 *Welcome to FastAPI Todo App!*

Hi Shubham! 👋

Your account has been created successfully. 

✨ Features you'll love:
• Create and manage tasks
• Set task times and get reminders
• Mark tasks complete
• Filter and organize todos

💡 *Enable Notifications:*
Add your WhatsApp number in profile settings to get reminders 10 minutes before your tasks!

Happy task managing! 🚀
```

### Task Reminder (10 min before):
```
⏰ *Task Reminder!*

Hi Shubham! 

🔔 Your task is coming up in 10 minutes:

📝 *Important Meeting*
⏰ Scheduled for: 02:30 PM
📅 Date: March 02, 2026

Don't forget to complete it! ✅

_Reply STOP to unsubscribe from reminders_
```

---

## 🏗️ Architecture

### Background Scheduler:
- Runs every 60 seconds
- Checks database for upcoming tasks
- Sends WhatsApp reminders automatically
- Handles multiple users simultaneously

### WhatsApp Service:
- Singleton instance
- Twilio API integration
- Error handling and logging
- Rate limiting protection

### Flow:
```
User creates task with task_time
    ↓
Saved to database
    ↓
Background scheduler checks every minute
    ↓
10 minutes before task_time?
    ↓
Send WhatsApp reminder
    ↓
User gets notification! 📱
```

---

## 🧪 Testing

### Test Welcome Message:

1. Register new user with phone number
2. Check your WhatsApp for welcome message
3. Should receive within 5 seconds

### Test Task Reminder:

1. Create a task with `task_time` = 11 minutes from now
2. Enable notifications: `notification_enabled: true`
3. Wait 1 minute
4. Check WhatsApp - should receive reminder in 10 minutes

### Test Notification Toggle:

1. Create task with notifications enabled
2. Update task with `notification_enabled: false`
3. No reminder will be sent

---

## 📱 Phone Number Format

### Correct Formats:
```
+919876543210    ✅ (India)
+14155551234     ✅ (USA)
+447700900000    ✅ (UK)
+971501234567    ✅ (UAE)
```

### Wrong Formats:
```
9876543210       ❌ (missing country code)
+91 98765 43210  ❌ (spaces)
919876543210     ❌ (missing +)
```

**Important:** Always include `+` and country code!

---

## ⚙️ Configuration Options

### Twilio Sandbox (FREE - Testing):
```
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```
- Free for testing
- Users must join sandbox first
- Send "join <code>" to activate

### Twilio Production (Paid):
```
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238887
```
- Get approved WhatsApp Business number
- No "join" required
- Users receive messages directly
- Costs: ~$0.005 per message

### Reminder Timing:
Currently: **10 minutes before task**

To change, edit `notification_scheduler.py`:
```python
reminder_start = now + timedelta(minutes=9, seconds=30)  # Change 9
reminder_end = now + timedelta(minutes=10, seconds=30)   # Change 10
```

---

## 🚨 Troubleshooting

### Issue: "WhatsApp service not enabled"
**Solution:** 
- Check environment variables are set
- Verify TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN
- Restart server

### Issue: "Failed to send message"
**Solution:**
- User must join Twilio sandbox first
- Send "join <code>" to sandbox number
- Check phone number format (+country code)

### Issue: "No reminders received"
**Checklist:**
- [ ] User has phone_number in profile
- [ ] Todo has task_time set
- [ ] notification_enabled is True
- [ ] Task is not completed
- [ ] User joined Twilio sandbox
- [ ] Server is running (scheduler active)

### Issue: "Invalid phone number"
**Solution:**
- Use international format: +[country code][number]
- No spaces or special characters
- Example: `+919876543210`

---

## 💰 Cost Breakdown

### FREE Tier (Twilio Trial):
- $15 credit
- ~3000 messages
- Perfect for testing
- Sandbox mode only

### Production Costs:
- WhatsApp messages: $0.005 each (0.5 cents)
- 100 messages/day = $15/month
- 1000 messages/day = $150/month

### Optimization Tips:
1. Only send reminders for important tasks
2. Let users opt-out with notification toggle
3. Batch messages if possible
4. Consider alternative: Email notifications (FREE)

---

## 🔐 Security Best Practices

### 1. Environment Variables:
```bash
# NEVER commit these to Git!
TWILIO_ACCOUNT_SID=secret
TWILIO_AUTH_TOKEN=secret
```

### 2. Rate Limiting:
```python
# Already implemented in scheduler
await asyncio.sleep(1)  # 1 second delay between messages
```

### 3. User Privacy:
- Phone numbers stored securely
- Optional field (not required)
- Users control notifications per task

---

## 📈 Future Enhancements

### Possible Additions:
1. **Multiple Reminder Times**
   - 1 hour before
   - 30 minutes before
   - 10 minutes before

2. **Recurring Tasks**
   - Daily reminders
   - Weekly reminders
   - Custom schedules

3. **SMS Fallback**
   - If WhatsApp fails, send SMS

4. **Email Notifications**
   - FREE alternative to WhatsApp
   - No sandbox requirement

5. **Custom Messages**
   - Users can customize reminder text
   - Add emojis, templates

---

## 🎯 Usage Example

### Complete Workflow:

```bash
# 1. Register with phone number
POST /register
{
  "name": "Shubham",
  "email": "shubham@example.com", 
  "password": "pass123",
  "phone_number": "+919876543210"
}
# → Welcome WhatsApp received! ✅

# 2. Login
POST /token
username: shubham@example.com
password: pass123
# → Get access token

# 3. Create task with reminder
POST /todos
{
  "title": "Client Call",
  "priority": 5,
  "task_time": "2026-03-02T15:00:00",  # 3:00 PM
  "notification_enabled": true
}
# → Task created, reminder scheduled

# 4. At 2:50 PM (10 min before)
# → WhatsApp reminder sent automatically! 📱

# 5. Complete task
PUT /todos/{id}
{
  "isCompleted": true
}
# → No more reminders for this task
```

---

## ✅ Verification Checklist

Before deploying to production:

- [ ] Twilio account created
- [ ] Credentials added to environment variables
- [ ] Dependencies installed (twilio==9.0.4)
- [ ] Database migration applied
- [ ] WhatsApp sandbox tested
- [ ] Welcome message working
- [ ] Task reminders working
- [ ] Notification toggle working
- [ ] Phone number validation working
- [ ] Error handling tested
- [ ] Logs showing scheduler running

---

## 📞 Support

### Twilio Support:
- Docs: https://www.twilio.com/docs/whatsapp
- Console: https://console.twilio.com
- Support: https://support.twilio.com

### Feature Issues:
Check logs for:
```
✅ WhatsApp service initialized
✅ Notification scheduler started
📬 Found X todos needing reminders
✅ Reminder sent for task: ...
```

---

**🎉 Congratulations! WhatsApp notifications are now fully integrated!**

Users can now:
- ✅ Get welcome messages on signup
- ✅ Receive reminders 10 minutes before tasks
- ✅ Control notifications per task
- ✅ Manage their phone number in profile

**Happy notifying! 📱✨**
