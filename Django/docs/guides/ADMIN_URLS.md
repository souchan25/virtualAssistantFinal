# Admin Dashboard URL Reference

## Dashboard Pages

All admin dashboard pages are protected with `@staff_member_required` decorator.

### 1. Overview Dashboard
```
URL: http://localhost:8000/api/admin/monitoring/
Name: admin-monitoring
View: admin_views.backend_monitoring_dashboard()
Description: System overview with health checks, user stats, and API metrics
```

### 2. User Management Dashboard
```
URL: http://localhost:8000/api/admin/users/
Name: admin-users
View: admin_views.admin_users_page()
Description: User directory, activity tracking, and user management
```

### 3. Health Records Dashboard
```
URL: http://localhost:8000/api/admin/health-records/
Name: admin-health
View: admin_views.admin_health_records_page()
Description: Symptom submissions, disease predictions, and health trends
```

### 4. API Analytics Dashboard
```
URL: http://localhost:8000/api/admin/api-analytics/
Name: admin-analytics
View: admin_views.admin_api_analytics_page()
Description: API performance, error tracking, and endpoint usage
```

### 5. Settings & Configuration
```
URL: http://localhost:8000/api/admin/settings/
Name: admin-settings
View: admin_views.admin_settings_page()
Description: System configuration, LLM providers, and database stats
```

---

## Template Links in Templates

All templates use Django's URL tag for consistent navigation:

```html
<!-- From any dashboard page, navigate to another: -->
<a href="{% url 'admin:admin-monitoring' %}">Overview</a>
<a href="{% url 'admin:admin-users' %}">Users</a>
<a href="{% url 'admin:admin-health' %}">Health Records</a>
<a href="{% url 'admin:admin-analytics' %}">API Analytics</a>
<a href="{% url 'admin:admin-settings' %}">Settings</a>
```

---

## Django Admin Integration

The admin dashboards integrate with Django's default admin site:

```
Main Admin: http://localhost:8000/admin/
├── Dashboard Pages (Custom)
│   ├── Monitoring: /api/admin/monitoring/
│   ├── Users: /api/admin/users/
│   ├── Health: /api/admin/health-records/
│   ├── Analytics: /api/admin/api-analytics/
│   └── Settings: /api/admin/settings/
└── Standard Admin Models
    ├── Users: /admin/clinic/customuser/
    ├── Symptoms: /admin/clinic/symptomrecord/
    ├── Chats: /admin/clinic/chatsession/
    └── Audit Logs: /admin/clinic/auditlog/
```

---

## Code Examples

### Reference a Dashboard URL in Your Code

```python
# In views.py
from django.urls import reverse

dashboard_url = reverse('admin:admin-monitoring')

# In templates
<a href="{% url 'admin:admin-monitoring' %}">Go to Dashboard</a>
```

### Redirect to Dashboard

```python
# In a view
from django.shortcuts import redirect
from django.urls import reverse

return redirect(reverse('admin:admin-monitoring'))
```

---

## Security

All dashboard pages are protected:

```python
@staff_member_required
def admin_monitoring_dashboard(request):
    # Only accessible to staff members
    pass
```

- Requires login
- Requires staff status
- Cannot be accessed by regular users
- CSRF protection enabled

---

## Quick Navigation Tips

1. **From Overview Dashboard**: Use the tabbed navigation at the top
2. **From Any Dashboard**: Use the nav-tabs bar to switch sections
3. **From Admin Home**: Click "Backend Monitoring Dashboard" link (if added to admin homepage)
4. **Quick Actions**: Each page has quick action buttons to common admin tasks

---

## Data Refresh

Dashboard pages are rendered fresh on each request:
- Latest database data
- Real-time metrics
- No caching by default
- Timestamp shows when page was loaded

---

## Performance Notes

- Queries are optimized with `.values()` and `.annotate()`
- Large data sets use `.order_by('-timestamp')[:n]` for limit
- All database access uses Django ORM for safety
- No N+1 queries in default views

---

## Customization

To add a new dashboard page:

1. Create a view function in `admin_views.py`:
```python
@staff_member_required
def admin_new_dashboard(request):
    context = {
        'data': get_data(),
    }
    return render(request, 'admin/new_dashboard.html', context)
```

2. Add URL in `clinic/urls.py`:
```python
path('admin/new-dashboard/', admin_views.admin_new_dashboard, name='admin-new'),
```

3. Create template `admin/new_dashboard.html` with same styling

4. Add link to nav-tabs in all templates

---

**Last Updated**: January 2026
**Django Version**: 3.2+
**Status**: Production Ready
