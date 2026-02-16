# Azure Static Web Apps Deployment Guide

## 🚀 Quick Start

### Method 1: Simple Deployment (Recommended - No GitHub Issues)

**Windows:**
```bash
cd Vue
scripts\azure-deploy-simple.bat
```

**Linux/Mac:**
```bash
cd Vue
chmod +x scripts/azure-deploy-simple.sh
./scripts/azure-deploy-simple.sh
```

This method:
- ✅ No GitHub authentication required
- ✅ Deploys directly using Azure SWA CLI
- ✅ Works immediately after creation
- ✅ Manual deployment control

---

### Method 2: GitHub Actions (CI/CD)

If you want automatic deployments on every push:

**Step 1: Create GitHub Personal Access Token**

1. Go to: https://github.com/settings/tokens/new
2. Note: "Azure Static Web Apps - CPSU Health Assistant"
3. Expiration: 90 days (or your preference)
4. Select scopes:
   - ✅ `repo` (full control)
   - ✅ `workflow`
   - ✅ `write:packages`
   - ✅ `read:org`
5. Click "Generate token"
6. Copy the token (starts with `ghp_...`)

**Step 2: Deploy with GitHub Integration**

```bash
# Linux/Mac
export GITHUB_TOKEN=ghp_your_token_here
./scripts/azure-deploy-github.sh

# Windows (CMD)
set GITHUB_TOKEN=ghp_your_token_here
scripts\azure-deploy-github.bat

# Windows (PowerShell)
$env:GITHUB_TOKEN = "ghp_your_token_here"
.\scripts\azure-deploy-github.sh
```

---

## 📋 Prerequisites

1. **Azure CLI installed:**
   - Windows: https://aka.ms/installazurecliwindows
   - Linux/Mac: `curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash`

2. **Azure account logged in:**
   ```bash
   az login
   ```

3. **Node.js 18+ installed**

4. **Azure subscription with Static Web Apps enabled**

---

## 🔧 Configuration

### Environment Variables (.env.production)

Already configured in the repository:

```env
VITE_API_BASE_URL=https://your-django-backend.azurewebsites.net/api
VITE_RASA_URL=https://your-rasa-server.com:5005
VITE_APP_NAME=CPSU Health Assistant
VITE_APP_VERSION=1.0.0
```

**Update after deployment:**

1. Deploy Django backend to Azure App Service
2. Update `VITE_API_BASE_URL` with actual backend URL
3. Rebuild and redeploy Vue app

---

### staticwebapp.config.json

Already configured with:
- ✅ SPA routing fallback
- ✅ CORS headers
- ✅ Security headers (CSP, X-Frame-Options)
- ✅ MIME types configuration
- ✅ 404 handling

---

## 📊 Deployment Details

### Resource Configuration

| Setting | Value |
|---------|-------|
| Resource Group | cpsu-health-assistant-rg |
| App Name | cpsu-health-assistant |
| Location | East Asia |
| SKU | Free |
| App Location | /Vue |
| Output Location | dist |
| Branch | main |

### Free Tier Limits

| Resource | Limit | Usage |
|----------|-------|-------|
| Bandwidth | 100 GB/month | ~10-20 GB |
| Storage | 0.5 GB | ~50 MB |
| Build time | 10 min/build | ~2 min |
| **Cost** | **$0/month** | **FREE** ✅ |

---

## 🌐 Post-Deployment Configuration

### 1. Configure Django CORS

After deployment, add your Azure URL to Django CORS settings:

**File:** `Django/health_assistant/settings.py`

```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',  # Development
    'https://cpsu-health-assistant.azurestaticapps.net',  # Production
]
```

### 2. Update Frontend API URL

If needed, update the production API URL:

```bash
# View current settings
az staticwebapp appsettings list \
  --name cpsu-health-assistant \
  --resource-group cpsu-health-assistant-rg

# Update settings
az staticwebapp appsettings set \
  --name cpsu-health-assistant \
  --resource-group cpsu-health-assistant-rg \
  --setting-names VITE_API_BASE_URL=https://your-backend.azurewebsites.net/api
```

### 3. Custom Domain (Optional)

```bash
# Add custom domain
az staticwebapp hostname set \
  --name cpsu-health-assistant \
  --resource-group cpsu-health-assistant-rg \
  --hostname health.cpsu.edu.ph

# Note: You'll need to add DNS records (TXT or CNAME) in your domain provider
```

---

## 🔍 Monitoring & Management

### View Deployment Status

```bash
# Show app details
az staticwebapp show \
  --name cpsu-health-assistant \
  --resource-group cpsu-health-assistant-rg \
  --output table

# Get app URL
az staticwebapp show \
  --name cpsu-health-assistant \
  --resource-group cpsu-health-assistant-rg \
  --query "defaultHostname" -o tsv
```

### View Logs

```bash
# View application logs
az staticwebapp logs show \
  --name cpsu-health-assistant \
  --resource-group cpsu-health-assistant-rg
```

### GitHub Actions (if using Method 2)

- View workflows: https://github.com/souchan25/virtualAssistantFinal/actions
- Manually trigger: Click "Run workflow" button
- Check build logs for errors

---

## 🔄 Update Deployment

### Manual Update (Method 1 users)

```bash
cd Vue

# Make your changes to code...

# Rebuild and redeploy
npm run build
swa deploy ./dist \
  --deployment-token YOUR_TOKEN \
  --app-location . \
  --output-location dist \
  --env production
```

Or simply run the script again:
```bash
./scripts/azure-deploy-simple.sh  # Linux/Mac
scripts\azure-deploy-simple.bat   # Windows
```

### Automatic Update (Method 2 users)

Just push to GitHub:
```bash
git add .
git commit -m "Update Vue app"
git push origin main
# GitHub Actions automatically deploys! 🚀
```

---

## 🛠️ Troubleshooting

### Issue: "Deployment failed"

**Check:**
1. Azure CLI is logged in: `az account show`
2. Subscription is active: `az account list --output table`
3. Build succeeds locally: `npm run build`

### Issue: "CORS error in browser"

**Fix:**
1. Add Azure URL to Django CORS_ALLOWED_ORIGINS
2. Restart Django server
3. Check browser console for exact error

### Issue: "404 on refresh"

**Fix:**
Already handled by `staticwebapp.config.json` → All routes redirect to index.html

### Issue: "Assets not loading"

**Check:**
1. Build completed: `ls -la dist/`
2. Images in `src/assets/` are included
3. Vite base path is correct (should be `/`)

---

## 🗑️ Delete Deployment

### Delete Static Web App Only

```bash
az staticwebapp delete \
  --name cpsu-health-assistant \
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

## 📚 Additional Resources

- [Azure Static Web Apps Documentation](https://docs.microsoft.com/en-us/azure/static-web-apps/)
- [SWA CLI Documentation](https://azure.github.io/static-web-apps-cli/)
- [Vue.js Deployment Guide](https://vitejs.dev/guide/static-deploy.html)
- [Azure Free Services](https://azure.microsoft.com/en-us/free/)

---

## ✅ Deployment Checklist

Before deployment:
- [ ] Azure CLI installed and logged in
- [ ] Node.js 18+ installed
- [ ] Vue app builds successfully (`npm run build`)
- [ ] `.env.production` configured
- [ ] `staticwebapp.config.json` present

After deployment:
- [ ] App accessible at Azure URL
- [ ] Django CORS configured with Azure URL
- [ ] All routes work (login, dashboard, staff pages)
- [ ] Assets (images, CSS) loading correctly
- [ ] API calls to backend working
- [ ] Test on mobile devices

---

## 🎯 Next Steps

1. ✅ **Deploy Vue to Azure Static Web Apps** (THIS GUIDE)
2. ⏭️ **Deploy Django to Azure App Service**
   - Use Azure App Service for Linux (Free/Basic tier)
   - Or Azure Container Instances (Docker)
3. ⏭️ **Deploy Rasa (Optional)**
   - Azure Container Instances
   - Or keep using local Rasa server
4. ⏭️ **Configure Database**
   - Azure Database for PostgreSQL (has free tier)
   - Or keep using SQLite (development only)

---

**Questions?** Check the [main documentation](../README.md) or Django backend docs!
