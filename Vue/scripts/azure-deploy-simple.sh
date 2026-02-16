#!/bin/bash
# Simple Azure Static Web Apps Deployment (No GitHub Integration)
# Use this method to avoid GitHub authentication issues

set -e  # Exit on error

echo "🚀 CPSU Health Assistant - Azure Static Web Apps Deployment"
echo "=========================================================="
echo ""

# Configuration
RESOURCE_GROUP="cpsu-health-assistant-rg"
APP_NAME="cpsu-health-assistant"
LOCATION="eastasia"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo -e "${RED}❌ Azure CLI not found. Install from: https://aka.ms/installazurecliwindows${NC}"
    exit 1
fi

# Check if logged in
echo -e "${BLUE}🔐 Checking Azure authentication...${NC}"
if ! az account show &> /dev/null; then
    echo -e "${RED}❌ Not logged in to Azure${NC}"
    echo "Run: az login"
    exit 1
fi

echo -e "${GREEN}✅ Azure authentication OK${NC}"
echo ""

# Create resource group if doesn't exist
echo -e "${BLUE}📦 Checking resource group...${NC}"
if ! az group show --name $RESOURCE_GROUP &> /dev/null; then
    echo "Creating resource group: $RESOURCE_GROUP"
    az group create --name $RESOURCE_GROUP --location $LOCATION --output table
    echo -e "${GREEN}✅ Resource group created${NC}"
else
    echo -e "${GREEN}✅ Resource group exists${NC}"
fi
echo ""

# Create Static Web App (without GitHub)
echo -e "${BLUE}🌐 Creating Azure Static Web App...${NC}"
if ! az staticwebapp show --name $APP_NAME --resource-group $RESOURCE_GROUP &> /dev/null; then
    az staticwebapp create \
      --name $APP_NAME \
      --resource-group $RESOURCE_GROUP \
      --location $LOCATION \
      --sku Free \
      --output table
    echo -e "${GREEN}✅ Static Web App created${NC}"
else
    echo -e "${GREEN}✅ Static Web App exists${NC}"
fi
echo ""

# Get deployment token
echo -e "${BLUE}🔑 Getting deployment token...${NC}"
DEPLOYMENT_TOKEN=$(az staticwebapp secrets list \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query "properties.apiKey" -o tsv)

if [ -z "$DEPLOYMENT_TOKEN" ]; then
    echo -e "${RED}❌ Failed to get deployment token${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Deployment token retrieved${NC}"
echo ""

# Get app URL
APP_URL=$(az staticwebapp show \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query "defaultHostname" -o tsv)

echo -e "${BLUE}📦 Installing dependencies...${NC}"
cd "$(dirname "$0")/.."  # Go to Vue directory
npm install
echo -e "${GREEN}✅ Dependencies installed${NC}"
echo ""

echo -e "${BLUE}🔨 Building Vue app...${NC}"
npm run build
echo -e "${GREEN}✅ Build complete${NC}"
echo ""

# Check if SWA CLI is installed
if ! command -v swa &> /dev/null; then
    echo -e "${BLUE}📥 Installing Azure Static Web Apps CLI...${NC}"
    npm install -g @azure/static-web-apps-cli
    echo -e "${GREEN}✅ SWA CLI installed${NC}"
    echo ""
fi

# Deploy
echo -e "${BLUE}🚀 Deploying to Azure...${NC}"
swa deploy ./dist \
  --deployment-token "$DEPLOYMENT_TOKEN" \
  --env production

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ DEPLOYMENT SUCCESSFUL!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}🌐 Your app is available at:${NC}"
echo -e "${GREEN}   https://$APP_URL${NC}"
echo ""
echo -e "${BLUE}📊 Next steps:${NC}"
echo "   1. Configure Django CORS: Add https://$APP_URL"
echo "   2. Update .env.production with backend URL"
echo "   3. Test the deployed app"
echo ""
echo -e "${BLUE}🔧 Management commands:${NC}"
echo "   View logs:    az staticwebapp logs show --name $APP_NAME --resource-group $RESOURCE_GROUP"
echo "   View details: az staticwebapp show --name $APP_NAME --resource-group $RESOURCE_GROUP"
echo "   Delete app:   az staticwebapp delete --name $APP_NAME --resource-group $RESOURCE_GROUP --yes"
echo ""
