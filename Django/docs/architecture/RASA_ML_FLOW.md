# Rasa Integration with Django ML Backend

## Architecture: Rasa-First with ML Integration

```
┌─────────────────────────────────────────────────────────────┐
│                  User Interface (Mobile/Web)                │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    RASA CHATBOT SERVER                      │
│                   (Primary Conversation)                    │
│                                                             │
│  ┌────────────────────────────────────────────────────┐   │
│  │ 1. Greeting & Symptom Collection                   │   │
│  │    "Hello! What symptoms are you experiencing?"    │   │
│  │    User: "I have fever and headache"               │   │
│  └────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌────────────────────────▼───────────────────────────┐   │
│  │ 2. Entity Extraction                               │   │
│  │    Detected: ["fever", "headache"]                 │   │
│  └────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌────────────────────────▼───────────────────────────┐   │
│  │ 3. Call Django ML API                              │   │
│  │    POST /api/rasa/predict/                         │   │
│  │    {                                               │   │
│  │      "symptoms": ["fever", "headache"],            │   │
│  │      "generate_insights": false  // FREE tier      │   │
│  │    }                                               │   │
│  └────────────────────────────────────────────────────┘   │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                   DJANGO ML BACKEND                         │
│                                                             │
│  ┌────────────────────────────────────────────────────┐   │
│  │ 4. ML Prediction (scikit-learn)                    │   │
│  │    - Load trained model                            │   │
│  │    - Predict from 132 symptoms                     │   │
│  │    - Return: Disease + Confidence + Precautions    │   │
│  └────────────────────────────────────────────────────┘   │
│                           │                                 │
│                           ▼                                 │
│  ┌────────────────────────────────────────────────────┐   │
│  │ 5. Return Prediction                               │   │
│  │    {                                               │   │
│  │      "predicted_disease": "Common Cold",           │   │
│  │      "confidence": 0.85,                           │   │
│  │      "precautions": [                              │   │
│  │        "Get rest",                                 │   │
│  │        "Drink fluids",                             │   │
│  │        "Take paracetamol"                          │   │
│  │      ]                                             │   │
│  │    }                                               │   │
│  └────────────────────────────────────────────────────┘   │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                    RASA CHATBOT SERVER                      │
│                                                             │
│  ┌────────────────────────────────────────────────────┐   │
│  │ 6. Format Response                                 │   │
│  │    "Based on your symptoms (fever, headache),      │   │
│  │     you might have Common Cold (85% confidence).   │   │
│  │                                                    │   │
│  │     Recommendations:                               │   │
│  │     • Get plenty of rest                           │   │
│  │     • Drink lots of fluids                         │   │
│  │     • Take paracetamol if needed                   │   │
│  │                                                    │   │
│  │     Would you like to:                             │   │
│  │     [Visit Clinic] [Add More Symptoms] [End]"      │   │
│  └────────────────────────────────────────────────────┘   │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
              User sees response


┌─────────────────────────────────────────────────────────────┐
│              LLM FALLBACK (Only when Rasa fails)            │
│                                                             │
│  Used ONLY when:                                           │
│  • Rasa server is down                                     │
│  • Rasa confidence < 0.6                                   │
│  • User asks complex/unusual questions                     │
│                                                             │
│  Fallback chain (FREE tier):                               │
│  1. Gemini 2.5 Flash (60 req/min free)                     │
│  2. Gemini 2.5 Flash Lite (higher limits)                  │
│                                                             │
│  NOT USED for normal symptom collection!                   │
└─────────────────────────────────────────────────────────────┘
```

## Example Conversation Flow

### Scenario: Student with Fever and Headache

```
User: "Hello"
Rasa: "Hello! I'm your CPSU health assistant. How can I help you today?"

User: "I'm not feeling well"
Rasa: "I'm sorry to hear that. Can you tell me what symptoms you're experiencing?"

User: "I have fever and headache"
Rasa: [Extracts: fever, headache]
      [Calls Django: POST /api/rasa/predict/]
      [Gets: Common Cold, 85%]
      
      "Based on your symptoms, you might have Common Cold (85% confidence).
      
       Here's what you should do:
       • Get plenty of rest
       • Drink lots of fluids  
       • Take paracetamol for fever
       
       Do you have any other symptoms?"

User: "Yes, I also feel tired"
Rasa: [Extracts: fever, headache, fatigue]
      [Calls Django again with updated symptoms]
      [Gets: Flu, 78%]
      
      "With the additional symptom, it looks more like Flu (78% confidence).
      
       Recommendations:
       • Rest at home for 2-3 days
       • Stay hydrated
       • Avoid contact with others (it's contagious)
       
       Would you like to visit the campus clinic?"

User: "Yes, I'll visit the clinic"
Rasa: "Great! The CPSU clinic is open Mon-Fri, 8AM-5PM.
       I've recorded your symptoms. Please mention this conversation
       when you visit.
       
       Take care and feel better soon! 🏥"
```

### Why This Flow is Better

✅ **Free Tier Only**:
- Rasa: FREE (self-hosted)
- ML Model: FREE (runs locally)
- LLM: Only for rare edge cases (Gemini free tier: 60 req/min)

✅ **Fast**:
- Rasa: ~100-200ms per message
- ML Prediction: ~50-100ms
- Total: <300ms per interaction

✅ **Accurate**:
- Rasa handles conversation context
- ML model provides medical predictions
- LLM only for unusual cases

✅ **Scalable**:
- Rasa handles thousands of concurrent users
- ML model is local (no API limits)
- No expensive LLM calls for normal chats

## Rasa Configuration

### 1. Create Rasa Project

```bash
# Install Rasa
pip install rasa

# Create project
rasa init --no-prompt

cd rasa_project
```

### 2. Configure Domain (`domain.yml`)

```yaml
version: "3.1"

intents:
  - greet
  - report_symptoms
  - add_symptoms
  - visit_clinic
  - goodbye

entities:
  - symptom

slots:
  symptoms:
    type: list
    influence_conversation: true
    mappings:
      - type: from_entity
        entity: symptom

responses:
  utter_greet:
    - text: "Hello! I'm your CPSU health assistant. How can I help you today?"

  utter_ask_symptoms:
    - text: "Can you tell me what symptoms you're experiencing?"

  utter_ask_more_symptoms:
    - text: "Do you have any other symptoms?"
    - text: "Is there anything else you're experiencing?"

  utter_clinic_info:
    - text: "The CPSU clinic is open Monday-Friday, 8AM-5PM. Location: Main Campus Health Building."

  utter_goodbye:
    - text: "Take care and feel better soon! If symptoms worsen, please visit the clinic immediately. 🏥"

actions:
  - action_predict_disease  # Custom action to call Django API
```

### 3. Create Custom Action (`actions/actions.py`)

```python
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

class ActionPredictDisease(Action):
    """Call Django ML API to predict disease"""
    
    def name(self) -> Text:
        return "action_predict_disease"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get symptoms from slots
        symptoms = tracker.get_slot('symptoms') or []
        
        if not symptoms:
            dispatcher.utter_message(text="I need to know your symptoms first. What are you experiencing?")
            return []
        
        # Call Django ML API
        try:
            response = requests.post(
                'http://localhost:8000/api/rasa/predict/',
                json={
                    'symptoms': symptoms,
                    'sender_id': tracker.sender_id,
                    'generate_insights': False  # FREE tier - no LLM
                },
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                
                disease = data.get('predicted_disease', 'Unknown')
                confidence = data.get('confidence', 0) * 100
                precautions = data.get('precautions', [])
                is_communicable = data.get('is_communicable', False)
                
                # Format response
                message = f"Based on your symptoms ({', '.join(symptoms)}), "
                message += f"you might have **{disease}** ({confidence:.0f}% confidence).\n\n"
                
                if is_communicable:
                    message += "⚠️ Note: This condition may be contagious. Please avoid close contact with others.\n\n"
                
                message += "**Recommendations:**\n"
                for i, precaution in enumerate(precautions[:4], 1):
                    message += f"{i}. {precaution}\n"
                
                dispatcher.utter_message(text=message)
                dispatcher.utter_message(text="Would you like to visit the CPSU clinic?")
                
            else:
                dispatcher.utter_message(text="Sorry, I couldn't analyze your symptoms right now. Please try again.")
                
        except Exception as e:
            dispatcher.utter_message(text="I'm having trouble connecting to the diagnosis system. Please try again in a moment.")
        
        return []
```

### 4. Start Services

```bash
# Terminal 1: Start Django
cd Django
python manage.py runserver

# Terminal 2: Start Rasa Actions Server
cd rasa_project
rasa run actions

# Terminal 3: Start Rasa Server
cd rasa_project
rasa run --enable-api --cors "*" --port 5005
```

## FREE Tier Usage Breakdown

### Normal Conversation (95% of cases)
```
User: "I have fever and headache"
→ Rasa: Extracts symptoms (FREE)
→ Django: ML prediction (FREE, local)
→ Rasa: Formats response (FREE)
Total cost: $0
Response time: <300ms
```

### Edge Case with LLM (5% of cases)
```
User: "What's the difference between Type 1 and Type 2 diabetes?"
→ Rasa: Can't handle (complex medical question)
→ Django: Falls back to Gemini Flash (FREE tier: 60/min)
→ User: Gets detailed LLM explanation
Total cost: $0 (within free tier)
Response time: ~700ms
```

### Monthly Estimates (1000 students)
```
Conversations per month: 5,000
- Rasa handles: 4,750 (95%)  → Cost: $0
- LLM fallback: 250 (5%)     → Cost: $0 (free tier)
- ML predictions: 5,000      → Cost: $0 (local)

Total monthly cost: $0
```

## API Endpoints

### For Rasa to Call

**1. Disease Prediction**
```bash
POST /api/rasa/predict/
{
  "symptoms": ["fever", "headache"],
  "sender_id": "user-123",
  "generate_insights": false  # Set false for free tier
}
```

**2. Available Symptoms**
```bash
GET /api/rasa/symptoms/

Response:
{
  "symptoms": ["fever", "headache", "cough", ...],
  "count": 132
}
```

### For Frontend to Call

**Chat Message** (goes to Rasa first)
```bash
POST /api/chat/message/
{
  "session_id": "uuid",
  "message": "I have a fever",
  "language": "english"
}

Response:
{
  "response": "I understand. How long have you had the fever?",
  "source": "rasa",  # or "llm_fallback"
  "session_id": "uuid"
}
```

## Testing

### Test ML Prediction Webhook
```bash
curl -X POST http://localhost:8000/api/rasa/predict/ \
  -H "Content-Type: application/json" \
  -d '{
    "symptoms": ["fever", "headache", "fatigue"],
    "sender_id": "test-123"
  }'
```

### Test Rasa Integration
```bash
# Start Rasa server first
rasa run --enable-api --port 5005

# Send message
curl -X POST http://localhost:5005/webhooks/rest/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "test-user",
    "message": "I have fever and headache"
  }'
```

---

**Cost**: 100% FREE tier  
**Performance**: <300ms per interaction  
**LLM Usage**: <5% of conversations  
**ML Model**: 100% local (no API calls)
