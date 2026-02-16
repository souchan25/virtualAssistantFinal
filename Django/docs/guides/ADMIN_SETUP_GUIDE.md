# Django Admin Panel Setup Guide
## Developer Backend Monitoring & Staff Account Management

### 🔒 Security & Privacy First

**IMPORTANT:** This admin panel is configured for **DEVELOPERS ONLY**, not for clinic staff.

**What you CAN do:**
- ✅ Create clinic staff accounts
- ✅ Manage user permissions and roles
- ✅ Monitor backend flow (via Django logs)
- ✅ Track system health and errors

**What is HIDDEN (by design):**
- ❌ All medical data (medications, alerts, follow-ups)
- ❌ Patient symptoms and diagnoses
- ❌ AI chat conversations
- ❌ Health insights and records
- ❌ Sensitive audit logs

**Why?** You're a developer, not a medical professional. Patient data privacy is paramount.

---

## 🎨 Features

### Modern UI with Jazzmin
- Clean, responsive interface with CPSU green theme
- Dashboard with quick access to user management
- Enhanced navigation and search capabilities
- Colored status badges for account status
- Focus on backend monitoring and staff account creation

### What's Visible in Admin Panel

✅ **User Management ONLY**
- Create clinic staff accounts
- Manage student accounts
- Set roles and permissions
- Activate/deactivate accounts
- Bulk actions for user management

### What's Hidden (Sensitive Medical Data)

❌ **NOT visible in admin panel:**
- **Medication** - Prescription data
- **MedicationLog** - Medication adherence records
- **FollowUp** - Patient follow-up appointments
- **EmergencyAlert** - Emergency medical alerts
- **SymptomRecord** - Patient diagnosis data
- **HealthInsight** - AI-generated health insights
- **ChatSession** - Chat conversation logs
- **ConsentLog** - Privacy consent logs
- **AuditLog** - System audit trails
- **DepartmentStats** - Statistical aggregations

> **All medical data is HIDDEN for security and privacy.** Clinic staff access medical data through the Vue.js frontend, not the admin panel.

---

## 📦 Installation

### 1. Install Jazzmin (Already Done)
```bash
cd Django
pip install django-jazzmin>=2.6.0
```

### 2. Requirements
The `requirements.txt` already includes:
```
django-jazzmin>=2.6.0
```
### 3. Configuration Already Added
The following have been configured in your project:

**`health_assistant/settings.py`:**
- Jazzmin added to `INSTALLED_APPS` (must be before `django.contrib.admin`)
- `JAZZMIN_SETTINGS` - Full configuration with CPSU branding
- `JAZZMIN_UI_TWEAKS` - Green theme matching CPSU colors

**`clinic/admin.py`:**
- Completely redesigned with modern admin classes
- Colored status badges
- Quick actions and bulk operations
- Sensitive models removed from admin registration

---

## 🚀 Usage

### Access Admin Panel
```
http://localhost:8000/admin/
```

### Login Credentials
Use your superuser credentials:
```bash
# If you don't have a superuser, create one:
cd Django
python manage.py createsuperuser
# When prompted, enter:
# - School ID (instead of username)
# - Password
```

### Creating Staff Accounts

1. **Navigate to:** Users → Add User
2. **Fill in:**
   - School ID: `STAFF-001` (or similar)
   - Name: `Staff Name`
   - Department: `College of Nursing` (or appropriate)
   - Role: Select `clinic_staff`
   - Password: Set secure password
   - **Check:** `Is Staff` (important for admin access)
   - **Check:** `Is Active`
3. **Save**

### Bulk Actions

**For Users:**
- ✓ Activate selected users
- ✗ Deactivate selected users
- 👔 Grant staff access

**For Follow-Ups:**
- ✓ Mark as completed
- ✗ Mark as missed

**For Emergency Alerts:**
- 👁️ Acknowledge alerts
- 🔄 Mark as in progress
- ✅ Mark as resolved

---

## 🎨 Admin Panel Features

### Dashboard
- Quick overview of all models
- Recent actions log
- Quick links to add new records

### User Management
**List View:**
- School ID, Name, Role, Department
- Colored status badges (Consent, Account)
- Filter by role, consent, active status
- Search by ID, name, department

**Detail View:**
- 🔐 Login Credentials
- 👤 Personal Information
- 🛡️ Role & Permissions
- ✅ Data Consent
- 📅 Important Dates

### Medications
- Student links (click to view student)
- Active/Inactive status badges
- Date hierarchy for easy filtering
- Collapsible sections for cleaner UI

### Follow-Ups
- Student links
- Status badges (Pending/Completed/Missed/Cancelled)
- Reason preview (truncated for readability)
- Quick complete/miss actions

### Emergency Alerts
- Severity badges (Low/Medium/High/Critical)
- Status badges (Pending/Acknowledged/In Progress/Resolved)
- Alert descriptions with locations
- Response tracking

---

## 🎯 Key Admin Actions

### Create Clinic Staff Account
```python
1. Admin → Users → Add User
2. School ID: STAFF-XXX
3. Role: clinic_staff
4. Is Staff: ✓ (checked)
5. Is Active: ✓ (checked)
6. Save
```

### Monitor Backend Flow
```python
# View recent activities:
1. Admin Dashboard → Recent Actions
2. Filter models by date
3. Check logs in terminal/console

# Track API usage:
- Check Django logs
- Monitor database queries
- Use middleware logging
```

### Bulk User Management
```python
1. Admin → Users
2. Select users (checkboxes)
3. Action dropdown:
   - Activate selected users
   - Deactivate selected users
   - Grant staff access
4. Go
```

---

## 🔒 Security Notes

### Admin Access Control
- Only superusers can access all admin features
- Staff users (with `is_staff=True`) can access assigned models
- Sensitive models are hidden from admin panel entirely

### Best Practices
1. **Never share superuser credentials**
2. **Create individual staff accounts** for each clinic personnel
3. **Use strong passwords** for all accounts
4. **Regularly review user permissions**
5. **Monitor admin logs** for suspicious activity

---

## 🎨 Customization

### Theme Colors
Current configuration uses CPSU green theme:
```python
# In settings.py JAZZMIN_UI_TWEAKS:
"brand_colour": "navbar-success",  # CPSU Green
"sidebar": "sidebar-dark-success",  # Green sidebar
```

### Custom Links
Top menu includes:
- Home (Dashboard)
- API Documentation
- Support (GitHub repository)

### Icons
Font Awesome icons used throughout:
- 👤 Users: `fas fa-user-circle`
- 💊 Medications: `fas fa-pills`
- 📋 Follow-Ups: `fas fa-calendar-check`
- 🚨 Emergencies: `fas fa-exclamation-triangle`

---

## 📊 Monitoring Backend Flow

### Django Logs
```python
# Check terminal for real-time logs
# Look for:
- Request/Response logs
- Database queries
- Error messages
- API calls
```

### Database Queries
```bash
# Access database directly if needed:
cd Django
python manage.py dbshell

# Or use admin panel to view/edit records
```

### API Usage
```python
# Monitor through:
1. Django admin → Users → Recent Actions
2. Check AuditLog via database (not in admin)
3. Server logs in terminal
```

---

## 🛠️ Troubleshooting

### Jazzmin Not Loading
```bash
# Ensure jazzmin is installed:
pip install django-jazzmin

# Check INSTALLED_APPS order:
# 'jazzmin' must be BEFORE 'django.contrib.admin'
```

### Admin Styles Not Working
```bash
# Collect static files:
python manage.py collectstatic

# Clear browser cache
```

### Can't Create Staff Account
```bash
# Ensure you're logged in as superuser
# Check that 'is_staff' is checked
# Verify role is set to 'clinic_staff'
```

---

## 📚 Additional Resources

- **Jazzmin Documentation:** https://django-jazzmin.readthedocs.io/
- **Django Admin:** https://docs.djangoproject.com/en/4.2/ref/contrib/admin/
- **Project Docs:** `/Django/docs/`

---

**Last Updated:** December 2024  
**Version:** 1.0 (Jazzmin Integration)
