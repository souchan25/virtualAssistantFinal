# 📚 CPSU Health Assistant - Complete Documentation Index

Welcome to the CPSU Virtual Health Assistant documentation! This guide will help you navigate all project documentation.

---

## 🚀 Quick Start

**New to the project?** Start here:
1. [Main README](README.md) - Project overview and setup
2. [Architecture Overview](docs/architecture/RASA_ML_FLOW.md) - How the system works
3. [API Documentation](docs/api/API_DOCS.md) - Endpoint reference

---

## 📁 Documentation Structure

### 🏗️ Architecture (`docs/architecture/`)

Core system design and flow diagrams:

| Document | Description | Best For |
|----------|-------------|----------|
| **[RASA_ML_FLOW.md](docs/architecture/RASA_ML_FLOW.md)** | Main system architecture: Rasa → Django ML → LLM fallback | Understanding overall flow ⭐ |
| **[HYBRID_ML_LLM_SYSTEM.md](docs/architecture/HYBRID_ML_LLM_SYSTEM.md)** | ML + LLM validation system details | Understanding prediction accuracy |
| **[ARCHITECTURE_DIAGRAM.md](docs/architecture/ARCHITECTURE_DIAGRAM.md)** | Visual architecture diagrams | Quick visual reference |

**Start here if you want to**: Understand how the system works, modify the architecture, or explain it to others.

---

### 🔌 API Documentation (`docs/api/`)

REST API endpoints and integration guides:

| Document | Description | Best For |
|----------|-------------|----------|
| **[API_DOCS.md](docs/api/API_DOCS.md)** | Complete REST API reference for all endpoints | API integration ⭐ |
| **[RASA_INTEGRATION.md](docs/api/RASA_INTEGRATION.md)** | Rasa webhook endpoints and integration | Setting up Rasa chatbot |

**Start here if you want to**: Integrate with the API, build a client, or set up Rasa.

---

### 🚢 Deployment (`docs/deployment/`)

Setup guides, summaries, and deployment documentation:

| Document | Description | Best For |
|----------|-------------|----------|
| **[COMPLETE_SUMMARY.md](docs/deployment/COMPLETE_SUMMARY.md)** | Full project setup and configuration | Initial setup ⭐ |
| **[UPDATE_SUMMARY.md](docs/deployment/UPDATE_SUMMARY.md)** | Latest updates and changes | See what's new |
| **[LLM_INTEGRATION_SUMMARY.md](docs/deployment/LLM_INTEGRATION_SUMMARY.md)** | LLM provider setup (Gemini, Grok, etc.) | Configuring AI models |
| **[RASA_LLM_SUMMARY.md](docs/deployment/RASA_LLM_SUMMARY.md)** | Rasa + LLM hybrid setup | Rasa deployment |
| **[PROJECT_SUMMARY.md](docs/deployment/PROJECT_SUMMARY.md)** | Original project specifications | Requirements reference |

**Start here if you want to**: Deploy the system, configure LLMs, or understand setup process.

---

## 🎯 Use Case Guides

### I want to...

#### 🏥 **Set up the Health Assistant**
1. Read: [README.md](README.md) - Installation
2. Read: [COMPLETE_SUMMARY.md](docs/deployment/COMPLETE_SUMMARY.md) - Configuration
3. Read: [LLM_INTEGRATION_SUMMARY.md](docs/deployment/LLM_INTEGRATION_SUMMARY.md) - API keys

#### 💬 **Integrate Rasa Chatbot**
1. Read: [RASA_ML_FLOW.md](docs/architecture/RASA_ML_FLOW.md) - Architecture
2. Read: [RASA_INTEGRATION.md](docs/api/RASA_INTEGRATION.md) - Setup guide
3. Read: [API_DOCS.md](docs/api/API_DOCS.md) - Webhook endpoints

#### 🤖 **Understand ML + LLM Hybrid**
1. Read: [HYBRID_ML_LLM_SYSTEM.md](docs/architecture/HYBRID_ML_LLM_SYSTEM.md) - How it works
2. Read: [RASA_ML_FLOW.md](docs/architecture/RASA_ML_FLOW.md) - Integration flow
3. Test: Use examples in hybrid docs

#### 🔧 **Build a Client/Frontend**
1. Read: [API_DOCS.md](docs/api/API_DOCS.md) - All endpoints
2. Read: [RASA_INTEGRATION.md](docs/api/RASA_INTEGRATION.md) - Chat integration
3. Test: `/api/chat/message/` endpoint

#### 📊 **Understand the Prediction System**
1. Read: [HYBRID_ML_LLM_SYSTEM.md](docs/architecture/HYBRID_ML_LLM_SYSTEM.md) - ML + LLM
2. Read: [RASA_ML_FLOW.md](docs/architecture/RASA_ML_FLOW.md) - Full flow
3. Check: `clinic/ml_service.py` for ML code

#### 🚀 **Deploy to Production**
1. Read: [COMPLETE_SUMMARY.md](docs/deployment/COMPLETE_SUMMARY.md) - Setup
2. Read: [LLM_INTEGRATION_SUMMARY.md](docs/deployment/LLM_INTEGRATION_SUMMARY.md) - API config
3. Configure: `.env` file with production values

---

## 🏗️ System Architecture Quick Reference

```
┌─────────────────────────────────────────────────────────────┐
│                    CPSU Health Assistant                    │
└─────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                │                           │
         ┌──────▼──────┐           ┌───────▼────────┐
         │    Rasa     │           │  Django REST   │
         │  Chatbot    │           │      API       │
         │             │           │                │
         │ • NLU       │◄─────────►│ • ML Service   │
         │ • Dialogue  │  Webhooks │ • LLM Service  │
         │ • Actions   │           │ • Auth         │
         └─────────────┘           │ • Database     │
                                   └────────┬───────┘
                                            │
                                   ┌────────┴────────┐
                                   │                 │
                          ┌────────▼─────┐  ┌───────▼────────┐
                          │  ML Model    │  │  LLM APIs      │
                          │ (scikit-     │  │ • Gemini       │
                          │  learn)      │  │ • Grok (free)  │
                          │              │  │ • Cohere       │
                          │ 132 symptoms │  │                │
                          │ 41 diseases  │  │ Validation &   │
                          │ 85-95% acc.  │  │ Insights       │
                          └──────────────┘  └────────────────┘
```

**Key Features**:
- 🤖 **Rasa**: Conversational AI (FREE, self-hosted)
- 🧠 **ML Model**: Fast predictions (85-95% accuracy, <100ms)
- 🔍 **LLM Validation**: Accuracy boost via Grok/Gemini (FREE tier)
- 💰 **Cost**: $0/month for normal usage

---

## 📋 API Endpoints Quick Reference

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login
- `POST /api/auth/logout/` - Logout

### Health Predictions
- `POST /api/symptoms/submit/` - Submit symptoms for prediction
- `GET /api/symptoms/available/` - Get all 132 symptoms

### Rasa Webhooks (for chatbot integration)
- `POST /api/rasa/predict/` - Get ML + LLM hybrid prediction
- `GET /api/rasa/symptoms/` - Get symptom list for NLU

### Chat (Direct LLM fallback)
- `POST /api/chat/start/` - Start chat session
- `POST /api/chat/message/` - Send message (Rasa → LLM fallback)
- `POST /api/chat/end/` - End session

**Full API docs**: [docs/api/API_DOCS.md](docs/api/API_DOCS.md)

---

## 🔑 Environment Variables

```env
# Required
SECRET_KEY=your-django-secret-key
DEBUG=True

# LLM APIs (FREE tier)
GEMINI_API_KEY=your-gemini-key          # 60 req/min free
OPENROUTER_API_KEY=your-openrouter-key  # Grok free tier
GROK_API_KEY=your-grok-key              # Alternative
COHERE_API_KEY=your-cohere-key          # Fallback

# Database (optional)
DATABASE_URL=sqlite:///db.sqlite3       # Default
```

See: [LLM_INTEGRATION_SUMMARY.md](docs/deployment/LLM_INTEGRATION_SUMMARY.md) for API key setup

---

## 🧪 Testing

### Quick Test Commands

```bash
# Test Django server
python manage.py runserver

# Test ML prediction
curl -X POST http://localhost:8000/api/rasa/predict/ \
  -H "Content-Type: application/json" \
  -d '{"symptoms": ["fever", "cough"], "generate_insights": true}'

# Test chat
curl -X POST http://localhost:8000/api/chat/message/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "I have fever and headache", "session_id": "test-123"}'

# Run tests
python manage.py test
```

---

## 🆘 Troubleshooting

### Common Issues

| Problem | Solution | Docs |
|---------|----------|------|
| ML model not found | Run training script in `ML/scripts/` | [ML README](../ML/README.md) |
| LLM validation failing | Check API keys in `.env` | [LLM Integration](docs/deployment/LLM_INTEGRATION_SUMMARY.md) |
| Rasa not connecting | Check webhook URLs | [Rasa Integration](docs/api/RASA_INTEGRATION.md) |
| Low prediction accuracy | Enable LLM validation (`generate_insights=true`) | [Hybrid System](docs/architecture/HYBRID_ML_LLM_SYSTEM.md) |

---

## 📊 Performance Benchmarks

### Response Times
- ML prediction only: ~100ms ⚡
- ML + LLM validation: ~500ms ⚡
- Full chat (Rasa): ~300ms ⚡

### Accuracy
- ML only: 85-95%
- ML + LLM hybrid: 90-98% ⭐

### Cost
- FREE tier: $0/month (95% of usage)
- Paid tier: $5-20/month (heavy usage)

---

## 🤝 Contributing

1. Read architecture docs to understand the system
2. Check API docs for endpoint specifications
3. Follow code patterns in existing files
4. Test with sample data before committing

---

## 📞 Support

- **Issues**: Create GitHub issue
- **Questions**: Check documentation first
- **Improvements**: Submit pull request

---

## 📚 Additional Resources

### External Documentation
- [Rasa Documentation](https://rasa.com/docs/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [scikit-learn](https://scikit-learn.org/)
- [Gemini API](https://ai.google.dev/docs)
- [OpenRouter API](https://openrouter.ai/docs)

### ML Model Documentation
- Location: `ML/docs/`
- Training: `ML/scripts/train_model_realistic.py`
- Testing: `ML/scripts/test_model.py`
- Prediction: `ML/scripts/predict.py`

---

## 📝 Version History

**Current Version**: 2.0 (Hybrid ML + LLM System)

**Major Updates**:
- ✅ Rasa-first architecture
- ✅ ML + LLM hybrid predictions
- ✅ FREE tier optimization
- ✅ Webhook endpoints for Rasa
- ✅ Improved accuracy (90-98%)

See: [UPDATE_SUMMARY.md](docs/deployment/UPDATE_SUMMARY.md) for detailed changelog

---

**Last Updated**: October 29, 2025  
**Maintained by**: CPSU Development Team
