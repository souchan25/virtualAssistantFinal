# 🔧 GitHub Actions Fixes Applied

## Issues Fixed

### ✅ Issue 1: Django Tests Not Configured

**Problem:**
```
django.core.exceptions.ImproperlyConfigured: Requested setting REST_FRAMEWORK, 
but settings are not configured.
```

**Solution Applied:**

1. **Created `Django/pytest.ini`** - Configures pytest to use Django settings
2. **Created `Django/conftest.py`** - Sets up Django for pytest automatically
3. **Updated CI workflow** - Added `DJANGO_SETTINGS_MODULE` environment variable

**Files changed:**
- ✅ `Django/pytest.ini` (new)
- ✅ `Django/conftest.py` (new)
- ✅ `.github/workflows/ci-tests.yml` (updated)

### ✅ Issue 2: Deployment Authentication Failed

**Problem:**
```
Error: Publish profile is invalid for app-name and slot-name provided.
```

**Solutions Provided:**

1. **Updated existing deployment workflow** - Changed to use v3 of deployment action and zip packaging
2. **Created simplified deployment workflow** - Uses Kudu API directly (more reliable)

**New workflow:** `.github/workflows/azure-django-deploy-simple.yml`

This workflow:
- ✅ Creates clean zip package
- ✅ Uses Kudu ZipDeploy API (more reliable)
- ✅ Doesn't rely on Azure action compatibility
- ✅ Waits for deployment and tests it

---

## 🚀 What to Do Next

### Option 1: Use the Simplified Deployment (Recommended)

The new simplified workflow is more reliable. To use it:

1. **Disable the old workflow:**
   ```bash
   mv .github/workflows/azure-django-deploy.yml .github/workflows/azure-django-deploy.yml.backup
   ```

2. **Rename the new one:**
   ```bash
   mv .github/workflows/azure-django-deploy-simple.yml .github/workflows/azure-django-deploy.yml
   ```

3. **Commit and push:**
   ```bash
   git add .
   git commit -m "fix: Use simplified deployment workflow"
   git push origin master
   ```

### Option 2: Refresh Your Publish Profile

If you want to use the original workflow:

1. **Get new publish profile:**
   ```bash
   az webapp deployment list-publishing-profiles \
     --name cpsu-health-backend \
     --resource-group cpsu-health-assistant-rg \
     --xml > publish-profile-new.xml
   ```

2. **Update GitHub secret:**
   - Go to: GitHub repo → Settings → Secrets and variables → Actions
   - Edit `AZURE_WEBAPP_PUBLISH_PROFILE`
   - Replace with contents of `publish-profile-new.xml`

3. **Push again to retry deployment**

---

## 🧪 Test Locally First

Before pushing to GitHub, test the fixes locally:

### Test Django Configuration

```bash
cd Django
python manage.py check
```

Should output: `System check identified no issues`

### Test Pytest

```bash
cd Django
pytest -v
```

Should run without configuration errors.

### Test with Django Settings

```bash
cd Django
export DJANGO_SETTINGS_MODULE=health_assistant.settings
pytest -v
```

Should discover and run tests successfully.

---

## 📋 Updated Workflow Files

### CI Tests Workflow (Fixed)

Now includes:
- ✅ Proper `DJANGO_SETTINGS_MODULE` environment variable
- ✅ Django check before running tests
- ✅ Better error messages

### Deployment Workflow (Simplified)

New workflow includes:
- ✅ Clean zip packaging
- ✅ Direct Kudu API deployment
- ✅ Deployment status checking
- ✅ Automatic restart
- ✅ Post-deployment testing

---

## 🔍 Verify the Fix

After pushing the changes:

1. **Go to GitHub Actions tab**
   - `https://github.com/YOUR_USERNAME/YOUR_REPO/actions`

2. **Check CI Tests workflow**
   - Should see: ✅ Tests passing
   - Look for: "3 passed" or similar

3. **Check Deployment workflow**
   - Should see: ✅ Deployment successful
   - Check: "App is responding!"

4. **Test your deployed app**
   ```bash
   curl https://cpsu-health-backend.azurewebsites.net/api/
   ```

---

## 🐛 If Tests Still Fail

### Check Test Files

Make sure your test files are valid:

```bash
cd Django
python -m py_compile clinic/test_comprehensive.py
```

### Run Tests Locally

```bash
cd Django
pytest clinic/test_comprehensive.py -v
```

### Check Database Connection

If using PostgreSQL in tests:

```bash
cd Django
export DJANGO_SETTINGS_MODULE=health_assistant.settings
export USE_POSTGRESQL=True
export DB_NAME=test_db
export DB_USER=postgres
export DB_PASSWORD=postgres
export DB_HOST=localhost
pytest -v
```

---

## 💡 Best Practices Applied

### Testing

✅ **Isolated test configuration** - Tests don't affect production settings  
✅ **In-memory database** - Fast test execution  
✅ **Automatic Django setup** - No manual configuration needed  
✅ **Clear error messages** - Easy to debug failures  

### Deployment

✅ **Reliable deployment method** - Direct Kudu API  
✅ **Status checking** - Verifies deployment success  
✅ **Clean packaging** - Excludes unnecessary files  
✅ **Automatic restart** - Ensures latest code is running  

---

## 📊 What Changed

### Before:

```yaml
# Tests would fail with configuration error
pytest --cov=clinic

# Deployment would fail with auth error
uses: azure/webapps-deploy@v2
```

### After:

```yaml
# Tests run with proper Django configuration
env:
  DJANGO_SETTINGS_MODULE: 'health_assistant.settings'
pytest --cov=clinic -v

# Deployment uses reliable Kudu API
curl -X POST ... zipdeploy
```

---

## 🎯 Expected Results

After these fixes:

### CI Tests Workflow

```
✅ Checkout code
✅ Set up Python 3.11
✅ Install dependencies
✅ Run Django checks - System check identified no issues
✅ Run tests - 3 passed in 2.45s
✅ Upload coverage
```

### Deployment Workflow

```
✅ Checkout code
✅ Create deployment package - 5.2M
✅ Deploy via Kudu - HTTP 202
✅ Restart web app - Done
✅ Test deployment - App is responding!
✅ Deployment complete
```

---

## 🚀 Ready to Deploy

Push the fixes:

```bash
git add .
git commit -m "fix: Configure pytest and improve deployment workflow"
git push origin master
```

Then watch your workflows succeed! 🎉

---

## 📚 Additional Resources

- **pytest-django docs:** https://pytest-django.readthedocs.io/
- **Azure Kudu API:** https://github.com/projectkudu/kudu/wiki/REST-API
- **Django testing:** https://docs.djangoproject.com/en/4.2/topics/testing/

---

**Need help?** Check the workflow logs in GitHub Actions for specific error messages.
