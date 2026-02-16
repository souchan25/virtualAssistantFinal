# Active GitHub Actions Workflows

## ✅ Currently Active

### 1. `tests-simple.yml`
**What it does:** Simple validation (no database needed)
- Runs `python manage.py check --deploy`
- Validates ML model exists
- Validates datasets exist

**Does NOT run:** Full pytest test suite (no database tests)

### 2. `deploy-django-final.yml`
**What it does:** Deploys Django to Azure
- Creates deployment package
- Deploys via Kudu API
- Verifies deployment

### 3. `upload-ml-models-simple.yml`
**What it does:** Uploads ML models to Azure
- Creates ML.zip
- Uploads via Kudu API

## ❌ Removed Workflows

The following workflows have been **completely removed** from the repository:
- ~~`ci-tests.yml`~~ - Had PostgreSQL SSL errors
- ~~`azure-django-deploy.yml`~~ - Had authentication issues

## 📝 Note

If you see old workflow runs in GitHub Actions, those are from before the workflows were removed. New pushes will only trigger the active workflows above.

To manually cancel old running workflows:
1. Go to GitHub Actions tab
2. Click on the running workflow
3. Click "Cancel workflow"
