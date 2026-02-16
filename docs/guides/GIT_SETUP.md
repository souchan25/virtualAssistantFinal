# Git Repository Setup - Quick Reference

## ✅ What WILL be committed (tracked by Git)

### Code & Configuration
- ✅ All Python source code (`*.py`)
- ✅ Django settings, models, views, serializers
- ✅ Vue.js source code (`Vue/src/**`)
- ✅ Rasa configuration (`domain.yml`, `config.yml`, `data/*.yml`, `actions/*.py`)
- ✅ ML training scripts (`ML/scripts/*.py`)
- ✅ Dataset CSVs (`ML/Datasets/active/*.csv`)
- ✅ Requirements files (`requirements.txt`, `package.json`)
- ✅ Documentation (`*.md`, `docs/`)
- ✅ Helper scripts (`start_rasa.sh`, etc.)

### Configuration Templates
- ✅ `.env.example` (template for environment variables)
- ✅ `.gitignore` (this file)
- ✅ `README.md` files in model directories

## ❌ What will NOT be committed (ignored)

### Virtual Environments & Dependencies
- ❌ `venv/` - Python virtual environment (~500 MB)
- ❌ `node_modules/` - Node.js packages (~200+ MB)
- ❌ `__pycache__/` - Python bytecode cache

### Trained Models (Large Binary Files)
- ❌ `ML/models/*.pkl` - ML models (1-5 MB each)
- ❌ `Rasa/models/*.tar.gz` - Rasa models (50-100 MB each)

### Database & User Data
- ❌ `db.sqlite3` - SQLite database (contains user data)
- ❌ `.env` - Environment variables (contains API keys)

### Build Outputs
- ❌ `Vue/dist/` - Vue.js production build
- ❌ `Django/staticfiles/` - Collected static files

### Temporary Files
- ❌ `*.log` - Log files
- ❌ `*.pyc`, `*.pyo` - Python compiled files
- ❌ `.DS_Store`, `Thumbs.db` - OS-specific files

## 📋 First-Time Git Setup

```bash
# 1. Initialize repository
git init

# 2. Add all files (respecting .gitignore)
git add .

# 3. Check what will be committed
git status

# 4. Make initial commit
git commit -m "Initial commit: CPSU Virtual Health Assistant"

# 5. Add remote (replace with your GitHub URL)
git remote add origin https://github.com/yourusername/VirtualAssistant.git

# 6. Push to GitHub
git branch -M main
git push -u origin main
```

## 🔧 Setup Instructions for New Clones

When someone clones your repository, they need to:

```bash
# 1. Clone repository
git clone https://github.com/yourusername/VirtualAssistant.git
cd VirtualAssistant

# 2. Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows Git Bash

# 3. Install dependencies
cd Django && pip install -r requirements.txt
cd ../Rasa && pip install -r requirements.txt
cd ../Vue && npm install

# 4. Create .env file
cp .env.example .env
# Edit .env with your API keys

# 5. Train ML model
cd ../ML/scripts
python train_model_realistic.py

# 6. Train Rasa model
cd ../../Rasa
rasa train

# 7. Setup Django database
cd ../Django
python manage.py migrate
python manage.py createsuperuser

# 8. Start development
python manage.py runserver
```

## 📊 Repository Size Estimate

**With models excluded:**
- Source code: ~5-10 MB
- Documentation: ~1-2 MB
- Datasets (CSVs): ~2-3 MB
- **Total: ~10-15 MB** ✅

**If models were included (not recommended):**
- ML models: ~5 MB
- Rasa models: ~100+ MB
- **Total: ~115+ MB** ❌

By excluding trained models, the repository stays lightweight and fast to clone!

## 🔒 Security Notes

**Never commit these files:**
- `.env` - Contains API keys and secrets
- `db.sqlite3` - Contains user data
- Any files with passwords or tokens

**Already protected by `.gitignore`:**
- ✅ `.env` is ignored
- ✅ `db.sqlite3` is ignored
- ✅ `*.pem`, `*.key` files are ignored

## 📝 Recommended .gitignore Policies

**Keep these tracked:**
- Source code and scripts
- Configuration templates
- Documentation
- Dataset CSVs (if < 100 MB)

**Ignore these:**
- Binary/compiled files
- Dependencies (can be reinstalled)
- User data and secrets
- Large model files (can be retrained)
