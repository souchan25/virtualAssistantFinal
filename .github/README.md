# 🚀 GitHub Actions CI/CD for CPSU Health Assistant

## What is This?

This folder contains automated deployment workflows using GitHub Actions. Instead of manually deploying with Azure CLI, you can now **just push to GitHub** and the deployment happens automatically!

## ✨ Features

✅ **Automated Django Deployment** - Push code → Auto-deploys to Azure  
✅ **Automated ML Upload** - Update models → Auto-uploads to Azure  
✅ **Continuous Testing** - Runs tests on every push/PR  
✅ **No manual commands** - Everything happens on git push  
✅ **Deployment history** - See all deployments in GitHub Actions tab  
✅ **Easy rollback** - Just revert commit and push  

## 🎯 Quick Start (3 Steps)

### Step 1: Add GitHub Secrets

You need to add 3 secrets to your GitHub repository:

1. **`AZURE_WEBAPP_PUBLISH_PROFILE`**
   - File: `publish-profile.xml` (already created in project root)
   - Copy the XML contents to GitHub secret

2. **`DJANGO_SECRET_KEY`**
   - Value: `M4wjF-dzGTT0pGUswWNdEchzq426mlCsgtzR9P8YiMlb8yZO_e2CKfZyg7ohOh0hWjQ`

3. **`AZURE_CREDENTIALS`** (Optional - only for advanced ML upload)
   - Run command in PowerShell (see `GET_CREDENTIALS.md`)

**How to add secrets:**
1. Go to GitHub repo → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add each secret

📖 **Detailed instructions:** See `GET_CREDENTIALS.md`

### Step 2: Push to GitHub

```bash
# Add all GitHub Actions workflows
git add .github/
git commit -m "Add GitHub Actions CI/CD"
git push origin master
```

### Step 3: Watch It Deploy! 🎉

Go to: `https://github.com/YOUR_USERNAME/YOUR_REPO/actions`

You'll see:
- ✅ Django deployment starting
- ✅ Tests running
- ✅ Deployment status

## 📋 Available Workflows

### 1. Deploy Django to Azure (`azure-django-deploy.yml`)

**Triggers:** Push to `master` with changes in `Django/` folder

**What it does:**
- Installs Python dependencies
- Runs Django checks
- Collects static files
- Deploys to Azure App Service

**Manual trigger:** GitHub Actions → "Deploy Django to Azure App Service" → Run workflow

### 2. Upload ML Models (`upload-ml-models-simple.yml`)

**Triggers:** Push to `master` with changes in `ML/models/` or `ML/Datasets/active/`

**What it does:**
- Creates ML.zip package
- Uploads to Azure via Kudu API
- Restarts the web app

**Manual trigger:** GitHub Actions → "Upload ML Models to Azure" → Run workflow

### 3. CI Tests (`ci-tests.yml`)

**Triggers:** Every push and pull request

**What it does:**
- Runs Django tests with PostgreSQL
- Validates ML models and datasets
- Checks code coverage
- Reports test results

## 🎓 Usage Examples

### Deploy Django Changes

```bash
# Edit Django code
vim Django/clinic/views.py

# Commit and push - deployment happens automatically!
git add Django/
git commit -m "Update API endpoint"
git push origin master

# Watch deployment in GitHub Actions tab
```

### Update ML Models

```bash
# Retrain model
cd ML/scripts
python train_model_realistic.py

# Commit and push - upload happens automatically!
cd ../..
git add ML/models/
git commit -m "Update ML model"
git push origin master

# Watch upload in GitHub Actions tab
```

### Create a Pull Request (with tests)

```bash
# Create feature branch
git checkout -b feature/new-symptom

# Make changes
vim Django/clinic/models.py

# Push to create PR
git push origin feature/new-symptom

# Tests run automatically on the PR!
```

## 🆚 Comparison: GitHub Actions vs Manual

| Feature | Manual Deployment | GitHub Actions |
|---------|------------------|----------------|
| Deploy command | `az webapp up ...` | `git push` |
| Time to deploy | 5-10 minutes | 3-5 minutes |
| Consistency | Error-prone | 100% consistent |
| Team collaboration | Everyone needs Azure CLI | Just need Git |
| Rollback | Complex | `git revert` + push |
| Deployment logs | Hard to find | In GitHub Actions tab |
| Testing | Manual | Automatic |
| ML upload | Separate command | Automatic |

## 🔧 Troubleshooting

### Deployment failing?

1. Check workflow logs in GitHub Actions tab
2. Verify secrets are set correctly
3. Check Azure App Service logs:
   ```bash
   az webapp log tail --name cpsu-health-backend --resource-group cpsu-health-assistant-rg
   ```

### Missing secrets?

See `GET_CREDENTIALS.md` for detailed instructions on getting credentials.

### Want to test locally first?

You can still use manual deployment:
```bash
cd Django
az webapp up --name cpsu-health-backend --resource-group cpsu-health-assistant-rg --runtime "PYTHON:3.11"
```

## 📚 Documentation

- **`SETUP_GITHUB_ACTIONS.md`** - Comprehensive setup guide
- **`GET_CREDENTIALS.md`** - How to get Azure credentials
- **`workflows/`** - Workflow files (YAML)

## 🎉 Benefits

**For You:**
- ⏰ Save time - no manual deployments
- 🛡️ Fewer errors - automated testing
- 📊 Better visibility - see deployment history
- 🔄 Easy rollback - just revert commits

**For Your Team:**
- 👥 Everyone can deploy - just push to Git
- 📝 Deployment documentation - workflows are self-documenting
- 🧪 Confidence - tests run before deployment
- 🚀 Faster iteration - quick feedback loop

## 🚀 Next Steps

1. ✅ Add GitHub secrets (see Step 1 above)
2. ✅ Push workflows to GitHub
3. ✅ Watch first deployment
4. ✅ Update Vue frontend to use Azure backend URL
5. ✅ Set up branch protection rules (optional)
6. ✅ Add deployment notifications (optional)

---

**Ready to deploy?** Just `git push`! 🚀
