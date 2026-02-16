# 🤖 Rasa + LLM Integration Guide

## Architecture Overview

### Chat Flow (Hybrid Approach)
```
User Message
    ↓
[1] Try Rasa Chatbot (Primary)
    ↓
    ├─ Success + High Confidence (≥0.6) → Return Rasa Response
    ↓
    └─ Fail / Low Confidence → LLM Fallback Chain:
        ↓
        [2] Gemini 2.5 Flash (Fast, High Quality)
            ↓
            └─ Fail → [3] Gemini 2.5 Flash Lite (Faster, Cheaper)
                ↓
                └─ Fail → [4] Grok 2 via OpenRouter
                    ↓
                    └─ Fail → [5] Claude 3.5 via OpenRouter
                        ↓
                        └─ Fail → [6] Cohere (Final Fallback)
                            ↓
                            └─ Fail → Generic Response
```

## Components

### 1. Rasa Service (`clinic/rasa_service.py`)
**Purpose**: Primary conversational AI for structured health dialogues

**Features**:
- Intent recognition
- Entity extraction
- Context management
- Multi-turn conversations
- Custom health flows

**When Rasa is Used**:
- User asks common health questions (fever, headache, etc.)
- Structured symptom collection
- Follow-up questions
- Predefined health workflows

**When LLM Fallback Triggers**:
- Rasa server is down/unreachable
- Confidence score < 0.6 (60%)
- Generic responses ("I don't understand")
- Complex/unusual queries Rasa can't handle

### 2. LLM Service (`clinic/llm_service.py`)
**Purpose**: Intelligent fallback for complex/unusual queries

**Fallback Chain**:
1. **Gemini 2.5 Flash** (Primary LLM)
   - Best quality
   - Multilingual (English, Filipino, dialects)
   - Free tier: 60 requests/minute

2. **Gemini 2.5 Flash Lite** (Secondary)
   - Faster response
   - Lower latency
   - Cheaper (if Flash fails)

3. **Grok 2** (via OpenRouter)
   - Real-time knowledge
   - Conversational tone
   - Good for complex queries

4. **Claude 3.5 Sonnet** (via OpenRouter)
   - High reasoning ability
   - Empathetic responses
   - Medical context understanding

5. **Cohere** (Final Fallback)
   - Reliable baseline
   - Good multilingual support

## Configuration

### Environment Variables (`.env`)

```bash
# Rasa Configuration
RASA_ENABLED=True                    # Enable/disable Rasa
RASA_SERVER_URL=http://localhost:5005  # Rasa server endpoint
RASA_TIMEOUT=5                       # Request timeout (seconds)
RASA_CONFIDENCE_THRESHOLD=0.6        # Min confidence to use Rasa response

# LLM API Keys
GEMINI_API_KEY=your-key-here
OPENROUTER_API_KEY=your-key-here
COHERE_API_KEY=your-key-here
```

### Settings (`health_assistant/settings.py`)

```python
# Rasa Settings
RASA_ENABLED = True
RASA_SERVER_URL = 'http://localhost:5005'
RASA_TIMEOUT = 5
RASA_CONFIDENCE_THRESHOLD = 0.6

# LLM Settings
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
COHERE_API_KEY = os.getenv('COHERE_API_KEY')
```

## Setting Up Rasa

### 1. Install Rasa
```bash
pip install rasa

# OR use Rasa in Docker
docker pull rasa/rasa:latest
```

### 2. Create Rasa Project
```bash
# Create new Rasa project
rasa init --no-prompt

# Or use existing Rasa project
cd /path/to/your/rasa/project
```

### 3. Train Rasa Model
```bash
# Train on your health-related intents
rasa train

# Example training data (domain.yml):
intents:
  - greet
  - fever_symptoms
  - headache_symptoms
  - emergency
  - goodbye

responses:
  utter_greet:
    - text: "Hello! I'm your CPSU health assistant. How can I help you today?"
  
  utter_ask_fever_duration:
    - text: "How long have you had the fever?"
  
  utter_emergency:
    - text: "This sounds serious. Please visit the CPSU clinic immediately or call emergency services."
```

### 4. Run Rasa Server
```bash
# Start Rasa server on port 5005
rasa run --enable-api --cors "*" --port 5005

# OR with Docker
docker run -p 5005:5005 rasa/rasa:latest run --enable-api --cors "*"
```

### 5. Test Rasa Connection
```bash
# From Django project
cd Django
python manage.py shell -c "
from clinic.rasa_service import RasaChatService
rasa = RasaChatService()
print('Rasa available:', rasa.is_available())
"
```

## API Response Format

### With Rasa (Success)
```json
{
  "response": "I understand you have a fever. How long have you been experiencing this?",
  "session_id": "uuid-here",
  "source": "rasa"
}
```

### With LLM Fallback
```json
{
  "response": "I'm sorry to hear you're not feeling well. Based on your symptoms...",
  "session_id": "uuid-here",
  "source": "llm_fallback"
}
```

## Testing the Integration

### Test 1: Rasa Response (Server Running)
```bash
# Start Rasa server first
rasa run --enable-api --port 5005

# Test via API
curl -X POST http://localhost:8000/api/chat/message/ \
  -H "Authorization: Token <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "existing-session-id",
    "message": "I have a fever",
    "language": "english"
  }'

# Expected: source = "rasa"
```

### Test 2: LLM Fallback (Rasa Down)
```bash
# Stop Rasa server or set RASA_ENABLED=False

# Test via API
curl -X POST http://localhost:8000/api/chat/message/ \
  -H "Authorization: Token <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "existing-session-id",
    "message": "What should I do about my persistent headache?",
    "language": "english"
  }'

# Expected: source = "llm_fallback"
```

### Test 3: Multilingual (Filipino)
```bash
curl -X POST http://localhost:8000/api/chat/message/ \
  -H "Authorization: Token <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "existing-session-id",
    "message": "May lagnat po ako at masakit ang ulo",
    "language": "filipino"
  }'
```

## Monitoring & Debugging

### Check Rasa Status
```python
from clinic.rasa_service import RasaChatService

rasa = RasaChatService()
print(f"Rasa Available: {rasa.is_available()}")
print(f"Rasa URL: {rasa.rasa_url}")
print(f"Confidence Threshold: {rasa.confidence_threshold}")
```

### Check LLM Status
```python
from clinic.llm_service import AIInsightGenerator

ai = AIInsightGenerator()
print(f"Gemini Flash: {ai.gemini_model is not None}")
print(f"Gemini Lite: {ai.gemini_lite_model is not None}")
print(f"OpenRouter: {ai.openrouter_client is not None}")
print(f"Cohere: {ai.cohere_client is not None}")
```

### View Logs
```bash
# Django logs show which service handled each request
# Look for:
# "Response from Gemini Flash"
# "Rasa failed, using LLM fallback"
# "Response from rasa"
```

## Best Practices

### 1. Rasa for Structured Flows
Use Rasa for:
- Symptom checkers (step-by-step)
- Appointment booking
- FAQ responses
- Predefined health protocols

### 2. LLM for Complex Queries
Use LLM fallback for:
- Open-ended health questions
- Emotional support
- Unusual symptom combinations
- Multilingual complex queries

### 3. Confidence Tuning
```python
# Adjust threshold based on Rasa performance
RASA_CONFIDENCE_THRESHOLD = 0.6  # Default

# Higher (0.8) → More LLM usage (better quality, higher cost)
# Lower (0.4) → More Rasa usage (structured, predictable)
```

### 4. Cost Optimization
```python
# For development/testing
RASA_ENABLED = True  # Use Rasa first (free)

# For production with budget
RASA_ENABLED = True
RASA_CONFIDENCE_THRESHOLD = 0.7  # Use LLM less frequently
```

## Troubleshooting

### Rasa Not Responding
```bash
# Check if Rasa is running
curl http://localhost:5005/status

# Expected: {"model_fingerprint": "...", "num_active_training_jobs": 0}

# If not running:
rasa run --enable-api --cors "*" --port 5005
```

### All LLMs Failing
```bash
# Check API keys
python manage.py shell -c "
from django.conf import settings
print('Gemini:', settings.GEMINI_API_KEY[:10] if settings.GEMINI_API_KEY else 'Not set')
print('OpenRouter:', settings.OPENROUTER_API_KEY[:10] if settings.OPENROUTER_API_KEY else 'Not set')
print('Cohere:', settings.COHERE_API_KEY[:10] if settings.COHERE_API_KEY else 'Not set')
"
```

### High Latency
```bash
# Reduce Rasa timeout
RASA_TIMEOUT=3  # Faster fallback to LLM

# Or disable Rasa temporarily
RASA_ENABLED=False
```

## Cost Estimates

### Rasa (Self-hosted)
- **Cost**: FREE (open source)
- **Hosting**: ~$5-20/month (VPS/cloud)
- **Best for**: Structured health conversations

### Gemini 2.5 Flash
- **Free Tier**: 60 requests/minute
- **Cost**: FREE for moderate usage
- **Best for**: General health questions

### Gemini 2.5 Flash Lite
- **Free Tier**: Higher rate limits
- **Cost**: Cheaper than Flash
- **Best for**: High-volume fallback

### OpenRouter (Grok, Claude)
- **Cost**: Pay-per-use ($0.001-0.01/request)
- **Best for**: Complex queries

### Cohere
- **Free Trial**: 100 API calls/month
- **Cost**: $1/1000 requests
- **Best for**: Final fallback

---

## Summary

✅ **Rasa**: Primary chatbot (structured, free, offline-capable)  
✅ **Gemini Flash**: First LLM fallback (high quality, multilingual)  
✅ **Gemini Lite**: Second LLM fallback (faster, cheaper)  
✅ **Grok/Claude**: Third fallback (via OpenRouter, complex queries)  
✅ **Cohere**: Final fallback (reliable baseline)  

**Recommended Setup**:
1. Start with Rasa for common health queries
2. Fall back to Gemini for complex/unusual cases
3. Use OpenRouter models for edge cases
4. Monitor costs and adjust thresholds

**Status**: ✅ **READY FOR PRODUCTION**
