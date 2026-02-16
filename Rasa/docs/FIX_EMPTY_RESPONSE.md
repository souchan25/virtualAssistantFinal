# Fix: Rasa Empty Response Issue

## 🔴 Problem
```
Rasa logs: "Ignoring message as there is no agent to handle it"
Django logs: "Rasa returned empty response"
```

## ✅ Root Cause
Rasa server is running BUT **no trained model is loaded**. This happens when:
1. Rasa was started without specifying a model file
2. No model was trained yet
3. Model file path is incorrect

---

## 🛠️ Solution (3 Steps)

### Step 1: Run Diagnostic
```bash
# From VirtualAssistant root directory
bash scripts/diagnose_rasa.sh
```

This will tell you exactly what's wrong and how to fix it.

### Step 2: Fix Rasa (Choose ONE method)

#### **Method A: Use the automated script** (Recommended)
```bash
cd Rasa
bash start_server.sh
```

This script will:
- ✅ Find the latest trained model
- ✅ Start Rasa with correct parameters
- ✅ Enable API and CORS
- ✅ Show you which model is loaded

#### **Method B: Manual start**
```bash
cd Rasa

# Stop any running Rasa server first
# Ctrl+C or kill the process

# Start with specific model
rasa run \
  --model models/20251102-000705-fat-outpost.tar.gz \
  --enable-api \
  --cors "*" \
  --port 5005
```

**Important:** Replace `20251102-000705-fat-outpost.tar.gz` with your actual model filename!

### Step 3: Verify It Works
```bash
# Test Rasa directly
curl -X POST http://localhost:5005/webhooks/rest/webhook \
  -H "Content-Type: application/json" \
  -d '{"sender":"test","message":"hello"}'

# Should return something like:
# [{"recipient_id":"test","text":"Hello! I'm the CPSU Virtual Health Assistant..."}]
```

**If you get `[]` (empty array):** Model isn't loaded. Go back to Step 2.

---

## 🚀 Complete Startup Sequence

For a fresh start, run these commands **in order, in separate terminals**:

### Terminal 1: Django
```bash
cd Django
python manage.py runserver
```

### Terminal 2: Rasa Action Server
```bash
cd Rasa
rasa run actions
```

### Terminal 3: Rasa Server
```bash
cd Rasa
bash start_server.sh
```

---

## 📝 Quick Reference

### Check if Rasa is working:
```bash
curl http://localhost:5005/status
```

### Check if model is loaded:
```bash
curl -X POST http://localhost:5005/webhooks/rest/webhook \
  -d '{"sender":"test","message":"hi"}' \
  -H "Content-Type: application/json"
```

### View available models:
```bash
ls -lh Rasa/models/
```

### Train a new model (if needed):
```bash
cd Rasa
rasa train
# Takes 2-3 minutes
```

---

## 🎯 Expected Behavior After Fix

### Rasa Logs (GOOD ✅):
```
2025-12-10 10:15:23 INFO     rasa.core.processor  - Received user message: 'I have fever'
2025-12-10 10:15:23 DEBUG    rasa.core.processor  - Predicted next action 'action_extract_symptoms'
```

### Django Logs (GOOD ✅):
```
INFO - Rasa response received: Let me analyze your symptoms... (confidence: 0.95)
[10/Dec/2025 10:15:23] "POST /api/chat/message/ HTTP/1.1" 200 256
```

### Rasa Logs (BAD ❌):
```
2025-12-10 10:00:31 INFO     rasa.core.agent  - Ignoring message as there is no agent to handle it.
```
**This means:** No model loaded. Follow steps above!

---

## 💡 Pro Tips

1. **Always use `start_server.sh`** - It automatically finds and loads the latest model
2. **Check logs** - `tail -f Rasa/rasa_server.log` shows what's happening
3. **Restart properly** - Stop Rasa (Ctrl+C), then start again
4. **LLM Fallback works** - Even if Rasa fails, Django will use OpenRouter/Gemini/Groq for chat

---

## 🆘 Still Not Working?

1. **Run diagnostic:**
   ```bash
   bash scripts/diagnose_rasa.sh
   ```

2. **Check Django logs** for "Using LLM fallback" - this confirms Rasa isn't responding

3. **Verify ports:**
   - Django: http://localhost:8000 ✅
   - Rasa: http://localhost:5005 ✅
   - Rasa Actions: http://localhost:5055 ✅

4. **Retrain model:**
   ```bash
   cd Rasa
   rasa train --force
   bash start_server.sh
   ```

---

**Created:** 2025-12-10  
**Status:** Tested and working ✅
