# 🧭 Project Navigation Guide

**Quick reference for navigating the CPSU Virtual Health Assistant codebase**

---

## 📂 Folder Structure

```
VirtualAssistant/
│
├── 📄 README.md                    ← Start here!
├── 📄 NAVIGATION.md                ← This file
│
├── 📁 Django/                      ← Backend API
│   ├── README.md                  ← Django setup & usage
│   ├── manage.py                  ← Django CLI commands
│   ├── clinic/                    ← Main application code
│   └── docs/                      ← All Django documentation
│       ├── DOCUMENTATION_INDEX.md ← Complete doc index
│       ├── architecture/          ← System design docs
│       ├── api/                   ← API reference
│       ├── deployment/            ← Setup guides
│       └── guides/                ← Complete implementation guide
│
├── 📁 ML/                         ← Machine Learning
│   ├── README.md                  ← ML setup & training
│   ├── Datasets/                  ← Training data
│   ├── scripts/                   ← Training & prediction
│   ├── models/                    ← Saved models (.pkl)
│   └── docs/                      ← ML documentation
│
├── 📁 docs/                       ← Project-wide documentation
│   ├── guides/                    ← Complete project guide
│   └── project-info/              ← Requirements & specs
│
└── 📁 .github/                    ← GitHub configs
    └── copilot-instructions.md    ← AI agent guidance
```

---

## 🎯 Common Tasks

### I want to...

#### 🚀 **Get Started**
1. Read: [`README.md`](README.md) (root)
2. Follow: Quick Start instructions
3. Check: [`Django/README.md`](Django/README.md) for backend setup

#### 🏗️ **Understand the System**
1. Read: [`docs/guides/PROJECT_COMPLETE.md`](docs/guides/PROJECT_COMPLETE.md)
2. Check: [`Django/docs/architecture/RASA_ML_FLOW.md`](Django/docs/architecture/RASA_ML_FLOW.md)
3. Review: [`Django/docs/architecture/HYBRID_ML_LLM_SYSTEM.md`](Django/docs/architecture/HYBRID_ML_LLM_SYSTEM.md)

#### 🤖 **Work with ML Model**
1. Go to: `ML/` folder
2. Read: [`ML/README.md`](ML/README.md)
3. Train: Run `ML/scripts/train_model_realistic.py`
4. Test: Run `ML/scripts/test_model.py`

#### 🔌 **Use the API**
1. Read: [`Django/docs/api/API_DOCS.md`](Django/docs/api/API_DOCS.md)
2. Test endpoints with curl or Postman
3. Check: [`Django/docs/api/RASA_INTEGRATION.md`](Django/docs/api/RASA_INTEGRATION.md) for chatbot

#### 💬 **Set Up Rasa Chatbot**
1. Read: [`Django/docs/api/RASA_INTEGRATION.md`](Django/docs/api/RASA_INTEGRATION.md)
2. Follow: Rasa installation steps
3. Configure: Webhook endpoints

#### 🚀 **Deploy to Production**
1. Read: [`Django/docs/deployment/COMPLETE_SUMMARY.md`](Django/docs/deployment/COMPLETE_SUMMARY.md)
2. Configure: Environment variables
3. Set up: Production database & server

#### 🔧 **Configure LLM APIs**
1. Read: [`Django/docs/deployment/LLM_INTEGRATION_SUMMARY.md`](Django/docs/deployment/LLM_INTEGRATION_SUMMARY.md)
2. Get: FREE API keys (Gemini, OpenRouter, Cohere)
3. Add to: `Django/.env` file

#### 🧪 **Run Tests**
```bash
cd Django
python manage.py test
```

#### 📊 **Check Project Status**
1. Read: [`Django/docs/guides/IMPLEMENTATION_COMPLETE.md`](Django/docs/guides/IMPLEMENTATION_COMPLETE.md)
2. Review: Latest updates in [`Django/docs/deployment/UPDATE_SUMMARY.md`](Django/docs/deployment/UPDATE_SUMMARY.md)

---

## 📚 Documentation Map

### Root Level Documentation

| File | Purpose |
|------|---------|
| [`README.md`](README.md) | Main project overview & quick start |
| [`NAVIGATION.md`](NAVIGATION.md) | This navigation guide |
| [`docs/guides/PROJECT_COMPLETE.md`](docs/guides/PROJECT_COMPLETE.md) | Complete system overview |
| [`docs/project-info/Project.md`](docs/project-info/Project.md) | Original requirements |
| [`docs/project-info/Future.md`](docs/project-info/Future.md) | Future enhancements |

### Django Documentation (`Django/docs/`)

**Index**: [`Django/docs/DOCUMENTATION_INDEX.md`](Django/docs/DOCUMENTATION_INDEX.md)

#### Architecture (`Django/docs/architecture/`)
- `HYBRID_ML_LLM_SYSTEM.md` - ML + LLM hybrid system
- `RASA_ML_FLOW.md` - Complete system flow
- `ARCHITECTURE_DIAGRAM.md` - Visual diagrams

#### API (`Django/docs/api/`)
- `API_DOCS.md` - Complete API reference
- `RASA_INTEGRATION.md` - Rasa chatbot setup

#### Deployment (`Django/docs/deployment/`)
- `COMPLETE_SUMMARY.md` - Full setup guide
- `LLM_INTEGRATION_SUMMARY.md` - LLM configuration
- `UPDATE_SUMMARY.md` - Recent changes
- `PROJECT_SUMMARY.md` - Requirements summary

#### Guides (`Django/docs/guides/`)
- `IMPLEMENTATION_COMPLETE.md` - Implementation status

### ML Documentation (`ML/docs/`)

| File | Purpose |
|------|---------|
| `QUICKSTART.md` | ML quick start guide |
| `DATASET_USAGE.md` | Dataset information |
| `FINAL_STATUS.md` | ML project status |

---

## 🔍 Find Specific Information

### Code Files

| What | Where |
|------|-------|
| **Database models** | `Django/clinic/models.py` |
| **API endpoints** | `Django/clinic/views.py` |
| **ML predictions** | `Django/clinic/ml_service.py` |
| **LLM integration** | `Django/clinic/llm_service.py` |
| **Rasa integration** | `Django/clinic/rasa_service.py` |
| **Hybrid predictions** | `Django/clinic/rasa_webhooks.py` |
| **URL routing** | `Django/clinic/urls.py` |
| **Settings** | `Django/health_assistant/settings.py` |

### ML Files

| What | Where |
|------|-------|
| **Training script** | `ML/scripts/train_model_realistic.py` |
| **Testing script** | `ML/scripts/test_model.py` |
| **Prediction CLI** | `ML/scripts/predict.py` |
| **Training data** | `ML/Datasets/active/train.csv` |
| **Test data** | `ML/Datasets/active/test.csv` |
| **Saved models** | `ML/models/*.pkl` |

---

## 🎓 Learning Path

### For New Developers

1. **Week 1: Understanding**
   - Read: Root `README.md`
   - Study: `docs/guides/PROJECT_COMPLETE.md`
   - Explore: Project structure

2. **Week 2: Backend**
   - Setup: Django environment
   - Read: `Django/README.md`
   - Study: `Django/docs/api/API_DOCS.md`
   - Practice: Run API tests

3. **Week 3: ML System**
   - Train: ML model
   - Read: `ML/README.md`
   - Study: `Django/docs/architecture/HYBRID_ML_LLM_SYSTEM.md`
   - Practice: Make predictions

4. **Week 4: Integration**
   - Setup: Rasa chatbot
   - Read: `Django/docs/api/RASA_INTEGRATION.md`
   - Practice: End-to-end flow

---

## 🔗 External Resources

- **Django**: https://docs.djangoproject.com/
- **Django REST Framework**: https://www.django-rest-framework.org/
- **Rasa**: https://rasa.com/docs/
- **scikit-learn**: https://scikit-learn.org/
- **Gemini API**: https://ai.google.dev/
- **OpenRouter**: https://openrouter.ai/docs

---

## 💡 Quick Tips

### Finding Files
```bash
# Find all Python files
find . -name "*.py" -type f

# Find all documentation
find . -name "*.md" -type f

# Find specific function
grep -r "function_name" --include="*.py"
```

### Updating Documentation
- Django docs → `Django/docs/`
- ML docs → `ML/docs/`
- Project docs → `docs/`

### Running Commands
```bash
# Django commands
cd Django
python manage.py <command>

# ML training
cd ML/scripts
python train_model_realistic.py

# Testing
cd Django
python manage.py test
```

---

## 🆘 Getting Help

1. **Check documentation first**:
   - Start with `DOCUMENTATION_INDEX.md` in relevant folder
   - Search for keywords in markdown files

2. **Common issues**:
   - ML model not found → Train model in `ML/scripts/`
   - API errors → Check `Django/docs/api/API_DOCS.md`
   - LLM not working → Check `.env` file and API keys

3. **Still stuck?**:
   - Create GitHub issue
   - Contact development team

---

**Last Updated**: October 29, 2025

**Maintained by**: CPSU Development Team
