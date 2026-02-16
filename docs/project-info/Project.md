Project Overview
The AI-Powered Virtual Health Assistant & Clinic Management System is a secure, campus-ready healthcare platform for students and staff, integrating:

Django: authentication, data storage, permissions, admin controls

Traditional ML Model: disease prediction, symptom classification, ICD-10 tagging, risk scoring

LLM APIs: multilingual conversational reasoning, medical advice, explanation, fallback Q&A

Rasa: smart orchestration of conversational, dialog, and workflow flows

🔄 Detailed Data Flow (End-to-End)
1. Authentication & User Session
User (student/staff) logs in via web/mobile with school ID and password.

Django verifies credentials, initiates session token, loads profile and permissions.

Session, audit logs, and consent status are recorded.

2. Symptom Reporting & Conversational Entry
Student accesses chatbot or symptom reporting UI.

Initial message/input is sent to Rasa server (via webhook/REST API).

3. Conversational Flow Management (Rasa)
Rasa Core/NLU:

Detects intent/entities from user input (“report fever for 3 days,” “what is my diagnosis?”).

Controls dialogue, asks for missing info or clarifications.

Rasa Dialogue Orchestration:

If intent is “symptom report,” routes to custom action (backend trigger).

For general questions or fallback, routes to LLM for broad medical reasoning or translation.

4. ML Model & LLM API Invocation
Django Backend receives Rasa action request (symptom payload + user/session info).

Parallel API Calls:

ML Model API:

Input: symptoms, profile

Output: prediction, ICD-10 tag, risk score, reliability/confidence

LLM API:

Input: symptoms, user context, (optionally ML output)

Output: contextual explanation, clarification questions, multilingual advice, follow-up suggestions

5. Aggregation & Response Construction
Backend aggregates ML and LLM outputs.

Synthesizes user-facing advice:

“Prediction: Influenza (ICD-10: J10, 92% confidence). Advice: Rest, monitor fever, see clinic if condition worsens.”

Follows privacy rules: only session-based insights displayed—no persistent conversation logs.

6. Frontend Display
Student receives:

Structured prediction (diagnosis, confidence, ICD tag)

Rich, human-friendly AI advice, next steps, multilingual explanations

Frequency alerts (e.g., “High frequency: Consider clinic referral”)

Real-time interaction continues via Rasa chat until session ends.

7. Clinic Staff & Admin Module
Staff log in via Django, access:

Directory of students (profiles & recent health events)

Live dashboard with symptom heatmaps, frequency analysis, top insights (CPSU-themed UI)

Filters by department, date range, disease category

Automated reporting: Excel & PDF exports include risk flags and trends

8. Notification & Referral Automation
System triggers:

Push or SMS notifications for high-risk cases, reminders (planned feature)

Hospital referral workflows when symptom frequency or severity exceeds thresholds

9. Storage, Compliance, & Export
All actions/audit events, health data, and reports stored securely in Django DB.

Consent, privacy preferences, and role-based data access strictly enforced.

Data exported for monthly/annual review, DOH sync, or administrative analysis.

📊 Data Flow Diagram (Text Representation)
text
[User Login (Django)] 
       |
   [Session Token + Profile]
       |
   [Chatbot/Symptom UI]
       |
   [Rasa NLU/Core] ----- Intent detection, dialogue management
       |
[Symptom Report]------[General Query/Fallback]
    |                          |
[Backend: ML Model API]   [Backend: LLM API]
    |             \         |
  [Prediction]   [LLM Explanation, Advice, Clarification]
       \             /
   [Aggregate, Synthesize Response]
       |
   [Frontend Display (Student/Staff Portal)]
       |
[Store in DB: Session Insights, Audit, Reports]
       |
   [Dashboard, Reporting, Notification, Referral]
🛡️ Technical Highlights
Security: Session tokens, audit logs, consent-based storage, role permissions (Django)

AI Accuracy: ML for fast, reliable prediction + LLM for natural, explainable, multilingual advice

Conversation Orchestration: Rasa ensures smooth, error-tolerant, and personalized dialogue for users and staff

Reporting & Compliance: Verified Excel/PDF reports, automated hospital referral flags, privacy first