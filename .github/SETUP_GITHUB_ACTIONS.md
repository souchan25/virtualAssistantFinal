# 🚀 GitHub Actions Setup Guide

## Overview

We've created 3 GitHub Actions workflows for automated deployment:

1. **`azure-django-deploy.yml`** - Deploys Django backend to Azure
2. **`upload-ml-models.yml`** - Uploads ML models to Azure
3. **`ci-tests.yml`** - Runs tests and validation on every push/PR

## 📋 Prerequisites

- GitHub repository for your code
- Azure App Service already created (✅ you have this)
- Azure subscription (✅ Azure for Students)

## 🔐 Required GitHub Secrets

You need to add these secrets to your GitHub repository:

### 1. AZURE_WEBAPP_PUBLISH_PROFILE

This contains Azure App Service credentials.

**How to get it:**

```bash
# Download publish profile
az webapp deployment list-publishing-profiles \
  --name cpsu-health-backend \
  --resource-group cpsu-health-assistant-rg \
  --xml > publish-profile.xml

# Copy the contents
cat publish-profile.xml
```

**How to add to GitHub:**
1. Go to your GitHub repo
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `AZURE_WEBAPP_PUBLISH_PROFILE`
5. Value: Paste the entire XML content from publish-profile.xml
6. Click "Add secret"

### 2. DJANGO_SECRET_KEY

Your Django secret key for production.

**Value:**
```
M4wjF-dzGTT0pGUswWNdEchzq426mlCsgtzR9P8YiMlb8yZO_e2CKfZyg7ohOh0hWjQ
```

**How to add to GitHub:**
1. Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `DJANGO_SECRET_KEY`
4. Value: Paste the secret key above
5. Click "Add secret"

### 3. AZURE_CREDENTIALS (for ML upload workflow)

Azure Service Principal credentials.

**How to create:**

```bash
# Create service principal
az ad sp create-for-rbac \
  --name "github-actions-cpsu-health" \
  --role contributor \
  --scopes /subscriptions/302b6181-2931-4203-8580-9491e1797b2a/resourceGroups/cpsu-health-assistant-rg \
  --sdk-auth

# This will output JSON like:
# {
#   "clientId": "...",
#   "clientSecret": "...",
#   "subscriptionId": "302b6181-2931-4203-8580-9491e1797b2a",
#   "tenantId": "...",
#   ...
# }
```

**How to add to GitHub:**
1. Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `AZURE_CREDENTIALS`
4. Value: Paste the entire JSON output
5. Click "Add secret"

## 📝 Quick Setup Commands

Run these commands to set everything up:

```bash
# 1. Download publish profile
az webapp deployment list-publishing-profiles \
  --name cpsu-health-backend \
  --resource-group cpsu-health-assistant-rg \
  --xml

# 2. Create service principal
az ad sp create-for-rbac \
  --name "github-actions-cpsu-health" \
  --role contributor \
  --scopes /subscriptions/302b6181-2931-4203-8580-9491e1797b2a/resourceGroups/cpsu-health-assistant-rg \
  --sdk-auth
```

Then add both outputs to GitHub Secrets.

## 🎯 How to Use

### Automatic Deployment (Recommended)

1. **Push Django changes:**
   ```bash
   git add Django/
   git commit -m "Update Django backend"
   git push origin master
   ```
   - Triggers `azure-django-deploy.yml`
   - Deploys Django code to Azure automatically

2. **Push ML changes:**
   ```bash
   git add ML/
   git commit -m "Update ML models"
   git push origin master
   ```
   - Triggers `upload-ml-models.yml`
   - Uploads ML models to Azure automatically

### Manual Deployment

You can also trigger deployments manually:

1. Go to your GitHub repo
2. Click "Actions" tab
3. Select the workflow (e.g., "Deploy Django to Azure App Service")
4. Click "Run workflow"
5. Select branch and click "Run workflow"

## 🔄 Workflow Details

### 1. Django Deployment Workflow

**Triggers:**
- Push to `master` branch with changes in `Django/` folder
- Manual trigger via GitHub Actions UI

**Steps:**
1. ✅ Checkout code
2. ✅ Set up Python 3.11
3. ✅ Install dependencies
4. ✅ Run Django checks
5. ✅ Collect static files
6. ✅ Deploy to Azure App Service

**Duration:** ~3-5 minutes

### 2. ML Models Upload Workflow

**Triggers:**
- Push to `master` branch with changes in `ML/models/` or `ML/Datasets/active/`
- Manual trigger via GitHub Actions UI

**Steps:**
1. ✅ Checkout code
2. ✅ Create ML.zip package
3. ✅ Login to Azure
4. ✅ Upload via Kudu API
5. ✅ Restart web app

**Duration:** ~2-3 minutes

### 3. CI Tests Workflow

**Triggers:**
- Every push to `master`
- Every pull request

**Steps:**
1. ✅ Run Django tests with PostgreSQL
2. ✅ Run ML validation
3. ✅ Check code coverage
4. ✅ Upload coverage to Codecov

**Duration:** ~2-4 minutes

## 📊 Benefits of GitHub Actions

### vs Manual Deployment:

| Feature | Manual (az CLI) | GitHub Actions |
|---------|----------------|----------------|
| Deployment time | 5-10 minutes | 3-5 minutes |
| Consistency | Manual steps, prone to errors | Automated, consistent |
| Rollback | Manual, complex | Git revert + push |
| Testing | Manual | Automated on every push |
| Logs | Hard to find | Built into GitHub |
| Team collaboration | Everyone needs Azure CLI | Just push to Git |

### Advantages:

✅ **Automated** - Push and forget  
✅ **Tested** - Runs checks before deploying  
✅ **Versioned** - Deployment config in Git  
✅ **Visible** - See deployment status in GitHub  
✅ **Rollback** - Easy to revert to previous version  
✅ **Scalable** - Easy to add more environments (staging, production)

## 🧪 Testing the Setup

### 1. Test Django Deployment

```bash
# Make a small change
cd Django
echo "# Test change" >> README.md
git add .
git commit -m "test: GitHub Actions deployment"
git push origin master

# Watch deployment in GitHub Actions
# Go to: https://github.com/YOUR_USERNAME/YOUR_REPO/actions
```

### 2. Test ML Upload

```bash
# Update ML model or dataset
cd ML/models
touch test.txt
git add .
git commit -m "test: ML upload workflow"
git push origin master

# Watch in GitHub Actions
```

## 🔍 Troubleshooting

### Deployment fails with "unauthorized"

**Solution:** Check that `AZURE_WEBAPP_PUBLISH_PROFILE` secret is set correctly

```bash
# Re-download publish profile
az webapp deployment list-publishing-profiles \
  --name cpsu-health-backend \
  --resource-group cpsu-health-assistant-rg \
  --xml
```

### ML upload fails

**Solution:** Check that `AZURE_CREDENTIALS` is valid

```bash
# Recreate service principal
az ad sp create-for-rbac \
  --name "github-actions-cpsu-health-v2" \
  --role contributor \
  --scopes /subscriptions/302b6181-2931-4203-8580-9491e1797b2a/resourceGroups/cpsu-health-assistant-rg \
  --sdk-auth
```

### Workflow not triggering

**Solution:** Check the `paths` filter in workflow YAML

```yaml
on:
  push:
    branches:
      - master  # Make sure this matches your branch name
    paths:
      - 'Django/**'  # Check this path matches your structure
```

## 🎉 Success Checklist

After setup, you should be able to:

- [ ] Push Django changes and see them deploy automatically
- [ ] Push ML changes and see models upload automatically
- [ ] View deployment logs in GitHub Actions tab
- [ ] Access your app at: https://cpsu-health-backend.azurewebsites.net
- [ ] Roll back by reverting commit and pushing

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Azure App Service Deploy Action](https://github.com/Azure/webapps-deploy)
- [Azure Login Action](https://github.com/Azure/login)

## 💡 Next Steps

1. Set up GitHub secrets (see above)
2. Push code to trigger first deployment
3. Set up branch protection rules
4. Add staging environment (optional)
5. Set up deployment notifications (Slack, Discord, etc.)

---

**Need help?** Check the troubleshooting section or review workflow logs in GitHub Actions tab.
