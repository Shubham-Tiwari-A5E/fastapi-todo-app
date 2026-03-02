# 🚀 WhatsApp Notifications - Quick Setup

## ✅ What's Been Added

### New Features:
1. **Phone Number** in user profile (WhatsApp number with country code)
2. **Task Time** - Schedule tasks for specific date/time
3. **Notification Toggle** - Enable/disable reminders per task
4. **10-Min Reminders** - Automatic WhatsApp alerts before tasks
5. **Welcome Messages** - Greet new users on registration

### Files Modified/Created:
- ✅ `models.py` - Added phone_number, task_time, notification_enabled
- ✅ `schemas.py` - Updated schemas for new fields
- ✅ `users.py` - Welcome message integration
- ✅ `services/todoService.py` - Handle new fields
- ✅ `services/whatsapp_service.py` - NEW: WhatsApp integration
- ✅ `services/notification_scheduler.py` - NEW: Background scheduler
- ✅ `main.py` - Start/stop scheduler on app lifecycle
- ✅ `requirements.txt` - Added twilio==9.0.4
- ✅ `alembic/versions/...` - Database migration

---

## 🎯 Quick Start (3 Steps)

### Step 1: Install Twilio
```bash
cd C:\Users\A5E\Python\FastAPI\Todos
..\fastapienv\Scripts\pip install twilio python-dotenv
```

### Step 2: Get Twilio Credentials (FREE!)

1. **Sign up:** https://www.twilio.com/try-twilio
2. **Get credentials:**
   - Account SID: `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - Auth Token: `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
3. **Join WhatsApp Sandbox:**
   - Go to: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
   - Send `join <your-code>` to `+1 415 523 8886`

### Step 3: Set Environment Variables

**Option A: Create .env file** (for local)

Create `C:\Users\A5E\Python\FastAPI\Todos\.env`:

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

**Option B: Render Environment Variables** (for production)

Add in Render Dashboard → Your Service → Environment:
```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxx
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

---

## 🧪 Test It Now!

### Test 1: Start Server
```bash
cd C:\Users\A5E\Python\FastAPI\Todos
..\fastapienv\Scripts\uvicorn main:app --reload
```

**Look for:**
```
✅ Database connection successful!
✅ WhatsApp service initialized
✅ WhatsApp notification scheduler started
```

### Test 2: Register with Phone Number

**POST** `http://localhost:8000/register`

```json
{
  "name": "Test User",
  "email": "test@example.com",
  "password": "test123",
  "phone_number": "+919876543210"
}
```

**Check WhatsApp:** You should receive welcome message! 🎉

### Test 3: Create Task with Reminder

**POST** `http://localhost:8000/todos` (with Bearer token)

```json
{
  "title": "Test Task",
  "description": "Testing reminders",
  "priority": 3,
  "task_time": "2026-03-02T15:30:00",
  "notification_enabled": true
}
```

**Result:** Reminder scheduled for 10 minutes before task time!

---

## 📊 API Changes Summary

### User Registration (Updated):
```json
// NEW: phone_number field
{
  "name": "string",
  "email": "string",
  "password": "string",
  "phone_number": "+919876543210"  // NEW! Optional
}
```

### User Profile (NEW Endpoints):
```
GET /profile        - Get user profile
PUT /profile        - Update name and phone number
```

### Todo Creation (Updated):
```json
{
  "title": "string",
  "description": "string",
  "priority": 1-5,
  "isCompleted": false,
  "task_time": "2026-03-02T14:30:00",    // NEW! Optional
  "notification_enabled": true            // NEW! Default: true
}
```

---

## 🔧 Configuration

### Environment Variables:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TWILIO_ACCOUNT_SID` | Yes* | None | Twilio Account SID |
| `TWILIO_AUTH_TOKEN` | Yes* | None | Twilio Auth Token |
| `TWILIO_WHATSAPP_NUMBER` | No | `whatsapp:+14155238886` | Twilio sandbox number |

*Required only if you want WhatsApp notifications. App works without them.

---

## 📱 Phone Number Format

**Correct:**
```
+919876543210     ✅ India
+14155551234      ✅ USA
+447700900000     ✅ UK
```

**Wrong:**
```
9876543210        ❌ No country code
+91 987 654 3210  ❌ Spaces
919876543210      ❌ No + symbol
```

**Rule:** Always use `+[country code][number]` with no spaces!

---

## 🎯 Features in Action

### Welcome Message:
- **Trigger:** User registers with phone_number
- **When:** Immediately on registration
- **Format:** Friendly welcome with app features

### Task Reminder:
- **Trigger:** Task with task_time + notification_enabled
- **When:** Exactly 10 minutes before task_time
- **Condition:** Task not completed, user has phone_number
- **Format:** Task details + time + friendly reminder

### Notification Toggle:
- **Per Task:** Each task can have notifications ON/OFF
- **Default:** ON (enabled)
- **Update Anytime:** Change in PUT /todos/{id}

---

## 🚀 Deployment Checklist

### Local Development:
- [x] Install twilio package
- [ ] Create .env file with credentials
- [ ] Join Twilio WhatsApp sandbox
- [ ] Test welcome message
- [ ] Test task reminder
- [ ] Verify scheduler logs

### Render Deployment:
- [x] twilio==9.0.4 in requirements.txt
- [ ] Add environment variables in Render
- [ ] Push to GitHub
- [ ] Deploy to Render
- [ ] Check logs for scheduler startup
- [ ] Test with production database

---

## 🆘 Common Issues

### "WhatsApp service not enabled"
**Fix:** Set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN environment variables

### "Failed to send message"
**Fix:** 
1. User must join Twilio sandbox first
2. Send "join <code>" to +1 415 523 8886
3. Wait for confirmation message

### "No reminders received"
**Check:**
- User has phone_number?
- Task has task_time?
- notification_enabled is true?
- Task not completed?
- Server running?
- Check logs for scheduler activity

---

## 💡 Tips & Best Practices

### 1. **Testing:**
- Use FREE Twilio trial ($15 credit)
- Test with your own number first
- Join sandbox before expecting messages

### 2. **Phone Numbers:**
- Always validate format (+country code)
- Store as optional field
- Let users update anytime

### 3. **Notifications:**
- Default to enabled (better UX)
- Let users toggle per task
- Don't send for completed tasks

### 4. **Timing:**
- Current: 10 minutes before
- Easy to customize in `notification_scheduler.py`
- Consider time zones for global users

---

## 📖 Full Documentation

See `WHATSAPP_NOTIFICATIONS_GUIDE.md` for:
- Complete API reference
- Detailed setup instructions
- Message templates
- Architecture explanation
- Cost breakdown
- Troubleshooting guide

---

## 🎉 Summary

**You now have:**
- ✅ WhatsApp integration with Twilio
- ✅ Automatic welcome messages
- ✅ 10-minute task reminders
- ✅ Per-task notification control
- ✅ User phone number management
- ✅ Background scheduler running
- ✅ Production-ready code

**Next Steps:**
1. Get Twilio credentials (FREE trial)
2. Set environment variables
3. Test locally
4. Deploy to Render
5. Enjoy automated notifications! 🎊

**Questions?** Check `WHATSAPP_NOTIFICATIONS_GUIDE.md` for complete guide!
