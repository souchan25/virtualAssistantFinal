<!--
Guidance for AI coding agents working in this repository.
Keep this file short, concrete, and tied to the actual files present.
-->

# Copilot instructions — VirtualAssistant

## Summary
**CPSU Virtual Health Assistant** — Full-stack health assistant with Django REST API, hybrid ML+LLM disease prediction, Rasa chatbot integration, and Vue.js frontend with CPSU Mighty Hornbills branding (Earls Green & Lemon Yellow).

## 🚀 Quick Reference

**Most Common Tasks:**
```bash
# Start development (after first-time setup)
cd Django && python manage.py runserver          # Terminal 1
cd Rasa && rasa run actions                       # Terminal 2 (optional)
cd Rasa && rasa run --enable-api --cors "*"       # Terminal 3 (optional)

# Test ML prediction
curl -X POST http://localhost:8000/api/rasa/predict/ \
  -H "Content-Type: application/json" \
  -d '{"symptoms":["fever","cough"]}'

# Retrain ML model (after dataset changes)
cd ML/scripts && python train_model_realistic.py

# Run tests
cd Django && python manage.py test clinic
```

**Critical Files:**
- `Django/clinic/ml_service.py` — ML predictor (singleton pattern)
- `Django/clinic/llm_service.py` — LLM fallback chain  
- `Django/clinic/rasa_webhooks.py` — Rasa ↔ Django integration
- `Django/clinic/models.py` — CustomUser, SymptomRecord, EmergencyAlert, Medication, FollowUp
- `ML/scripts/train_model_realistic.py` — ML training pipeline
- `ML/models/disease_predictor_v2.pkl` — Trained ML model (must exist!)
- `Rasa/actions/actions.py` — Rasa custom actions (Django webhook calls)
- `Vue/src/services/api.ts` — Axios instance with token auto-injection

**Environment Setup:**
```bash
# Required for Django
GEMINI_API_KEY=...        # Optional (LLM features)
OPENROUTER_API_KEY=...    # Optional (LLM features)
COHERE_API_KEY=...        # Optional (LLM features)
```

## Big Picture Architecture

**System components (request flow):**

```
User (Vue.js) → Rasa Chatbot → Django REST API → Hybrid Prediction Engine
                      ↓                              ↓
              WebSocket/REST                 ┌───────────────────────┐
                                            │ 1. ML Model (scikit)  │ ← 85-95% accuracy
                                            │ 2. LLM Validation     │ ← Gemini/Grok/Cohere
                                            │ 3. Final Result       │ ← 90-98% accuracy
                                            └───────────────────────┘
                                                     ↓
                                        Response + Precautions + UI
```

**Directory structure:**
- `Vue/` — Frontend app (Vue 3 + Vite + TailwindCSS) with CPSU branding
- `Django/clinic/` — Main app: models, views, ML/LLM integration, Rasa webhooks
- `Django/health_assistant/` — Django project config, settings, URL routing
- `ML/` — Standalone ML training pipeline (generates `.pkl` models used by Django)
- `Rasa/` — Chatbot config (domain, intents, actions) - connects via webhook to Django
- `Django/docs/` — Complete API reference, architecture diagrams, deployment guides

**Critical data flows:**
1. **Rasa → Django ML**: Rasa calls `/api/rasa/predict/` webhook with symptoms → Django returns predictions
2. **ML Service**: Loads `.pkl` model from `ML/models/`, metadata CSVs from `ML/Datasets/active/`
3. **LLM Fallback**: Multi-provider chain (Gemini → Grok → Cohere) validates ML predictions
4. **Auth**: Custom user model with `school_id` (not username), token-based auth
5. **Database**: SQLite (dev) with `CustomUser`, `SymptomRecord`, `ChatSession`, `EmergencyAlert`, `Medication`, `FollowUp`
6. **Emergency System**: Students trigger SOS → staff receive real-time alerts → respond with actions
7. **Medication Tracking**: Staff prescribe → students log adherence → staff monitor compliance

## Critical Workflows

### First-Time Setup (Windows)
```bash
# 1. Create virtual environment (if not exists)
python -m venv venv
source venv/Scripts/activate  # Git Bash on Windows

# 2. Install dependencies
cd Django
pip install -r requirements.txt
cd ../Rasa
pip install -r requirements.txt

# 3. Create .env file (optional, for LLM features)
# Copy to Django/.env:
# GEMINI_API_KEY=your_key_here
# OPENROUTER_API_KEY=your_key_here
# COHERE_API_KEY=your_key_here

# 4. Train ML model (REQUIRED first time)
cd ../ML/scripts
python train_model_realistic.py  # Saves to ML/models/disease_predictor_v2.pkl

# 5. Setup database
cd ../../Django
python manage.py migrate
python manage.py createsuperuser  # Use school_id, not username!
```

### Start Django Server (Development)
```bash
cd Django
python manage.py runserver  # http://localhost:8000
```
**Prerequisites:**
1. ML model must exist: `ML/models/disease_predictor_v2.pkl` (train first if missing)
2. Database migrated: `python manage.py migrate`
3. Virtual environment activated: `source venv/Scripts/activate` (Git Bash on Windows)
4. Environment variables in `.env` (optional for LLM features):
   - `GEMINI_API_KEY`, `OPENROUTER_API_KEY`, `COHERE_API_KEY`

### Start Rasa Chatbot (Full Integration)
```bash
# 1. Train Rasa model (first time only, ~2-3 minutes)
cd Rasa
rasa train

# 2. Start Rasa action server (port 5055)
rasa run actions  # Terminal 1

# 3. Start Rasa chatbot (port 5005)
rasa run --enable-api --cors "*"  # Terminal 2

# Test: rasa shell (interactive testing)
```
**Rasa Features:** 132+ symptom synonyms, emergency detection, Django ML integration.  
Django falls back to direct LLM chat if Rasa unavailable.

### Train ML Model (Required First-Time Setup)
```bash
cd ML/scripts
python train_model_realistic.py  # 85-95% accuracy (recommended)
# OR
python train_model_v2.py         # May reach 100% on clean data
```
**Output:** Saves to `ML/models/disease_predictor*.pkl` (used by Django)
**Note:** If Django fails with "ML model not found" error, this step is required.
**Verification:** Check that `ML/models/disease_predictor_v2.pkl` exists after training.

### Run Tests
```bash
cd Django
python manage.py test clinic     # Django unit tests
# OR
pytest                            # If using pytest
```

### API Testing (Key Endpoints)
```bash
# Register user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"school_id":"2024-001","password":"pass123","name":"Test User"}'

# Rasa webhook (symptom prediction)
curl -X POST http://localhost:8000/api/rasa/predict/ \
  -H "Content-Type: application/json" \
  -d '{"symptoms":["fever","cough","fatigue"],"generate_insights":true}'

# Chat message (direct LLM)
curl -X POST http://localhost:8000/api/chat/message/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"I have fever and cough","session_id":"test-session"}'
```

### Start Vue.js Frontend (Development)
```bash
cd Vue
npm install              # First time only (or use install.bat/install.sh)
npm run dev              # http://localhost:5173 (Vite default)
```
**Prerequisites:**
1. Node.js 18+ installed
2. Django backend running on `http://localhost:8000`
3. Environment file `.env` already configured (included in repo)
   - `VITE_API_BASE_URL=http://localhost:8000/api`
   - `VITE_RASA_URL=http://localhost:5005` (optional)

**Quick Install:** Run `install.bat` (Windows) or `install.sh` (Linux/Mac) for automated setup.  
**Architecture:** Vue 3 + TypeScript + Vite + TailwindCSS + Pinia (state management) + Vue Router

## Project-Specific Patterns

### Custom Authentication (Not Django Default!)
**Pattern:** Uses `school_id` instead of `username` for login.

```python
# Django/clinic/models.py
class CustomUser(AbstractBaseUser):
    school_id = models.CharField(unique=True)  # PRIMARY AUTH FIELD
    USERNAME_FIELD = 'school_id'
    
# Login API
user = authenticate(username=school_id, password=password)  # username param but school_id value!
```
**When creating users:** Always use `school_id`, never `username`.

### Hybrid ML+LLM Prediction Pattern
**File:** `Django/clinic/rasa_webhooks.py` (lines 50-80)

```python
# 1. Fast ML prediction (local model)
ml_result = predictor.predict(symptoms)  # <100ms

# 2. LLM validation (optional, FREE tier)
if generate_insights:
    llm_validation = llm_validator.validate_ml_prediction(
        symptoms, ml_result['predicted_disease'], ml_result['confidence']
    )
    # Boost confidence if LLM agrees (+5-12%)
    if llm_validation['agrees_with_ml']:
        final_confidence += llm_validation['confidence_boost']
```
**Cost:** $0/month (using free tiers). **Never** add paid LLM calls without explicit request.

### LLM Multi-Provider Fallback Chain
**File:** `Django/clinic/llm_service.py` (AIInsightGenerator class)

```python
# Provider priority (all FREE tier):
1. Gemini 2.5 Flash       → Fast, reliable (Google)
2. Qwen 3 (OpenRouter)    → Fast, free alternative
3. Grok 2 (Groq)          → Fast inference
4. Cohere                 → Final fallback

# Pattern: Try next provider on failure
for provider in providers:
    try:
        return provider.generate(prompt)
    except Exception:
        continue  # Auto-fallback
```
**Environment:** Providers initialize only if API key present (graceful degradation).

### Model Serialization Format (ML → Django Integration)
**Pattern:** All ML training scripts save models with metadata.

```python
# ML/scripts/train_model_*.py
model_data = {
    'model': trained_model,        # sklearn classifier
    'feature_names': symptom_list  # 132 symptoms (exact names)
}
pickle.dump(model_data, open('disease_predictor.pkl', 'wb'))

# Django/clinic/ml_service.py loads it:
model_data = pickle.load(open(settings.ML_MODEL_PATH, 'rb'))
self.model = model_data['model']
self.feature_names = model_data['feature_names']
```
**Critical:** Feature names must match CSV columns exactly (`fever`, `cough`, not `Fever`).

### Rasa → Django Webhook Integration
**Pattern:** Rasa sends symptoms to Django for ML prediction during conversations.

```python
# Rasa/actions/actions.py (when implemented)
response = requests.post(
    'http://localhost:8000/api/rasa/predict/',
    json={'symptoms': extracted_symptoms, 'sender_id': sender_id}
)

# Django/clinic/rasa_webhooks.py
@api_view(['POST'])
@permission_classes([AllowAny])  # Rasa webhook - no auth required
def rasa_webhook_predict(request):
    symptoms = request.data['symptoms']
    return Response(predictor.predict(symptoms))
```
**Security Note:** Webhook is AllowAny for Rasa access. In production, add API key validation.

### Settings Path Resolution (ML Models)
**File:** `Django/health_assistant/settings.py`

```python
BASE_DIR = Path(__file__).parent.parent  # Django/
ML_MODEL_PATH = BASE_DIR.parent / 'ML' / 'models' / 'disease_predictor_v2.pkl'
ML_DATASETS_PATH = BASE_DIR.parent / 'ML' / 'Datasets' / 'active'
```
**Pattern:** Django settings point to sibling `ML/` directory (not Django subdirectory).

### Singleton Service Pattern
**Pattern:** All services use singleton pattern to avoid reloading heavy resources.

```python
# Django/clinic/ml_service.py
_ml_predictor_instance = None

def get_ml_predictor():
    """Get singleton ML predictor instance"""
    global _ml_predictor_instance
    if _ml_predictor_instance is None:
        _ml_predictor_instance = MLPredictor()  # Loads model once
    return _ml_predictor_instance

# Django/clinic/llm_service.py
class AIInsightGenerator:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance  # Reuses same instance
```
**Critical:** Always use `get_ml_predictor()` function, never instantiate `MLPredictor()` directly.
Models are loaded once at first call (~2-3 seconds), then cached for all requests.

### Emergency Alert System (SOS Feature)
**Pattern:** Real-time emergency response system for medical emergencies.

```python
# Django/clinic/models.py
class EmergencyAlert(models.Model):
    URGENCY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)  # Building, room number
    symptoms = models.TextField()
    urgency_level = models.CharField(max_length=10, choices=URGENCY_CHOICES)
    is_resolved = models.BooleanField(default=False)
    responded_by = models.ForeignKey(CustomUser, related_name='emergency_responses')
    
# Trigger emergency (student)
POST /api/emergency/trigger/
{"location": "Engineering Building - Room 301", "symptoms": "chest pain", "urgency_level": "high"}

# Staff dashboard shows all active emergencies with color-coding
GET /api/emergency/active/  # Staff permission required
```

**Frontend Integration:** `Vue/src/views/staff/EmergencyDashboard.vue` displays real-time alerts with urgency color coding (red=critical, orange=high, yellow=medium).

### Medication Management System
**Pattern:** Complete prescription, logging, and adherence tracking workflow.

```python
# Django/clinic/models.py
class Medication(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    medication_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)  # "500mg", "2 tablets"
    frequency = models.CharField(max_length=100)  # "Twice daily", "Every 8 hours"
    start_date = models.DateField()
    end_date = models.DateField()
    prescribed_by = models.ForeignKey(CustomUser, related_name='prescribed_medications')
    special_instructions = models.TextField(blank=True)
    
class MedicationLog(models.Model):
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    taken_at = models.DateTimeField()
    notes = models.TextField(blank=True)
    
# Workflow:
# 1. Staff prescribes medication
POST /api/medications/prescribe/
{"student_id": 123, "medication_name": "Amoxicillin", "dosage": "500mg", 
 "frequency": "3 times daily", "duration_days": 7}

# 2. Student logs when they take medication
POST /api/medications/{id}/log/
{"taken_at": "2026-02-16T08:30:00Z", "notes": "Taken with breakfast"}

# 3. Staff monitors adherence rates
GET /api/medications/adherence/summary/
# Returns: {"adherence_rate": 85.5, "missed_doses": 3, "total_doses": 21}
```

**Frontend Integration:** 
- `Vue/src/views/staff/MedicationPrescribe.vue` - Staff prescription form
- `Vue/src/views/staff/AdherenceMonitor.vue` - Visual adherence analytics
- `Vue/src/views/MedicationList.vue` - Student view of active medications

### Follow-Up Appointment System
**Pattern:** Scheduled appointment tracking with status management.

```python
# Django/clinic/models.py
class FollowUp(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('missed', 'Missed'),
    ]
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    scheduled_date = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    scheduled_by = models.ForeignKey(CustomUser, related_name='scheduled_followups')
    completion_notes = models.TextField(blank=True)
    
    # Manager with helper queries
    objects = FollowUpManager()  # Has methods: upcoming(), overdue(), completed_last_month()
    
# Schedule follow-up (staff)
POST /api/followups/schedule/
{"student_id": 123, "scheduled_date": "2026-02-20T10:00:00Z", 
 "reason": "Check medication effectiveness"}

# Complete follow-up with notes (staff)
POST /api/followups/{id}/complete/
{"completion_notes": "Student reports improvement. Continue current medication."}

# Student views upcoming appointments
GET /api/followups/  # Auto-filtered by user role
```

**Frontend Integration:** `Vue/src/views/staff/FollowUpManagement.vue` with calendar view and automated reminders.

## Key Files & Their Roles

**Django Backend:**
- `clinic/models.py` — CustomUser (school_id auth), SymptomRecord, ChatSession, EmergencyAlert, Medication, MedicationLog, FollowUp, AuditLog
- `clinic/views.py` — 30+ REST endpoints (auth, symptoms, chat, emergency, medication, follow-ups, staff features)
- `clinic/ml_service.py` — MLPredictor class (singleton), loads `.pkl` model + metadata CSVs
- `clinic/llm_service.py` — AIInsightGenerator (singleton), multi-provider LLM chain
- `clinic/rasa_webhooks.py` ⭐ — `/api/rasa/predict/` webhook for Rasa integration
- `clinic/rasa_service.py` — RasaChatService (singleton), talks to Rasa REST API
- `clinic/serializers.py` — DRF serializers for all models (20+ serializers)
- `clinic/permissions.py` — IsStudent, IsClinicStaff, IsOwnerOrStaff, CanModifyProfile
- `clinic/urls.py` — URL routing for all API endpoints
- `health_assistant/settings.py` — ML_MODEL_PATH, LLM API keys, RASA_SERVER_URL
- `health_assistant/urls.py` — Root URL config (`/api/`, `/admin/`)

**ML Training Pipeline:**
- `ML/Datasets/active/train.csv` — 4,920 samples, 132 binary symptom columns + prognosis
- `ML/Datasets/active/test.csv` — 42 samples (same schema)
- `ML/Datasets/active/Symptom-severity.csv` — symptom → weight (1-7)
- `ML/Datasets/active/symptom_Description.csv` — disease → description text
- `ML/Datasets/active/symptom_precaution.csv` — disease → 4 precautions
- `ML/scripts/train_model_realistic.py` ⭐ — 85-95% accuracy (adds 5% noise)
- `ML/scripts/train_model_v2.py` — Enhanced model (clean data, may hit 100%)
- `ML/scripts/predict.py` — Standalone CLI prediction tool
- `ML/scripts/test_model.py` — Quick model validation
- `ML/models/disease_predictor_v2.pkl` — Trained model (generated by training scripts)

**Rasa Chatbot (Fully Configured!):**
- `Rasa/domain.yml` ⭐ — Health intents, symptom entities, medical responses
- `Rasa/actions/actions.py` ⭐ — Django ML integration, emergency detection
- `Rasa/data/nlu.yml` ⭐ — 132 symptoms with 400+ synonym mappings
- `Rasa/data/stories.yml` — Medical conversation flows
- `Rasa/data/rules.yml` — Emergency responses, fallbacks
- `Rasa/config.yml` — Medical domain-optimized NLU pipeline
- `Rasa/README.md` — Complete setup and testing guide
- `Rasa/TESTING_GUIDE.md` — Test scenarios and examples

**Helper Scripts:**
- `scripts/start_rasa.sh` — Interactive script to check/start Django + Rasa services
- `docs/guides/RASA_COMMANDS.md` — Quick reference for common Rasa commands

**Documentation (read these!):**
- `Django/docs/DOCUMENTATION_INDEX.md` — Complete navigation guide
- `Django/docs/architecture/HYBRID_ML_LLM_SYSTEM.md` — How hybrid system works
- `Django/docs/architecture/RASA_ML_FLOW.md` — Request flow diagrams
- `Django/docs/api/API_DOCS.md` — All endpoint specs with examples
- `ML/docs/QUICKSTART.md` — ML training workflow
- `ML/docs/DATASET_USAGE.md` — Which datasets are active/archived

**Vue.js Frontend:**
- `Vue/src/views/` — Student pages (Home, Dashboard, SymptomChecker, Chat, History, Profile, Medications, FollowUps, HealthDashboard)
- `Vue/src/views/staff/` — Staff pages (StaffDashboard, EmergencyDashboard, StudentRecords, MedicationPrescribe, AdherenceMonitor, FollowUpManagement, AnalyticsDashboard)
- `Vue/src/stores/` — Pinia stores (auth, symptoms, chat)
- `Vue/src/services/api.ts` — Axios instance with auto token injection
- `Vue/src/types/index.ts` — TypeScript type definitions
- `Vue/src/router/index.ts` — Vue Router with role-based auth guards (student/staff)
- `Vue/README.md` — Complete frontend documentation

## CPSU Branding & Design System

**Official Colors (Mighty Hornbills):**
- **Earls Green** (Primary): `#006B3F` — Represents tenacity and courage
  - Hex: `#006B3F`
  - RGB: `rgb(0, 107, 63)`
  - Tailwind: Create custom color `cpsu-green`
  
- **Lemon Yellow** (Secondary): `#FFF44F` — Represents vibrant energy
  - Hex: `#FFF44F`
  - RGB: `rgb(255, 244, 79)`
  - Tailwind: Create custom color `cpsu-yellow`

**Brand Usage:**
- Primary actions, headers, navigation → Earls Green
- Accents, highlights, CTAs → Lemon Yellow
- Text on Earls Green → White or Lemon Yellow
- Text on Lemon Yellow → Earls Green or dark gray
- Maintain WCAG AA contrast ratios (4.5:1 minimum)

**Typography:**
- Headers: Bold, modern sans-serif (Inter, Poppins recommended)
- Body: Clean, readable sans-serif (Inter, system fonts)
- Medical content: Professional, clear typography

**UI Patterns:**
- Health dashboard: Cards with green borders, yellow accents
- Symptom checker: Step-by-step forms with green progress indicators
- Chat interface: Green header, yellow user messages, white bot responses
- Emergency alerts: Red with yellow highlights

## How to Help

**Adding Django features:**
1. Models → `clinic/models.py` (extend CustomUser, SymptomRecord, etc.)
2. Serializers → `clinic/serializers.py` (follow DRF patterns)
3. Views → `clinic/views.py` or new viewset
4. URLs → `clinic/urls.py` (register routes)
5. Migrations → `python manage.py makemigrations` after model changes
6. Tests → `clinic/tests.py` (use Django TestCase)

**Modifying ML training:**
1. Create new script in `ML/scripts/` (follow `train_model_v2.py` pattern)
2. Models must save to `../models/*.pkl` with `{'model': ..., 'feature_names': ...}` format
3. Test with `python test_model.py` after training
4. Update `ML/README.md` with usage instructions

**Integrating new LLM provider:**
1. Add API key to `.env` and `settings.py`
2. Extend `AIInsightGenerator` in `clinic/llm_service.py`
3. Add to fallback chain in `validate_ml_prediction()` method
4. Test with `/api/rasa/predict/?generate_insights=true`

**Extending Rasa chatbot:**
1. Add intents/entities to `Rasa/domain.yml`
2. Training data to `Rasa/data/nlu.yml`
3. Custom actions to `Rasa/actions/actions.py`
4. Train: `rasa train` (creates model in `Rasa/models/`)
5. Test conversations: `rasa shell` or `rasa interactive`

**Dataset changes:**
1. Modify files in `ML/Datasets/active/` only
2. Update metadata JSON if schema changes
3. Re-train model: `cd ML/scripts && python train_model_realistic.py`
4. Restart Django server to reload model

**Working with Vue.js frontend:**
1. **Pages** → `Vue/src/views/` (use Vue 3 Composition API with `<script setup>`)
2. **State** → Use Pinia stores in `Vue/src/stores/` (auth, symptoms, chat)
3. **API calls** → Import `api` from `@/services/api` (tokens auto-injected)
4. **Types** → Import from `@/types` (User, Symptom, PredictionResult, etc.)
5. **Routing** → Add routes to `Vue/src/router/index.ts` with proper meta guards
6. **Styling** → Use TailwindCSS classes with CPSU colors (`cpsu-green`, `cpsu-yellow`)
7. **Reusable classes** → `.btn-primary`, `.btn-secondary`, `.btn-outline`, `.card`, `.card-bordered`, `.input-field`
8. **Testing** → Run Django backend first, then `npm run dev` in Vue folder

## Examples

**Add new Django API endpoint:**
```python
# clinic/views.py
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_new_endpoint(request):
    return Response({'data': 'value'})

# clinic/urls.py
urlpatterns = [
    path('my-endpoint/', views.my_new_endpoint, name='my-endpoint'),
]
```

**Use ML predictor in custom view:**
```python
from .ml_service import get_ml_predictor

def my_prediction_view(request):
    predictor = get_ml_predictor()  # Singleton instance
    result = predictor.predict(['fever', 'cough'])
    return Response(result)
```

**Add LLM validation to custom logic:**
```python
from .llm_service import AIInsightGenerator

ai_gen = AIInsightGenerator()  # Singleton
validation = ai_gen.validate_ml_prediction(
    symptoms=['fever', 'cough'],
    ml_prediction='Common Cold',
    ml_confidence=0.85
)
# validation = {'agrees': True, 'confidence_boost': 0.08, ...}
```

**Test API with authentication:**
```bash
# 1. Register/login to get token
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"school_id":"2024-001","password":"test123"}' | jq -r '.token')

# 2. Use token in authenticated request
curl -X GET http://localhost:8000/api/profile/ \
  -H "Authorization: Token $TOKEN"
```

**Quick start with helper script:**
```bash
# Check system status and start services
bash start_rasa.sh  # Interactive menu for Rasa setup
```

**Vue.js API integration example:**
```typescript
// Vue/src/services/api.ts (TypeScript)
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add auth token to requests
api.interceptors.request.use(config => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    config.headers.Authorization = `Token ${token}`
  }
  return config
})

export default api
```

**Vue component with CPSU branding:**
```vue
<!-- Vue/src/components/HealthCard.vue -->
<template>
  <div class="bg-white rounded-lg border-2 border-cpsu-green shadow-lg p-6">
    <h2 class="text-2xl font-bold text-cpsu-green mb-4">{{ title }}</h2>
    <div class="space-y-2">
      <slot></slot>
    </div>
    <button class="mt-4 bg-cpsu-yellow text-cpsu-green font-semibold px-6 py-2 rounded-lg hover:bg-yellow-400 transition">
      {{ actionText }}
    </button>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  actionText: { type: String, default: 'Continue' }
})
</script>
```

**TailwindCSS config with CPSU colors:**
```javascript
// Vue/tailwind.config.js
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        'cpsu-green': '#006B3F',         // Earls Green - Primary
        'cpsu-yellow': '#FFF44F',        // Lemon Yellow - Secondary
        'cpsu-green-dark': '#004d2d',    // Darker shade for hover states
        'cpsu-yellow-dark': '#e6db3d',   // Darker yellow for hover
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        heading: ['Poppins', 'Inter', 'sans-serif'],
      }
    }
  },
  plugins: []
}
```

## Complete API Endpoint Reference

**Authentication** (`/api/auth/`):
- `POST /auth/register/` — Register new user (student/staff)
- `POST /auth/login/` — Login with school_id + password → returns token
- `POST /auth/logout/` — Logout (invalidates token)

**User Profile** (`/api/profile/`):
- `GET /profile/` — Get current user profile
- `PUT /profile/` — Update profile (name, department, cpsu_address only)
- `PATCH /profile/` — Partial update profile
- `POST /profile/consent/` — Update data consent

**Symptoms & Prediction** (`/api/symptoms/`):
- `POST /symptoms/submit/` — Submit symptoms → get ML+LLM prediction
- `GET /symptoms/available/` — List all 132 available symptoms
- `GET /symptoms/` — List user's symptom history (ViewSet)
- `GET /symptoms/{id}/` — Get specific symptom record
- `DELETE /symptoms/{id}/` — Delete symptom record

**Rasa Webhooks** (`/api/rasa/`) - **AllowAny permission**:
- `POST /rasa/predict/` — ML prediction webhook for Rasa
- `GET /rasa/symptoms/` — Get symptom list for Rasa

**Chat** (`/api/chat/`) - Direct LLM fallback:
- `POST /chat/start/` — Start chat session
- `POST /chat/message/` — Send message → get LLM response
- `POST /chat/insights/` — Generate health insights
- `POST /chat/end/` — End chat session

**Emergency SOS** (`/api/emergency/`) - Students & Staff:
- `POST /emergency/trigger/` — Student triggers emergency alert (location, symptoms, urgency)
- `GET /emergency/active/` — Get active emergencies (staff: all, student: own)
- `GET /emergency/history/` — Get emergency history
- `POST /emergency/{id}/respond/` — Staff responds to emergency with action notes

**Medication Management** (`/api/medications/`) - Students & Staff:
- `POST /medications/prescribe/` — Staff prescribes medication to student
- `GET /medications/` — List medications (staff: all, student: own)
- `GET /medications/{id}/` — Get medication details
- `PUT /medications/{id}/` — Update medication
- `POST /medications/{id}/log/` — Student logs medication adherence
- `GET /medications/{id}/logs/` — Get adherence logs
- `GET /medications/adherence/summary/` — Get adherence statistics

**Follow-Up Appointments** (`/api/followups/`) - Students & Staff:
- `POST /followups/schedule/` — Staff schedules follow-up appointment
- `GET /followups/` — List follow-ups (staff: all, student: own)
- `GET /followups/{id}/` — Get follow-up details
- `PUT /followups/{id}/` — Update follow-up
- `POST /followups/{id}/complete/` — Staff marks follow-up as completed
- `POST /followups/{id}/cancel/` — Cancel follow-up appointment

**Staff Only** (`/api/staff/`) - **IsClinicStaff permission**:
- `GET /staff/dashboard/` — Dashboard stats (total students, conditions, trends)
- `GET /staff/students/` — Student directory with health records
- `GET /staff/analytics/` — Advanced analytics (disease trends, emergency patterns, medication adherence)
- `GET /staff/export/` — Export reports (CSV/Excel)

## Common Troubleshooting

**"ML model not found" error:**
```bash
cd ML/scripts && python train_model_realistic.py
# Verify: ML/models/disease_predictor_v2.pkl exists
```

**Django won't start:**
```bash
source venv/Scripts/activate  # Activate virtual environment first
cd Django && python manage.py migrate  # Run migrations
python manage.py runserver
```

**Rasa not connecting to Django:**
- Verify Django is running on `http://localhost:8000`
- Check `RASA_SERVER_URL` in `Django/health_assistant/settings.py`
- Test webhook: `curl -X POST http://localhost:8000/api/rasa/predict/ -H "Content-Type: application/json" -d '{"symptoms":["fever"]}'`

**LLM validation failing:**
- Check `.env` file has API keys (`GEMINI_API_KEY`, `OPENROUTER_API_KEY`, `COHERE_API_KEY`)
- LLM is optional - system works without it (ML-only mode)
- Test with: `curl -X POST http://localhost:8000/api/rasa/predict/ -d '{"symptoms":["fever"],"generate_insights":true}'`

**Vue.js can't connect to backend:**
- Verify Django is running on `http://localhost:8000`
- Check `.env` has `VITE_API_BASE_URL=http://localhost:8000/api`
- Check browser console for CORS errors (CORS is enabled by default)

**Database migrations failing:**
```bash
cd Django
python manage.py makemigrations clinic
python manage.py migrate
```

## What NOT to Do

- **Do not use `username` field** — this project uses `school_id` for authentication
- **Do not modify `AUTH_USER_MODEL`** — CustomUser is deeply integrated
- **Do not hard-code symptom/disease names** — always load from model/datasets
- **Do not add paid LLM providers** — stick to FREE tier (Gemini/Grok/Cohere)
- **Do not skip migrations** — run `makemigrations` + `migrate` after model changes
- **Do not modify `ML/Datasets/archive/`** — historical data only
- **Do not change model pickle format** — breaks Django integration
- **Do not bypass role-based permissions** — always use `IsStudent`, `IsClinicStaff` in views
- **Do not store sensitive health data in plain text** — follows HIPAA-like privacy patterns
- **Do not delete EmergencyAlert records** — audit trail required for safety

## When Uncertain

Ask:
- "Should this be a Django view, viewset, or API view?" (views.py has examples of all patterns)
- "Does this need authentication?" (check `permissions.py` for IsStudent, IsClinicStaff, etc.)
- "Should I retrain the ML model?" (yes if datasets change, no if only Django code changes)
- "Is this LLM provider FREE tier?" (verify before adding new providers)
- "Where should tests go?" (`clinic/tests.py` for Django, `ML/scripts/test_model.py` for ML)
