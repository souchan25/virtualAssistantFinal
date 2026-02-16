#!/bin/bash
# Azure Static Web Apps Deployment with GitHub Integration
# Requires GitHub Personal Access Token (PAT)

set -e  # Exit on error

echo "🚀 CPSU Health Assistant - Azure Static Web Apps Deployment (GitHub)"
echo "======================================================================"
echo ""

# Configuration
RESOURCE_GROUP="cpsu-health-assistant-rg"
APP_NAME="cpsu-health-assistant"
LOCATION="eastasia"
GITHUB_REPO="https://github.com/souchan25/virtualAssistantFinal"
BRANCH="main"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check for GitHub token
if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${RED}❌ GITHUB_TOKEN environment variable not set${NC}"
    echo ""
    echo -e "${YELLOW}To create a GitHub Personal Access Token:${NC}"
    echo "1. Go to: https://github.com/settings/tokens/new"
    echo "2. Note: 'Azure Static Web Apps - CPSU Health Assistant'"
    echo "3. Expiration: 90 days"
    echo "4. Scopes: repo, workflow, write:packages, read:org"
    echo "5. Generate token and copy it"
    echo ""
    echo -e "${BLUE}Then run:${NC}"
    echo "export GITHUB_TOKEN=ghp_your_token_here"
    echo "./scripts/azure-deploy-github.sh"
    echo ""
    exit 1
fi

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo -e "${RED}❌ Azure CLI not found${NC}"
    exit 1
fi

# Check if logged in
echo -e "${BLUE}🔐 Checking Azure authentication...${NC}"
if ! az account show &> /dev/null; then
    echo -e "${RED}❌ Not logged in. Run: az login${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Azure authentication OK${NC}"
echo ""

# Create resource group
echo -e "${BLUE}📦 Checking resource group...${NC}"
if ! az group show --name $RESOURCE_GROUP &> /dev/null; then
    az group create --name $RESOURCE_GROUP --location $LOCATION --output table
    echo -e "${GREEN}✅ Resource group created${NC}"
else
    echo -e "${GREEN}✅ Resource group exists${NC}"
fi
echo ""

# Create Static Web App with GitHub integration
echo -e "${BLUE}🌐 Creating Static Web App with GitHub integration...${NC}"
az staticwebapp create \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --source $GITHUB_REPO \
  --location $LOCATION \
  --branch $BRANCH \
  --app-location "/Vue" \
  --output-location "dist" \
  --token $GITHUB_TOKEN \
  --output table

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Static Web App created with GitHub Actions${NC}"
    echo ""
    
    # Get app URL
    APP_URL=$(az staticwebapp show \
      --name $APP_NAME \
      --resource-group $RESOURCE_GROUP \
      --query "defaultHostname" -o tsv)
    
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}✅ DEPLOYMENT CONFIGURED!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "${BLUE}🌐 Your app will be available at:${NC}"
    echo -e "${GREEN}   https://$APP_URL${NC}"
    echo ""
    echo -e "${BLUE}📊 Next steps:${NC}"
    echo "   1. GitHub Actions workflow created in .github/workflows/"
    echo "   2. Push to main branch triggers automatic deployment"
    echo "   3. Check deployment status: https://github.com/souchan25/virtualAssistantFinal/actions"
    echo "   4. Configure Django CORS with: https://$APP_URL"
    echo ""
else
    echo -e "${RED}❌ Deployment failed. Check GitHub token permissions.${NC}"
    exit 1
fi
