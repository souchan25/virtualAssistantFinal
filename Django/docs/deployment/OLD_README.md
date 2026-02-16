# CPSU Virtual Health Assistant - Django Backend

A comprehensive health management system for Central Philippine State University with ML-powered disease prediction, AI chat assistant, and clinic management features.

## 🎯 Features

### For Students
- **Secure Authentication** - School ID-based login with encrypted passwords
- **Symptom Tracking** - Record and track symptoms with duration and severity
- **ML Disease Prediction** - Get instant predictions from 132 symptoms → 41 diseases
- **AI Health Assistant** - Multilingual chat support (English, Filipino, dialects)
- **Health Insights** - Top 3 AI-generated insights with references and reliability scores
- **Privacy First** - Explicit data consent with audit logging

### For Clinic Staff
- **Real-Time Dashboard** - Daily/weekly/monthly symptom trends
- **Student Directory** - Searchable, filterable student health records
- **Department Analytics** - Breakdown by department with top diseases
- **Hospital Referrals** - Auto-flag students with 5+ reports in 30 days
- **Data Export** - Excel reports for compliance and analysis
- **Audit Logs** - Complete security audit trail

## 🏗️ Architecture

```
Django/
├── health_assistant/       # Project settings
│   ├── settings.py        # Configuration
│   ├── urls.py            # Main URL routing
│   └── wsgi.py
├── clinic/                 # Main app
│   ├── models.py          # 7 core models
│   ├── views.py           # API endpoints
│   ├── serializers.py     # DRF serializers
│   ├── permissions.py     # Role-based access control
│   ├── middleware.py      # Audit logging middleware
│   ├── ml_service.py      # ML/AI integration
│   ├── admin.py           # Django admin config
│   └── tests.py           # Comprehensive tests
├── manage.py
├── requirements.txt
└── .env.example
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd Django
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings
```

### 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser

```bash
python manage.py createsuperuser
# Enter school_id (e.g., "admin001"), name, and password
```

### 5. Run Development Server

```bash
python manage.py runserver
```

API available at: `http://localhost:8000/api/`  
Admin panel: `http://localhost:8000/admin/`

## 📡 API Endpoints

### Authentication
```
POST /api/auth/register/       # Register new user
POST /api/auth/login/          # Login (get auth token)
POST /api/auth/logout/         # Logout (delete token)
```

### User Profile
```
GET    /api/profile/           # Get user profile
PATCH  /api/profile/           # Update profile (name, dept, address only)
POST   /api/profile/consent/   # Update data consent
```

### Symptoms & ML (Students only, requires consent)
```
POST /api/symptoms/submit/     # Submit symptoms → get prediction
GET  /api/symptoms/            # List own symptom records
GET  /api/symptoms/available/  # Get 132 available symptoms
```

### AI Chat (Students only, requires consent)
```
POST /api/chat/start/          # Start new chat session
POST /api/chat/message/        # Send message (real-time, not stored)
POST /api/chat/insights/       # Generate top 3 health insights
POST /api/chat/end/            # End session
```

### Clinic Staff (Staff role only)
```
GET  /api/staff/dashboard/     # Dashboard with statistics
GET  /api/staff/students/      # Searchable student directory
GET  /api/staff/export/        # Export symptom data
GET  /api/audit/               # View audit logs
```

## 🔒 Security Features

1. **Role-Based Access Control**
   - Students: Can only access own records
   - Staff: Can view all student data
   - Immutable fields: `school_id`, `role`

2. **Data Consent System**
   - Required for symptom submission and AI features
   - Tracked in `ConsentLog` with IP and timestamp
   - Users can revoke consent anytime

3. **Audit Logging**
   - Logs: logins, data exports, record access
   - Includes: IP address, user agent, timestamps
   - Failed login attempts tracked

4. **Middleware Protection**
   - `AuditMiddleware` - Auto-logs sensitive actions
   - CORS protection configured

## 🧪 Testing

Run all tests:
```bash
python manage.py test clinic
```

Run with coverage:
```bash
coverage run --source='clinic' manage.py test clinic
coverage report
coverage html  # Creates htmlcov/ directory
```

Test categories:
- **Model Tests**: User creation, consent, referral logic
- **API Tests**: Authentication, CRUD operations
- **Permission Tests**: Role-based access control
- **ML Tests**: Prediction accuracy, model loading

## 🔗 ML Integration

The Django backend integrates with the ML system in `../ML/`:

```python
# clinic/ml_service.py
from django.conf import settings

# Loads model from settings.ML_MODEL_PATH
predictor = MLPredictor()
result = predictor.predict(['fever', 'cough'])

# Returns:
# {
#     'predicted_disease': 'Common Cold',
#     'confidence_score': 0.85,
#     'top_predictions': [...],
#     'description': '...',
#     'precautions': [...]
# }
```

**Requirements:**
- Model must exist at `ML/models/disease_predictor_v2.pkl`
- Metadata CSVs in `ML/Datasets/active/`
- Model format: `{'model': sklearn_model, 'feature_names': list}`

## 📊 Database Schema

### Core Models

1. **CustomUser** - School ID-based authentication
   - Immutable: `school_id`, `role`
   - Editable: `name`, `department`, `cpsu_address`
   - Consent tracking

2. **SymptomRecord** - Health submissions
   - ML predictions with confidence scores
   - Auto-categorization (communicable/acute)
   - Referral tracking

3. **HealthInsight** - AI-generated insights
   - Session-based (not persistent across chats)
   - Reliability scores
   - References/sources

4. **ChatSession** - Session metadata only
   - No conversation history stored
   - Language tracking
   - Duration metrics

5. **ConsentLog** - Audit consent changes
6. **AuditLog** - Security audit trail
7. **DepartmentStats** - Cached statistics

## 🛠️ Development Workflow

### Adding New Endpoints

1. Define view in `clinic/views.py`
2. Create serializer in `clinic/serializers.py`
3. Add permission class if needed
4. Register URL in `clinic/urls.py`
5. Write tests in `clinic/tests.py`

### Modifying Models

```bash
# After editing models.py
python manage.py makemigrations
python manage.py migrate
```

### Custom Management Commands

Create in `clinic/management/commands/`:
```python
# Example: update_department_stats.py
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Update cached department statistics
        pass
```

Run: `python manage.py update_department_stats`

## 🚀 Production Deployment

### Environment Variables
```bash
DEBUG=False
ALLOWED_HOSTS=your-domain.com
SECRET_KEY=use-strong-random-key
```

### Database
Switch to PostgreSQL in settings.py:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}
```

### Static Files
```bash
python manage.py collectstatic
```

### Security Checklist
- [ ] Change `SECRET_KEY`
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Enable HTTPS redirects
- [ ] Set secure cookie flags
- [ ] Configure CORS properly
- [ ] Review audit log retention
- [ ] Implement rate limiting

## 🤝 Integration with Frontend

Expected request format:

**Register:**
```json
POST /api/auth/register/
{
  "school_id": "2024-001",
  "password": "securepass",
  "password_confirm": "securepass",
  "name": "Juan Dela Cruz",
  "department": "Computer Science",
  "cpsu_address": "Dorm 1",
  "data_consent_given": true
}
```

**Submit Symptoms:**
```json
POST /api/symptoms/submit/
Authorization: Token <user-token>

{
  "symptoms": ["fever", "cough", "headache"],
  "duration_days": 3,
  "severity": 2,
  "on_medication": false
}
```

**Response:**
```json
{
  "record_id": "uuid",
  "prediction": {
    "predicted_disease": "Common Cold",
    "confidence_score": 0.85,
    "top_predictions": [...],
    "description": "...",
    "precautions": [...]
  },
  "requires_referral": false
}
```

## 📝 Notes

- **Conversation History**: Not stored per requirements (privacy)
- **AI Insights**: Session-based, top 3 only
- **Referral Logic**: Automatic when 5+ reports in 30 days
- **Model Updates**: Restart server after updating ML models
- **Time Zone**: Set to `UTC` in settings (adjust if needed)

## 📄 License

Educational project for CPSU. Not for medical diagnosis.

## 🆘 Troubleshooting

**ML model not loading:**
```bash
# Check path in settings.py
ML_MODEL_PATH = BASE_DIR.parent / 'ML' / 'models' / 'disease_predictor_v2.pkl'

# Verify file exists
ls ../ML/models/
```

**Import errors:**
```bash
pip install -r requirements.txt --upgrade
```

**Database errors:**
```bash
python manage.py migrate --run-syncdb
```

**Tests failing:**
```bash
# Run specific test
python manage.py test clinic.tests.AuthenticationAPITests.test_user_registration -v 2
```

---

**Everything is set up and working!** 🎉
