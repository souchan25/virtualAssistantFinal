# 🚀 Django Backend Deployment to Azure (Supabase Database)

## ✅ Azure Student Subscription Benefits

Your **Azure for Students** subscription includes:
- **$100 free credits** for 12 months
- **Free services** without credit card:
  - App Service (B1 Basic) - **FREE** with student subscription
  - 1 GB outbound data transfer/month
  - Azure Database for PostgreSQL (or use Supabase)
  
**Cost for this deployment: $0/month** ✅

---

## 📋 Prerequisites

### 1. Azure Setup
```bash
# Install Azure CLI (if not installed)
winget install Microsoft.AzureCLI

# Login to Azure
az login

# Verify student subscription
az account list --output table
```

### 2. Supabase Database Setup

**Get your Supabase credentials:**

1. Go to: https://supabase.com/dashboard/project/YOUR_PROJECT/settings/database
2. Copy these values:
   - **Host:** `db.xxxxx.supabase.co`
   - **Database:** `postgres`
   - **User:** `postgres.xxxxx`
   - **Password:** Your project password
   - **Port:** `5432`

### 3. ML Folder (REQUIRED!)

**⚠️ IMPORTANT: The ML folder IS NEEDED for deployment!**

Your Django app loads:
- `ML/models/disease_predictor_v2.pkl` - Trained ML model
- `ML/Datasets/active/*.csv` - Metadata (symptoms, descriptions, precautions)

**Without these files, ML predictions will fail!**

---

## 🚀 Quick Deployment (Automated Script)

### Option 1: Run Deployment Script

```bash
# Make script executable
cd Django
chmod +x scripts/azure-deploy.sh

# Run deployment
./scripts/azure-deploy.sh
```

The script will:
1. ✅ Create Resource Group
2. ✅ Create App Service Plan (B1 Basic - FREE with student subscription)
3. ✅ Create Web App (Python 3.11)
4. ✅ Configure environment variables (Supabase credentials)
5. ✅ Deploy Django code
6. ✅ Set startup command

**Time: 5-10 minutes**

---

### Option 2: Manual Deployment (Step-by-Step)

#### Step 1: Create Resources

```bash
# Set variables
RESOURCE_GROUP="cpsu-health-assistant-rg"
APP_NAME="cpsu-health-backend"
LOCATION="eastasia"
PLAN_NAME="cpsu-health-plan"

# Create resource group (if not exists)
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create App Service Plan (B1 Basic - FREE for students)
az appservice plan create \
  --name $PLAN_NAME \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --sku B1 \
  --is-linux

# Create Web App
az webapp create \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --plan $PLAN_NAME \
  --runtime "PYTHON:3.11"
```

#### Step 2: Configure Environment Variables

```bash
# Generate secret key
SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(50))")

# Set environment variables
az webapp config appsettings set \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings \
    DEBUG="False" \
    USE_POSTGRESQL="True" \
    DB_NAME="postgres" \
    DB_USER="postgres.your-supabase-id" \
    DB_PASSWORD="your-supabase-password" \
    DB_HOST="db.your-supabase-id.supabase.co" \
    DB_PORT="5432" \
    SECRET_KEY="$SECRET_KEY" \
    DJANGO_ALLOWED_HOSTS="$APP_NAME.azurewebsites.net" \
    CORS_ALLOWED_ORIGINS="https://delightful-forest-0eb2a9000.6.azurestaticapps.net" \
    WEBSITES_PORT="8000" \
    SCM_DO_BUILD_DURING_DEPLOYMENT="true"
```

**⚠️ Replace with your actual Supabase credentials!**

#### Step 3: Configure Startup Command

```bash
# Set startup script
az webapp config set \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --startup-file "startup.sh"
```

#### Step 4: Deploy Code

```bash
# Deploy from local directory
cd Django
az webapp up \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --runtime "PYTHON:3.11" \
  --sku B1 \
  --location $LOCATION
```

---

## 📦 Upload ML Folder (CRITICAL STEP!)

After deploying Django code, upload the ML folder:

### Method 1: Using Script (Recommended)

```bash
cd Django
chmod +x scripts/upload-ml-models.sh
./scripts/upload-ml-models.sh
```

### Method 2: Manual Upload via Kudu

```bash
# 1. Create ML.zip
cd VirtualAssistant
zip -r ML.zip ML/ -x "*.pyc" -x "__pycache__/*"

# 2. Get FTP credentials
az webapp deployment list-publishing-credentials \
  --name cpsu-health-backend \
  --resource-group cpsu-health-assistant-rg

# 3. Upload via browser:
# Go to: https://cpsu-health-backend.scm.azurewebsites.net/ZipDeployUI
# Drag and drop ML.zip

# 4. Extract to /home/site/wwwroot/ML/
```

### Method 3: Using Azure Portal

1. Go to Azure Portal → Your App Service
2. Click **Advanced Tools (Kudu)** → **Go**
3. Click **Debug console** → **CMD**
4. Navigate to `/home/site/wwwroot/`
5. Upload `ML` folder (drag and drop)

---

## 🗄️ Initialize Database

### Run Migrations

```bash
# SSH into Azure App Service
az webapp ssh \
  --name cpsu-health-backend \
  --resource-group cpsu-health-assistant-rg

# Inside SSH:
cd /home/site/wwwroot
python manage.py migrate
```

### Create Superuser

```bash
# Inside SSH session:
python manage.py createsuperuser
# Enter school_id (not username!)
# Enter password
```

### Create Sample Data (Optional)

```bash
# Inside SSH session:
python manage.py create_staff
python manage.py create_sample_data
```

---

## 🔧 Post-Deployment Configuration

### 1. Update Vue Frontend API URL

**File:** `Vue/.env.production`

```env
VITE_API_BASE_URL=https://cpsu-health-backend.azurewebsites.net/api
```

**Redeploy Vue:**
```bash
cd Vue
npm run build
swa deploy ./dist --deployment-token YOUR_TOKEN --env production
```

### 2. Verify Django CORS Settings

**File:** `Django/health_assistant/settings.py`

Already updated with Azure Static Web App URL ✅

### 3. Test Backend API

```bash
# Health check
curl https://cpsu-health-backend.azurewebsites.net/api/

# Register test user
curl -X POST https://cpsu-health-backend.azurewebsites.net/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"school_id":"2024-001","password":"test123","name":"Test User"}'

# Test ML prediction
curl -X POST https://cpsu-health-backend.azurewebsites.net/api/rasa/predict/ \
  -H "Content-Type: application/json" \
  -d '{"symptoms":["fever","cough"]}'
```

---

## 📊 Cost Breakdown (Student Subscription)

| Resource | SKU | Cost |
|----------|-----|------|
| App Service Plan | B1 Basic | **$0** (Free for students) |
| App Service | - | Included |
| Database | Supabase Free | **$0** |
| Bandwidth | 1 GB/month | **$0** |
| **Total** | | **$0/month** ✅ |

**Note:** After student credits expire, B1 Basic is ~$13/month.

---

## 🔍 Monitoring & Management

### View Logs

```bash
# Real-time log streaming
az webapp log tail \
  --name cpsu-health-backend \
  --resource-group cpsu-health-assistant-rg

# Download logs
az webapp log download \
  --name cpsu-health-backend \
  --resource-group cpsu-health-assistant-rg \
  --log-file logs.zip
```

### SSH Access

```bash
az webapp ssh \
  --name cpsu-health-backend \
  --resource-group cpsu-health-assistant-rg
```

### Restart App

```bash
az webapp restart \
  --name cpsu-health-backend \
  --resource-group cpsu-health-assistant-rg
```

### View Environment Variables

```bash
az webapp config appsettings list \
  --name cpsu-health-backend \
  --resource-group cpsu-health-assistant-rg
```

---

## 🛠️ Troubleshooting

### Issue: "Application Error"

**Check logs:**
```bash
az webapp log tail --name cpsu-health-backend --resource-group cpsu-health-assistant-rg
```

**Common fixes:**
1. Verify environment variables are set correctly
2. Check `startup.sh` permissions: `chmod +x startup.sh`
3. Ensure `requirements.txt` has all dependencies
4. Verify Supabase connection: `python manage.py check --database default`

### Issue: "ML Model Not Found"

**Solution:**
```bash
# Upload ML folder using script
cd Django
./scripts/upload-ml-models.sh

# Verify inside SSH:
az webapp ssh --name cpsu-health-backend --resource-group cpsu-health-assistant-rg
ls -la /home/site/wwwroot/ML/models/
# Should see: disease_predictor_v2.pkl
```

### Issue: "Database Connection Failed"

**Check Supabase credentials:**
1. Go to Supabase Dashboard → Settings → Database
2. Verify connection string format
3. Ensure IP whitelist includes Azure IPs (or use `0.0.0.0/0` for all)
4. Check SSL is enabled in Django settings ✅

### Issue: "CORS Error"

**Update Azure environment variables:**
```bash
az webapp config appsettings set \
  --name cpsu-health-backend \
  --resource-group cpsu-health-assistant-rg \
  --settings CORS_ALLOWED_ORIGINS="https://delightful-forest-0eb2a9000.6.azurestaticapps.net"
```

---

## 🔄 Update Deployment

### Update Code

```bash
cd Django
az webapp up \
  --name cpsu-health-backend \
  --resource-group cpsu-health-assistant-rg
```

### Update ML Models

```bash
# Retrain model locally
cd ML/scripts
python train_model_realistic.py

# Upload to Azure
cd ../../Django
./scripts/upload-ml-models.sh
```

### Update Dependencies

```bash
# Update requirements.txt locally
pip freeze > requirements.txt

# Redeploy
az webapp restart --name cpsu-health-backend --resource-group cpsu-health-assistant-rg
```

---

## 🗑️ Delete Deployment

### Delete App Service Only

```bash
az webapp delete \
  --name cpsu-health-backend \
  --resource-group cpsu-health-assistant-rg \
  --yes
```

### Delete Entire Resource Group (ALL resources)

```bash
az group delete \
  --name cpsu-health-assistant-rg \
  --yes --no-wait
```

---

## ✅ Deployment Checklist

**Before deployment:**
- [ ] Azure CLI installed and logged in
- [ ] Student subscription verified
- [ ] Supabase database created and credentials ready
- [ ] ML model trained (`ML/models/disease_predictor_v2.pkl` exists)
- [ ] `requirements.txt` up to date
- [ ] `startup.sh` created and executable
- [ ] `.env.production` configured

**During deployment:**
- [ ] Resource group created
- [ ] App Service Plan created (B1 Basic)
- [ ] Web App created (Python 3.11)
- [ ] Environment variables set (Supabase credentials)
- [ ] Django code deployed
- [ ] Startup command configured
- [ ] ML folder uploaded

**After deployment:**
- [ ] Database migrations run (`python manage.py migrate`)
- [ ] Superuser created
- [ ] Sample data created (optional)
- [ ] Vue frontend API URL updated
- [ ] Backend API tested (health check, register, predict)
- [ ] Logs checked for errors
- [ ] CORS working from Vue app
- [ ] ML predictions working

---

## 📚 Additional Resources

- [Azure App Service Documentation](https://docs.microsoft.com/en-us/azure/app-service/)
- [Django on Azure Guide](https://docs.microsoft.com/en-us/azure/app-service/quickstart-python)
- [Supabase Documentation](https://supabase.com/docs)
- [Azure for Students](https://azure.microsoft.com/en-us/free/students/)

---

## 🎯 System Architecture (Production)

```
┌─────────────────┐
│  Vue.js (SWA)   │ → Frontend on Azure Static Web Apps
└────────┬────────┘
         │ HTTPS
         ↓
┌─────────────────┐
│ Django (Azure)  │ → Backend on Azure App Service B1
│  - REST API     │
│  - ML Service   │
│  - LLM Service  │
└────────┬────────┘
         │
    ┌────┴──────┬──────────────┐
    ↓           ↓              ↓
┌─────────┐ ┌─────────┐  ┌─────────┐
│Supabase │ │ML Models│  │LLM APIs │
│(Postgres│ │(Local)  │  │(Gemini) │
└─────────┘ └─────────┘  └─────────┘
```

---

**Questions?** Check the [main documentation](../README.md) or Vue deployment guide!
