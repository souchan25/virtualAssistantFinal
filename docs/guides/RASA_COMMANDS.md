# CPSU Virtual Health Assistant - Command Reference

## 🚀 Quick Start Commands

### 1. Activate Virtual Environment (Windows Git Bash)
```bash
source venv/Scripts/activate
```

### 2. Train Rasa Model (First Time Only - ~2-3 minutes)
```bash
cd Rasa
rasa train
```

### 3. Start Django Backend (Terminal 1)
```bash
cd Django
python manage.py runserver
# Keep this running! Django must be on http://localhost:8000
```

### 4. Start Rasa Action Server (Terminal 2)
```bash
cd Rasa
rasa run actions
# Keep this running! Actions server on http://localhost:5055
```

### 5. Test Rasa Chatbot (Terminal 3)

**Option A: Interactive Shell**
```bash
cd Rasa
rasa shell
# Type your messages and test the bot
```

**Option B: Run as API Server**
```bash
cd Rasa
rasa run --enable-api --cors "*"
# Chatbot API on http://localhost:5005
```

---

## 📋 Common Commands

### Training
```bash
cd Rasa
rasa train              # Train both NLU and Core
rasa train nlu          # Train only NLU
rasa train core         # Train only dialogue
```

### Testing
```bash
cd Rasa
rasa shell              # Interactive testing
rasa shell --debug      # Show detailed logs
rasa test               # Run test stories
rasa interactive        # Interactive learning mode
```

### Data Validation
```bash
cd Rasa
rasa data validate      # Check for errors in training data
```

### Visualization
```bash
cd Rasa
rasa visualize          # Generate story graph
```

---

## 🐛 Troubleshooting

### Error: "The path 'config.yml' does not exist"
**Solution:** You're in the wrong directory!
```bash
pwd                     # Check current directory
cd /d/VirtualAssistant/Rasa  # Change to Rasa folder
```

### Error: "Action server not running"
**Solution:** Start action server in separate terminal
```bash
cd Rasa
rasa run actions
```

### Error: Django API not reachable
**Solution:** Check Django is running
```bash
curl http://localhost:8000/api/rasa/predict/
# Should get 405 Method Not Allowed (which means it's running)
```

### Error: "No NLU data found"
**Solution:** Make sure you're in the Rasa directory with data/ folder
```bash
ls data/               # Should show nlu.yml, stories.yml, rules.yml
```

---

## 📂 Directory Structure

```
VirtualAssistant/
├── venv/              # Virtual environment
│   └── Scripts/activate   # Activation script
├── Django/            # Backend (port 8000)
├── Rasa/              # Chatbot (port 5005)
│   ├── config.yml     # MUST be here to train
│   ├── domain.yml
│   ├── data/
│   ├── actions/
│   └── models/        # Generated after training
└── ML/                # ML models
```

---

## ✅ All 3 Services Running

You need **3 terminals** running simultaneously:

**Terminal 1 - Django:**
```bash
cd Django
python manage.py runserver
# ✅ Running on http://localhost:8000
```

**Terminal 2 - Rasa Actions:**
```bash
cd Rasa
rasa run actions
# ✅ Running on http://localhost:5055
```

**Terminal 3 - Rasa Chatbot:**
```bash
cd Rasa
rasa shell
# ✅ Interactive mode
# OR
rasa run --enable-api --cors "*"
# ✅ API mode on http://localhost:5005
```

---

## 🧪 Test Conversation

Once all services are running:

```bash
cd Rasa
rasa shell
```

Then type:
```
Your input ->  Hi
Your input ->  I have fever and cough
Your input ->  I also feel tired
Your input ->  yes
```

Bot should respond with diagnosis from Django ML API!

---

## 📊 Expected Training Output

```
Training NLU model...
Processed 132 examples for NLU
Training Core model...  
Processed 10 stories
Processed 6 rules
Training completed
Saved model to 'models/20241031-143022.tar.gz'
```

---

## 🔄 Quick Reference

| Task | Command |
|------|---------|
| Activate venv | `source venv/Scripts/activate` |
| Train Rasa | `cd Rasa && rasa train` |
| Test Rasa | `cd Rasa && rasa shell` |
| Start Django | `cd Django && python manage.py runserver` |
| Start Actions | `cd Rasa && rasa run actions` |
| Run Rasa API | `cd Rasa && rasa run --enable-api --cors "*"` |

---

## 💡 Tips

1. **Always** `cd Rasa` before running rasa commands
2. **Always** activate venv first: `source venv/Scripts/activate`
3. **Always** start Django before testing (Rasa needs it!)
4. Training creates files in `Rasa/models/` directory
5. Use `rasa shell --debug` to see what Rasa is thinking

---

Save this file for reference!
