#!/bin/bash
# Upload ML folder to Azure App Service
# Required for ML predictions to work

set -e

echo "📦 Uploading ML Models to Azure"
echo "================================"

RESOURCE_GROUP="cpsu-health-assistant-rg"
APP_NAME="cpsu-health-backend"

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI not found"
    exit 1
fi

# Check if logged in
if ! az account show &> /dev/null; then
    echo "❌ Not logged in. Run: az login"
    exit 1
fi

echo "✅ Azure authentication OK"
echo ""

# Navigate to project root
cd "$(dirname "$0")/../.."

# Check if ML folder exists
if [ ! -d "ML" ]; then
    echo "❌ ML folder not found"
    echo "Please run this script from the VirtualAssistant directory"
    exit 1
fi

echo "📂 Found ML folder"
echo "   - models/disease_predictor_v2.pkl"
echo "   - Datasets/active/*.csv"
echo ""

# Create zip of ML folder
echo "Creating ML.zip..."
cd ML
zip -r ../ML.zip . -x "*.pyc" -x "__pycache__/*" -x "*.git/*"
cd ..

echo "✅ ML.zip created"
echo ""

# Upload to Azure using Kudu API
echo "Uploading to Azure App Service..."

# Get publishing credentials
CREDS=$(az webapp deployment list-publishing-credentials \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query "{username:publishingUserName, password:publishingPassword}" -o json)

USERNAME=$(echo $CREDS | jq -r '.username')
PASSWORD=$(echo $CREDS | jq -r '.password')

# Upload zip to wwwroot/ML
echo "Uploading ML.zip to Azure..."
curl -X PUT \
  -u "$USERNAME:$PASSWORD" \
  --data-binary @ML.zip \
  https://$APP_NAME.scm.azurewebsites.net/api/zip/site/wwwroot/ML/

echo ""
echo "✅ ML folder uploaded to Azure!"
echo ""

# Clean up
rm ML.zip

echo "🧹 Cleaned up local ML.zip"
echo ""
echo "✅ Done! ML models are now available on Azure."
echo "   Path: /home/site/wwwroot/ML/"
echo ""
