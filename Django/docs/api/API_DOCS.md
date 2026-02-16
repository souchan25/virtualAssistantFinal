# API Documentation - CPSU Health Assistant

Complete REST API reference for the Virtual Health Assistant backend.

## Base URL
```
Development: http://localhost:8000/api/
Production: https://your-domain.com/api/
```

## Authentication

All endpoints (except registration and login) require authentication via Token.

**Header:**
```
Authorization: Token <your-auth-token>
```

---

## 📍 Endpoints Overview

| Category | Method | Endpoint | Permission |
|----------|--------|----------|-----------|
| **Auth** | POST | `/auth/register/` | AllowAny |
| | POST | `/auth/login/` | AllowAny |
| | POST | `/auth/logout/` | Authenticated |
| **Profile** | GET | `/profile/` | Authenticated |
| | PATCH | `/profile/` | Owner |
| | POST | `/profile/consent/` | Authenticated |
| **Symptoms** | POST | `/symptoms/submit/` | Student + Consent |
| | GET | `/symptoms/` | Student (own) / Staff (all) |
| | GET | `/symptoms/available/` | Authenticated |
| **AI Chat** | POST | `/chat/start/` | Student + Consent |
| | POST | `/chat/message/` | Student + Consent |
| | POST | `/chat/insights/` | Student + Consent |
| | POST | `/chat/end/` | Student |
| **Staff** | GET | `/staff/dashboard/` | Staff Only |
| | GET | `/staff/students/` | Staff Only |
| | GET | `/staff/export/` | Staff Only |
| **Audit** | GET | `/audit/` | Staff Only |

---

## 🔐 Authentication Endpoints

### Register User
Create a new student or staff account.

**Endpoint:** `POST /api/auth/register/`

**Request Body:**
```json
{
  "school_id": "2024-001",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!",
  "name": "Juan Dela Cruz",
  "department": "Computer Science",
  "cpsu_address": "Dorm 1, Room 205",
  "data_consent_given": true
}
```

**Response (201 Created):**
```json
{
  "token": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0",
  "user": {
    "school_id": "2024-001",
    "name": "Juan Dela Cruz",
    "department": "Computer Science",
    "cpsu_address": "Dorm 1, Room 205",
    "role": "student",
    "data_consent_given": true,
    "consent_date": "2025-10-29T10:30:00Z",
    "date_joined": "2025-10-29T10:30:00Z"
  },
  "message": "Registration successful"
}
```

**Validation Rules:**
- `school_id`: Required, unique, max 20 chars
- `password`: Min 8 chars, must match `password_confirm`
- `name`: Required, max 150 chars
- `department`: Required
- `role`: Auto-set to "student" (staff requires admin approval)

---

### Login
Authenticate and receive auth token.

**Endpoint:** `POST /api/auth/login/`

**Request Body:**
```json
{
  "school_id": "2024-001",
  "password": "SecurePass123!"
}
```

**Response (200 OK):**
```json
{
  "token": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0",
  "user": {
    "school_id": "2024-001",
    "name": "Juan Dela Cruz",
    "role": "student",
    ...
  },
  "message": "Login successful"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "error": "Invalid credentials"
}
```

---

### Logout
Invalidate current auth token.

**Endpoint:** `POST /api/auth/logout/`

**Headers:**
```
Authorization: Token <your-token>
```

**Response (200 OK):**
```json
{
  "message": "Logout successful"
}
```

---

## 👤 Profile Endpoints

### Get Profile
Retrieve current user's profile.

**Endpoint:** `GET /api/profile/`

**Response (200 OK):**
```json
{
  "school_id": "2024-001",
  "name": "Juan Dela Cruz",
  "department": "Computer Science",
  "cpsu_address": "Dorm 1, Room 205",
  "role": "student",
  "data_consent_given": true,
  "consent_date": "2025-10-29T10:30:00Z",
  "date_joined": "2025-10-29T10:30:00Z"
}
```

---

### Update Profile
Modify editable fields (name, department, cpsu_address).

**Endpoint:** `PATCH /api/profile/`

**Request Body:**
```json
{
  "name": "Juan P. Dela Cruz",
  "department": "Information Technology",
  "cpsu_address": "Off-Campus"
}
```

**Response (200 OK):**
```json
{
  "school_id": "2024-001",
  "name": "Juan P. Dela Cruz",
  "department": "Information Technology",
  ...
}
```

**⚠️ Immutable Fields (will return 400 error):**
- `school_id`
- `role`

---

### Update Data Consent
Grant or revoke health data storage consent.

**Endpoint:** `POST /api/profile/consent/`

**Request Body:**
```json
{
  "data_consent_given": true
}
```

**Response (200 OK):**
```json
{
  "message": "Consent granted",
  "data_consent_given": true,
  "consent_date": "2025-10-29T11:00:00Z"
}
```

**Note:** Revoking consent prevents symptom submission and AI features.

---

## 💊 Symptom & ML Endpoints

### Submit Symptoms
Submit symptoms and get ML disease prediction.

**Endpoint:** `POST /api/symptoms/submit/`

**Permission:** Student role + data consent required

**Request Body:**
```json
{
  "symptoms": ["continuous_sneezing", "shivering", "chills", "high_fever"],
  "duration_days": 3,
  "severity": 2,
  "on_medication": false,
  "medication_adherence": null
}
```

**Parameters:**
- `symptoms`: Array of symptom names (from available symptoms list)
- `duration_days`: Integer ≥ 1
- `severity`: 1 (Mild), 2 (Moderate), 3 (Severe)
- `on_medication`: Boolean
- `medication_adherence`: Boolean or null

**Response (201 Created):**
```json
{
  "record_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "prediction": {
    "predicted_disease": "Common Cold",
    "confidence_score": 0.85,
    "top_predictions": [
      {"disease": "Common Cold", "confidence": 0.85},
      {"disease": "Influenza", "confidence": 0.12},
      {"disease": "Allergy", "confidence": 0.03}
    ],
    "description": "The common cold is a viral infection of your nose and throat...",
    "precautions": [
      "drink vitamin c rich drinks",
      "take vapour",
      "avoid cold food",
      "keep fever in check"
    ],
    "matched_symptoms": ["continuous_sneezing", "shivering", "chills", "high_fever"],
    "is_communicable": true,
    "is_acute": true,
    "icd10_code": "J00"
  },
  "requires_referral": false,
  "referral_message": null
}
```

**Referral Trigger:**
If student has submitted 5+ reports in past 30 days:
```json
{
  "requires_referral": true,
  "referral_message": "You have reported symptoms 5+ times in the past 30 days. Please visit the clinic for evaluation."
}
```

---

### Get Available Symptoms
List all 132 symptoms the ML model recognizes.

**Endpoint:** `GET /api/symptoms/available/`

**Response (200 OK):**
```json
{
  "count": 132,
  "symptoms": [
    "abdominal_pain",
    "abnormal_menstruation",
    "acidity",
    ...
    "yellow_urine",
    "yellowing_of_eyes",
    "yellowish_skin"
  ]
}
```

---

### List Symptom Records
Retrieve symptom submission history.

**Endpoint:** `GET /api/symptoms/`

**Query Parameters:**
- `start_date`: Filter by created date (YYYY-MM-DD)
- `end_date`: Filter by end date

**Student Response (200 OK) - Own records only:**
```json
[
  {
    "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "student": 1,
    "student_school_id": "2024-001",
    "student_name": "Juan Dela Cruz",
    "symptoms": ["fever", "cough", "headache"],
    "duration_days": 3,
    "severity": 2,
    "predicted_disease": "Common Cold",
    "confidence_score": 0.85,
    "top_predictions": [...],
    "on_medication": false,
    "medication_adherence": null,
    "is_communicable": true,
    "is_acute": true,
    "icd10_code": "J00",
    "requires_referral": false,
    "referral_triggered": false,
    "referral_date": null,
    "created_at": "2025-10-29T12:00:00Z",
    "updated_at": "2025-10-29T12:00:00Z"
  }
]
```

**Staff Response:** All students' records with filtering.

---

## 🤖 AI Chat Endpoints

### Start Chat Session
Begin a new AI conversation session.

**Endpoint:** `POST /api/chat/start/`

**Permission:** Student + consent required

**Request Body:**
```json
{
  "language": "english"
}
```

**Languages:** `english`, `filipino`, `tagalog`, `cebuano`

**Response (201 Created):**
```json
{
  "session_id": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
  "message": "Chat session started",
  "language": "english"
}
```

---

### Send Chat Message
Send message and get AI response (real-time, not stored).

**Endpoint:** `POST /api/chat/message/`

**Request Body:**
```json
{
  "session_id": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
  "message": "I have fever and cough for 3 days",
  "language": "english"
}
```

**Response (200 OK):**
```json
{
  "response": "Thank you for sharing. Based on your symptoms (fever and cough for 3 days), I recommend consulting with a healthcare professional. Have you tried any home remedies yet?",
  "session_id": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d"
}
```

**Note:** Conversation history is NOT stored (privacy requirement).

---

### Generate Health Insights
Create top 3 AI-generated insights for current session.

**Endpoint:** `POST /api/chat/insights/`

**Request Body:**
```json
{
  "session_id": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
  "symptoms": ["fever", "cough", "headache"],
  "disease": "Common Cold"
}
```

**Response (200 OK):**
```json
[
  {
    "id": "insight-uuid-1",
    "session_id": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
    "insight_text": "Monitor your symptoms closely. If fever exceeds 38.5°C or persists beyond 3 days, seek medical attention.",
    "references": [
      "WHO Disease Guidelines 2024",
      "Mayo Clinic Symptom Checker"
    ],
    "reliability_score": 0.92,
    "generated_at": "2025-10-29T12:30:00Z"
  },
  {
    "id": "insight-uuid-2",
    "insight_text": "Stay well-hydrated with 8-10 glasses of water daily. Adequate hydration supports immune function and recovery.",
    "references": [
      "CDC Health Recommendations",
      "Johns Hopkins Medicine"
    ],
    "reliability_score": 0.88,
    "generated_at": "2025-10-29T12:30:01Z"
  },
  {
    "id": "insight-uuid-3",
    "insight_text": "Get 7-9 hours of sleep. Rest is crucial for your immune system to fight the infection effectively.",
    "references": [
      "National Sleep Foundation",
      "CPSU Clinic Guidelines"
    ],
    "reliability_score": 0.85,
    "generated_at": "2025-10-29T12:30:02Z"
  }
]
```

**Note:** Only top 3 insights per session. Old insights are deleted when new ones are generated.

---

### End Chat Session
Mark session as ended and calculate duration.

**Endpoint:** `POST /api/chat/end/`

**Request Body:**
```json
{
  "session_id": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d"
}
```

**Response (200 OK):**
```json
{
  "message": "Session ended",
  "duration_seconds": 450
}
```

---

## 🏥 Clinic Staff Endpoints

### Dashboard Overview
Get clinic statistics and analytics.

**Endpoint:** `GET /api/staff/dashboard/`

**Permission:** Staff role only

**Response (200 OK):**
```json
{
  "total_students": 500,
  "students_with_symptoms_today": 12,
  "students_with_symptoms_7days": 45,
  "students_with_symptoms_30days": 120,
  "top_insight": "Common Cold (25 cases)",
  "department_breakdown": [
    {
      "department": "Computer Science",
      "total_students": 100,
      "students_with_symptoms": 18,
      "percentage_with_symptoms": 18.0,
      "top_diseases": [
        {"disease": "Common Cold", "count": 8},
        {"disease": "Flu", "count": 5}
      ],
      "communicable_count": 12,
      "non_communicable_count": 6,
      "acute_count": 15,
      "chronic_count": 3,
      "referral_pending_count": 1
    },
    ...
  ],
  "recent_symptoms": [
    {
      "id": "uuid",
      "student_school_id": "2024-001",
      "predicted_disease": "Common Cold",
      "created_at": "2025-10-29T14:00:00Z",
      ...
    }
  ],
  "pending_referrals": 3
}
```

---

### Student Directory
Search and filter student health records.

**Endpoint:** `GET /api/staff/students/`

**Query Parameters:**
- `department`: Filter by department name
- `search`: Search by name or school_id
- `has_symptoms`: Filter students with symptoms (`true`/`false`)

**Example:** `GET /api/staff/students/?department=Computer Science&has_symptoms=true`

**Response (200 OK):**
```json
[
  {
    "school_id": "2024-001",
    "name": "Juan Dela Cruz",
    "department": "Computer Science",
    "cpsu_address": "Dorm 1",
    "data_consent_given": true,
    "date_joined": "2025-10-01T10:00:00Z"
  },
  ...
]
```

---

### Export Report
Export symptom data for analysis.

**Endpoint:** `GET /api/staff/export/`

**Query Parameters:**
- `start_date`: Filter from date (YYYY-MM-DD)
- `end_date`: Filter to date (YYYY-MM-DD)

**Response (200 OK):**
```json
{
  "message": "Export functionality - implement Excel generation",
  "record_count": 150,
  "data": [
    {
      "id": "uuid",
      "student_school_id": "2024-001",
      "symptoms": ["fever", "cough"],
      ...
    }
  ]
}
```

**TODO:** Implement Excel/CSV export using `openpyxl` or `pandas`.

---

### View Audit Logs
Access security audit trail.

**Endpoint:** `GET /api/audit/`

**Query Parameters:**
- `action`: Filter by action type (login, create, export, etc.)
- `school_id`: Filter by user school_id
- `start_date`: Filter from date

**Response (200 OK):**
```json
[
  {
    "id": "uuid",
    "user": 1,
    "user_school_id": "2024-001",
    "action": "login",
    "model_name": "",
    "object_id": "",
    "changes": {},
    "timestamp": "2025-10-29T10:30:00Z",
    "ip_address": "192.168.1.100",
    "user_agent": "Mozilla/5.0...",
    "success": true,
    "error_message": ""
  },
  ...
]
```

---

## 🚨 Error Responses

### Standard Error Format
```json
{
  "error": "Error message description",
  "detail": "Additional details if available"
}
```

### Common Status Codes

| Code | Meaning | When |
|------|---------|------|
| 200 | OK | Successful GET/POST |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Validation error, missing fields |
| 401 | Unauthorized | Missing/invalid auth token |
| 403 | Forbidden | No permission for resource |
| 404 | Not Found | Resource doesn't exist |
| 500 | Server Error | Internal server error |

### Validation Error Example
```json
{
  "school_id": ["This field is required."],
  "password": ["Passwords must match."]
}
```

---

## 📝 Notes

1. **Authentication:** Include `Authorization: Token <token>` header in all requests except login/register
2. **Pagination:** List endpoints are paginated (50 items per page)
3. **Timestamps:** All dates are in ISO 8601 format (UTC)
4. **ML Model:** Predictions require model at `../ML/models/disease_predictor_v2.pkl`
5. **Privacy:** Chat messages are not stored, only session metadata and insights
6. **Referrals:** Automatically triggered after 5 symptom reports in 30 days

---

## 🔗 Integration Examples

### cURL Examples

**Login:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"school_id":"2024-100","password":"student123"}'
```

**Submit Symptoms:**
```bash
curl -X POST http://localhost:8000/api/symptoms/submit/ \
  -H "Authorization: Token <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "symptoms": ["fever", "cough"],
    "duration_days": 2,
    "severity": 2
  }'
```

### JavaScript (Fetch API)

```javascript
// Login
const login = async () => {
  const response = await fetch('http://localhost:8000/api/auth/login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      school_id: '2024-100',
      password: 'student123'
    })
  });
  const data = await response.json();
  localStorage.setItem('authToken', data.token);
};

// Submit Symptoms
const submitSymptoms = async (symptoms) => {
  const token = localStorage.getItem('authToken');
  const response = await fetch('http://localhost:8000/api/symptoms/submit/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Token ${token}`
    },
    body: JSON.stringify({
      symptoms: symptoms,
      duration_days: 3,
      severity: 2
    })
  });
  return await response.json();
};
```

---

**API Version:** 1.0  
**Last Updated:** October 29, 2025
