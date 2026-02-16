# 🎨 Django Admin Dashboard - Quick Reference Card

## 📋 Dashboard Overview

| Dashboard | URL | Features | Icon |
|-----------|-----|----------|------|
| **Monitoring** | `/api/admin/monitoring/` | System health, user stats, API metrics | 📊 |
| **Users** | `/api/admin/users/` | User directory, activity, roles | 👥 |
| **Health Records** | `/api/admin/health-records/` | Symptoms, diseases, predictions | 🏥 |
| **API Analytics** | `/api/admin/api-analytics/` | Performance, errors, endpoints | 📈 |
| **Settings** | `/api/admin/settings/` | Config, providers, system info | ⚙️ |

---

## 🎨 CPSU Theme Colors

```
Primary:   #006B3F (Earls Green)    - Headers, Buttons, Primary Elements
Secondary: #FFF44F (Lemon Yellow)   - Accents, Highlights, Decorations
Dark:      #004d2d (Earls Green Dark) - Hover states, Dark backgrounds
Light:     #f8f9fa (Off-white)      - Background, Cards
Text:      #2c3e50 (Dark blue-gray) - Body text
```

---

## 🚀 Quick Start

### Access the Dashboards

```bash
# 1. Start Django
cd Django
python manage.py runserver

# 2. Open in browser
http://localhost:8000/api/admin/monitoring/

# 3. Login with staff credentials
```

### Test a Dashboard

```python
# In Django shell
python manage.py shell

from clinic.models import CustomUser, AuditLog
from clinic.admin_views import backend_monitoring_dashboard

# Data will be displayed automatically in templates
```

---

## 📊 Key Metrics Tracked

### Monitoring Dashboard
- ✓ Total Users
- ✓ Active Users (24h)
- ✓ Staff Count
- ✓ Student Count
- ✓ Total API Requests (24h)
- ✓ Failed Requests (24h)
- ✓ Success Rate (24h)
- ✓ Failed Login Attempts (24h)

### Users Dashboard
- ✓ Total Users
- ✓ Students vs Staff
- ✓ Active Users (30d)
- ✓ Recent User Registrations
- ✓ Most Active Users (30d)
- ✓ User Role Distribution

### Health Records Dashboard
- ✓ Total Symptom Records
- ✓ Records (7d, 30d)
- ✓ Confidence Distribution (High/Medium/Low)
- ✓ Top 10 Predicted Diseases
- ✓ Recent Symptom Submissions

### API Analytics Dashboard
- ✓ API Performance (7d, 30d)
- ✓ Success Rate Comparison
- ✓ Top 10 Endpoints
- ✓ Error Breakdown
- ✓ Recent Errors

### Settings Dashboard
- ✓ Debug Mode Status
- ✓ ML Model Status
- ✓ LLM Providers (4 providers)
- ✓ Database Statistics
- ✓ System Information

---

## 🔧 Common Customizations

### Add a New Stat Card

```html
<div class="stat-card">
    <div class="stat-label">Your Metric</div>
    <div class="stat-value">{{ your_value }}</div>
    <div style="font-size: 12px; color: var(--text-light);">Description</div>
</div>
```

### Change Colors

Edit CSS variables in templates:
```css
:root {
    --cpsu-green: #006B3F;      /* Change primary color */
    --cpsu-yellow: #FFF44F;     /* Change accent color */
}
```

### Add Quick Action Button

```html
<a href="{% url 'admin:your-url' %}" class="action-btn">
    <span>icon</span>
    Button Text
</a>
```

---

## 📁 File Structure

```
Django/
├── clinic/
│   ├── admin_views.py                 (5 view functions)
│   ├── urls.py                        (5 URL routes)
│   └── templates/
│       └── admin/
│           ├── base_site.html         (global admin styling)
│           ├── backend_monitoring.html (monitoring dashboard)
│           ├── users.html             (users dashboard)
│           ├── health_records.html    (health records dashboard)
│           ├── api_analytics.html     (analytics dashboard)
│           └── settings.html          (settings dashboard)
└── docs/
    └── guides/
        ├── ADMIN_DASHBOARD_GUIDE.md  (detailed guide)
        └── ADMIN_URLS.md             (URL reference)
```

---

## 🔒 Security Notes

- ✅ All pages require `@staff_member_required`
- ✅ CSRF protection enabled
- ✅ No sensitive data exposed
- ✅ Django ORM used (SQL injection safe)
- ✅ User authentication required

---

## 📊 Database Models Used

| Model | Purpose | Dashboard |
|-------|---------|-----------|
| `CustomUser` | User accounts | Monitoring, Users |
| `AuditLog` | API activity tracking | All |
| `SymptomRecord` | Health submissions | Health, Monitoring |
| `ChatSession` | Chat history | Health, Settings |

---

## 🎯 Navigation Tips

1. **Tab Navigation**: Click tabs at top to switch dashboards
2. **Quick Actions**: Use buttons for common tasks
3. **Filter Links**: Some numbers link to filtered admin views
4. **External Links**: Provider dashboard links open in new tabs
5. **Timestamps**: All pages show last update time

---

## 📈 Performance Tips

- Pages load data fresh on each request
- Optimized queries with `.values()` and `.annotate()`
- Limited results with `.order_by('-timestamp')[:n]`
- No N+1 queries by default
- No database caching (real-time data)

---

## 🆘 Troubleshooting

### Dashboard not loading?
1. Check Django is running: `python manage.py runserver`
2. Verify user is staff: `User.is_staff = True`
3. Check URL: `/api/admin/monitoring/`

### Data not showing?
1. Ensure database migrations are done: `python manage.py migrate`
2. Check model data exists
3. Verify querysets in view functions

### Styling issues?
1. Clear browser cache (Ctrl+Shift+Delete)
2. Check CSS variables in `:root`
3. Verify template syntax

---

## 📚 Documentation

- **Full Guide**: `Django/docs/guides/ADMIN_DASHBOARD_GUIDE.md`
- **URL Reference**: `Django/docs/guides/ADMIN_URLS.md`
- **Code**: Comments in `admin_views.py`

---

## ✨ Features

- ✓ Real-time data
- ✓ CPSU branded
- ✓ Responsive design
- ✓ Fast loading
- ✓ Mobile-friendly
- ✓ Well-documented
- ✓ Easy to customize
- ✓ Secure

---

**Version**: 2.0.0  
**Created**: January 2026  
**Status**: ✅ Production Ready  
**Maintainer**: Django Admin Team
