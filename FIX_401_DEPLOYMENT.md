# 🔧 Fix 401 Deployment Error

## The Problem

The deployment is getting **401 Unauthorized** because:
- Username length: 8 (too short)
- Password length: 8 (too short)

Azure publish profile credentials are usually **60+ characters long**, so 8 characters means the credential extraction is failing.

## Quick Fix: Use Azure CLI Deployment Instead

Since the publish profile credential extraction isn't working reliably, let's deploy directly using Azure CLI:

### Option 1: Deploy via Azure CLI (Recommended - Works Now!)

Run these commands locally:

```bash
# 1. Navigate to Django folder
cd Django

# 2. Create deployment package
zip -r ../django-deploy.zip . \
  -x "*.pyc" \
  -x "*__pycache__*" \
  -x "*.sqlite3" \
  -x ".git/*" \
  -x "venv/*" \
  -x "*.log"

# 3. Deploy using Azure CLI
az webapp deploy \
  --resource-group cpsu-health-assistant-rg \
  --name cpsu-health-backend \
  --src-path ../django-deploy.zip \
  --type zip \
  --async false

# 4. Restart the app
az webapp restart \
  --name cpsu-health-backend \
  --resource-group cpsu-health-assistant-rg

# 5. Test deployment
curl https://cpsu-health-backend.azurewebsites.net/api/
```

**This will work immediately** because you're already logged into Azure CLI!

---

### Option 2: Fix GitHub Actions (For Future Automated Deploys)

The GitHub Actions workflow needs the **real** (unredacted) credentials.

#### Get Unredacted Credentials

```bash
# Get fresh publish profile
az webapp deployment list-publishing-profiles \
  --name cpsu-health-backend \
  --resource-group cpsu-health-assistant-rg \
  --xml > publish-profile-real.xml

# View it (copy the ENTIRE content)
cat publish-profile-real.xml
```

#### Update GitHub Secret

1. Copy **ALL** content from `publish-profile-real.xml`
2. Go to: GitHub → Settings → Secrets → Actions
3. Edit `AZURE_WEBAPP_PUBLISH_PROFILE`
4. **Delete everything** and paste new content
5. Make sure NO characters are cut off!
6. Save

#### Verify the Secret

The publish profile should contain:
- **3 profiles**: Web Deploy, FTP, Zip Deploy
- **Long usernames**: Like `$cpsu-health-backend` or `cpsu-health-backend\$cpsu-health-backend`
- **Long passwords**: 60+ random characters
- **Total size**: ~1.5 KB

If you see "REDACTED" anywhere, that's wrong!

---

### Option 3: Use Deployment Center (Azure Portal)

1. Go to: https://portal.azure.com
2. Find: cpsu-health-backend (App Service)
3. Click: **Deployment Center**
4. Choose: **GitHub**
5. Select: Your repository
6. Select: `master` branch
7. Azure will set up GitHub Actions automatically!

This creates a workflow with built-in Azure credentials (no manual secret needed).

---

## 🚀 Recommended: Deploy Now via Azure CLI

Since you're already logged into Azure CLI, **Option 1 is the fastest**:

```bash
cd Django
zip -r ../django-deploy.zip . -x "*.pyc" -x "*__pycache__*" -x "*.sqlite3"
az webapp deploy --resource-group cpsu-health-assistant-rg --name cpsu-health-backend --src-path ../django-deploy.zip --type zip
az webapp restart --name cpsu-health-backend --resource-group cpsu-health-assistant-rg
```

**Time: 3-4 minutes**  
**Works: Immediately**  
**No secrets needed: You're already authenticated**

---

## ✅ After Deployment

Test your deployed app:

```bash
# Health check
curl https://cpsu-health-backend.azurewebsites.net/

# API check
curl https://cpsu-health-backend.azurewebsites.net/api/

# Admin panel
open https://cpsu-health-backend.azurewebsites.net/admin/
```

---

## 🎯 Why This Happened

The GitHub Actions workflow is trying to extract credentials from the publish profile XML, but:
1. The XML might be malformed in the GitHub secret
2. Special characters might have been escaped
3. The secret might have been truncated
4. The extraction regex might not match the format

**Azure CLI deployment avoids all these issues!**

---

## 📝 Next Steps After Deployment Works

1. ✅ Deploy Django (use Azure CLI - Option 1)
2. ✅ Test the API
3. ✅ Upload ML models
4. ✅ Update Vue frontend
5. Fix GitHub Actions later (optional)

For now, **just use Azure CLI to deploy** - it's faster and more reliable!
