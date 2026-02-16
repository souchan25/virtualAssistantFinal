# 🔐 Get GitHub Actions Credentials

## Quick Setup Guide

Follow these steps to get the credentials needed for GitHub Actions.

## Step 1: Get Azure Publish Profile

**Already done!** ✅ 

The file `publish-profile.xml` has been created in your project root.

**To view it:**

```bash
cat publish-profile.xml
```

**What to do with it:**

1. Copy the entire contents of `publish-profile.xml`
2. Go to your GitHub repository
3. Settings → Secrets and variables → Actions
4. Click "New repository secret"
5. Name: `AZURE_WEBAPP_PUBLISH_PROFILE`
6. Value: Paste the entire XML content
7. Click "Add secret"

---

## Step 2: Get Azure Service Principal

Due to path issues with Git Bash, please run this command in **PowerShell** or **CMD**:

### Option A: Using PowerShell (Recommended)

```powershell
az ad sp create-for-rbac `
  --name "github-actions-cpsu-health" `
  --role contributor `
  --scopes /subscriptions/302b6181-2931-4203-8580-9491e1797b2a/resourceGroups/cpsu-health-assistant-rg `
  --sdk-auth
```

### Option B: Using CMD

```cmd
az ad sp create-for-rbac --name "github-actions-cpsu-health" --role contributor --scopes /subscriptions/302b6181-2931-4203-8580-9491e1797b2a/resourceGroups/cpsu-health-assistant-rg --sdk-auth
```

### Option C: Simplified (Subscription-level)

If the above doesn't work, grant access to the entire subscription:

```powershell
az ad sp create-for-rbac `
  --name "github-actions-cpsu-health" `
  --role contributor `
  --scopes /subscriptions/302b6181-2931-4203-8580-9491e1797b2a `
  --sdk-auth
```

**Expected output:**

```json
{
  "clientId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "clientSecret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "subscriptionId": "302b6181-2931-4203-8580-9491e1797b2a",
  "tenantId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
  "resourceManagerEndpointUrl": "https://management.azure.com/",
  "activeDirectoryGraphResourceId": "https://graph.windows.net/",
  "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
  "galleryEndpointUrl": "https://gallery.azure.com/",
  "managementEndpointUrl": "https://management.core.windows.net/"
}
```

**What to do with it:**

1. Copy the entire JSON output (including the `{}`)
2. Go to your GitHub repository
3. Settings → Secrets and variables → Actions
4. Click "New repository secret"
5. Name: `AZURE_CREDENTIALS`
6. Value: Paste the entire JSON
7. Click "Add secret"

---

## Step 3: Add Django Secret Key

**Value:**
```
M4wjF-dzGTT0pGUswWNdEchzq426mlCsgtzR9P8YiMlb8yZO_e2CKfZyg7ohOh0hWjQ
```

**What to do:**

1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `DJANGO_SECRET_KEY`
5. Value: Paste the secret key above
6. Click "Add secret"

---

## Summary of GitHub Secrets to Add

| Secret Name | Where to Get It | Status |
|-------------|----------------|--------|
| `AZURE_WEBAPP_PUBLISH_PROFILE` | `publish-profile.xml` file | ✅ Ready |
| `AZURE_CREDENTIALS` | Run PowerShell command above | ⏳ Run command |
| `DJANGO_SECRET_KEY` | Copy from above | ✅ Ready |

---

## Alternative: Use Azure Portal

If Azure CLI commands don't work, you can get the publish profile from Azure Portal:

1. Go to https://portal.azure.com
2. Navigate to your App Service: `cpsu-health-backend`
3. Click "Get publish profile" in the top menu
4. Save the downloaded file
5. Copy its contents to GitHub secret

---

## Verify Setup

After adding all secrets, you should see 3 secrets in:
**GitHub Repo → Settings → Secrets and variables → Actions**

✅ `AZURE_WEBAPP_PUBLISH_PROFILE`  
✅ `AZURE_CREDENTIALS`  
✅ `DJANGO_SECRET_KEY`

---

## Test the Setup

Once secrets are added:

```bash
# Commit and push the GitHub Actions workflows
git add .github/
git commit -m "Add GitHub Actions CI/CD"
git push origin master

# Watch the deployment
# Go to: https://github.com/YOUR_USERNAME/YOUR_REPO/actions
```

The first deployment will start automatically!

---

## Troubleshooting

### Can't create service principal?

**Solution:** You might not have sufficient permissions. Try:

1. Ask your Azure subscription admin to create the service principal
2. Or use Azure Portal to create a deployment credential
3. Or use just the publish profile (simpler, but less features)

### GitHub Actions still failing?

**Solution:** Check the workflow logs in GitHub Actions tab for specific error messages.

For the ML upload workflow, if you don't want to use service principal, you can simplify it to only use the publish profile - I can update the workflow if needed.
