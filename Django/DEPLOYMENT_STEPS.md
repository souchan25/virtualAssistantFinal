# Manual Deployment Steps for Azure

## Current Status
- ✅ ML model trained: `ML/models/disease_predictor_v2.pkl`
- ✅ Azure resources created
- ✅ Environment variables configured
- ⚠️ Application not starting (503 error)

## Troubleshooting Steps

### Step 1: Check Application Logs via SSH

```bash
# SSH into the container
az webapp ssh --name cpsu-health-backend --resource-group cpsu-health-assistant-rg

# Once inside, check if the app is running
ps aux | grep gunicorn

# Check startup logs
cat /home/LogFiles/default_docker.log | tail -100

# Test Django manually
cd /home/site/wwwroot
python manage.py check
python manage.py migrate --check
```

### Step 2: Test Database Connection

```bash
# Inside SSH session
cd /home/site/wwwroot
python manage.py shell

# In Python shell:
from django.conf import settings
print(settings.DATABASES)

# Test connection
from django.db import connection
connection.ensure_connection()
print("Database connected!")
```

### Step 3: Fix Common Issues

#### Issue A: Port Binding
The app should bind to port from environment variable. Check startup.sh:

```bash
# Should use $PORT environment variable
exec gunicorn health_assistant.wsgi:application --bind=0.0.0.0:$PORT
```

#### Issue B: Missing ML Folder
ML predictions will show warnings but shouldn't crash the app. Check:

```bash
ls -la /home/site/wwwroot/
# ML folder won't be there yet - that's OK for now
```

#### Issue C: Database Migrations
Run migrations manually:

```bash
cd /home/site/wwwroot
python manage.py migrate
python manage.py createsuperuser
```

### Step 4: Alternative Deployment Method

If the current deployment isn't working, try using Azure Portal:

1. Go to Azure Portal → Your App Service
2. Click "Deployment Center"
3. Choose "Local Git" or "GitHub Actions"
4. Push code manually

### Step 5: Simplified Startup Script

Create a minimal startup script to test:

```bash
#!/bin/bash
cd /home/site/wwwroot
exec gunicorn health_assistant.wsgi:application --bind=0.0.0.0:8000 --workers=1 --timeout=300 --log-level=debug
```

### Step 6: Check Environment Variables

```bash
az webapp config appsettings list \
  --name cpsu-health-backend \
  --resource-group cpsu-health-assistant-rg \
  --query "[].{name:name, value:value}" \
  --output table
```

Ensure these are set:
- `DEBUG=False`
- `USE_POSTGRESQL=True`
- `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`
- `SECRET_KEY`
- `DJANGO_ALLOWED_HOSTS`
- `WEBSITES_PORT=8000`

### Step 7: Upload ML Folder (After App Works)

Once the Django app is running:

```bash
# Create ML folder in Azure
az webapp ssh --name cpsu-health-backend --resource-group cpsu-health-assistant-rg

# Inside SSH:
cd /home/site/wwwroot/..
mkdir -p ML/models
mkdir -p ML/Datasets/active

# Exit SSH and upload via Kudu
# Go to: https://cpsu-health-backend.scm.azurewebsites.net/ZipDeployUI
# Upload ML.zip (create locally first)
```

### Step 8: Create ML.zip Locally

```bash
# On your local machine
cd /path/to/VirtualAssistant
# Create zip (exclude Python cache)
tar -czf ML.tar.gz ML/ --exclude="*.pyc" --exclude="__pycache__"

# Or use Python
python -c "import shutil; shutil.make_archive('ML', 'zip', 'ML')"
```

## Quick Fixes

### Fix 1: Update startup.sh to be more robust

```bash
#!/bin/bash
set -x  # Print commands

echo "=========================================="
echo "Starting CPSU Health Backend"
echo "=========================================="

cd /home/site/wwwroot || exit 1

echo "Environment variables:"
env | grep -E "DB_|DEBUG|SECRET"

echo "Collecting static files..."
python manage.py collectstatic --noinput 2>&1 || echo "Static collection failed, continuing..."

echo "Running migrations..."
python manage.py migrate --noinput 2>&1 || echo "Migrations failed, continuing..."

echo "Starting Gunicorn on port ${WEBSITES_PORT:-8000}..."
exec gunicorn health_assistant.wsgi:application \
  --bind=0.0.0.0:${WEBSITES_PORT:-8000} \
  --workers=2 \
  --timeout=300 \
  --access-logfile '-' \
  --error-logfile '-' \
  --log-level info \
  --capture-output
```

### Fix 2: Update settings.py to handle Azure-specific paths

```python
# In settings.py, update STATIC settings:
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Ensure ALLOWED_HOSTS handles Azure correctly
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',')
if not ALLOWED_HOSTS or ALLOWED_HOSTS == ['']:
    ALLOWED_HOSTS = ['*']  # Fallback for development
```

## Testing After Fixes

```bash
# Test health endpoint
curl https://cpsu-health-backend.azurewebsites.net/api/

# Test with timeout
curl --max-time 30 https://cpsu-health-backend.azurewebsites.net/api/

# Check if site is responding
curl -I https://cpsu-health-backend.azurewebsites.net/
```

## Resources

- Azure App Service Logs: `az webapp log tail --name cpsu-health-backend --resource-group cpsu-health-assistant-rg`
- Kudu Console: https://cpsu-health-backend.scm.azurewebsites.net/
- Azure Portal: https://portal.azure.com

## Contact for Help

If issues persist:
1. Check Azure Portal → App Service → Diagnose and solve problems
2. Review deployment logs in Kudu
3. Test database connection from local machine
4. Consider using Docker container deployment instead
