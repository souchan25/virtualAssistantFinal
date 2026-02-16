#!/bin/bash
# Deploy Django Backend to Azure App Service (Linux)
# With Supabase PostgreSQL Database

set -e  # Exit on error

echo "🚀 CPSU Health Assistant - Django Backend Deployment to Azure"
echo "=============================================================="
echo ""

# Configuration
RESOURCE_GROUP="cpsu-health-assistant-rg"
APP_NAME="cpsu-health-backend"
LOCATION="eastasia"
PLAN_NAME="cpsu-health-plan"
RUNTIME="PYTHON:3.11"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

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

# Create resource group if doesn't exist
echo -e "${BLUE}📦 Checking resource group...${NC}"
if ! az group show --name $RESOURCE_GROUP &> /dev/null; then
    az group create --name $RESOURCE_GROUP --location $LOCATION --output table
    echo -e "${GREEN}✅ Resource group created${NC}"
else
    echo -e "${GREEN}✅ Resource group exists${NC}"
fi
echo ""

# Create App Service Plan (FREE F1 or BASIC B1)
echo -e "${BLUE}📋 Creating App Service Plan...${NC}"
echo -e "${YELLOW}⚠️  Choose a SKU:${NC}"
echo "   1. FREE (F1) - $0/month (Limited, for testing)"
echo "   2. BASIC (B1) - Free with Student Subscription"
echo ""
read -p "Enter choice (1 or 2): " SKU_CHOICE

if [ "$SKU_CHOICE" == "1" ]; then
    SKU="FREE"
    SKU_SIZE="F1"
else
    SKU="BASIC"
    SKU_SIZE="B1"
fi

if ! az appservice plan show --name $PLAN_NAME --resource-group $RESOURCE_GROUP &> /dev/null; then
    az appservice plan create \
      --name $PLAN_NAME \
      --resource-group $RESOURCE_GROUP \
      --location $LOCATION \
      --sku $SKU_SIZE \
      --is-linux \
      --output table
    echo -e "${GREEN}✅ App Service Plan created ($SKU_SIZE)${NC}"
else
    echo -e "${GREEN}✅ App Service Plan exists${NC}"
fi
echo ""

# Create Web App
echo -e "${BLUE}🌐 Creating Web App...${NC}"
if ! az webapp show --name $APP_NAME --resource-group $RESOURCE_GROUP &> /dev/null; then
    az webapp create \
      --name $APP_NAME \
      --resource-group $RESOURCE_GROUP \
      --plan $PLAN_NAME \
      --runtime "$RUNTIME" \
      --output table
    echo -e "${GREEN}✅ Web App created${NC}"
else
    echo -e "${GREEN}✅ Web App exists${NC}"
fi
echo ""

# Get Web App URL
APP_URL=$(az webapp show \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query "defaultHostName" -o tsv)

echo -e "${GREEN}🌐 Your backend URL: https://$APP_URL${NC}"
echo ""

# Configure App Settings (Environment Variables)
echo -e "${BLUE}⚙️  Configuring environment variables...${NC}"
echo -e "${YELLOW}⚠️  You'll need to set these manually or provide them now:${NC}"
echo ""

read -p "Enter Supabase DB_HOST (e.g., db.xxxxx.supabase.co): " DB_HOST
read -p "Enter Supabase DB_USER (e.g., postgres.xxxxx): " DB_USER
read -sp "Enter Supabase DB_PASSWORD: " DB_PASSWORD
echo ""
read -p "Enter Django SECRET_KEY (or press Enter to generate): " SECRET_KEY

if [ -z "$SECRET_KEY" ]; then
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))")
    echo "Generated SECRET_KEY: $SECRET_KEY"
fi

echo ""
echo -e "${BLUE}Setting environment variables...${NC}"

az webapp config appsettings set \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings \
    DEBUG="False" \
    USE_POSTGRESQL="True" \
    DB_NAME="postgres" \
    DB_USER="$DB_USER" \
    DB_PASSWORD="$DB_PASSWORD" \
    DB_HOST="$DB_HOST" \
    DB_PORT="5432" \
    SECRET_KEY="$SECRET_KEY" \
    DJANGO_ALLOWED_HOSTS="$APP_URL" \
    CORS_ALLOWED_ORIGINS="https://delightful-forest-0eb2a9000.6.azurestaticapps.net" \
    WEBSITES_PORT="8000" \
    SCM_DO_BUILD_DURING_DEPLOYMENT="true" \
  --output table

echo -e "${GREEN}✅ Environment variables configured${NC}"
echo ""

# Configure startup command
echo -e "${BLUE}⚙️  Configuring startup command...${NC}"
az webapp config set \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --startup-file "startup.sh" \
  --output table

echo -e "${GREEN}✅ Startup command configured${NC}"
echo ""

# Deploy code from local directory
echo -e "${BLUE}📦 Deploying code...${NC}"
echo -e "${YELLOW}⚠️  This will deploy the current Django directory to Azure${NC}"
read -p "Continue? (y/n): " CONFIRM

if [ "$CONFIRM" == "y" ] || [ "$CONFIRM" == "Y" ]; then
    cd "$(dirname "$0")/.."  # Go to Django directory
    
    # Create deployment package (exclude unnecessary files)
    echo "Creating deployment package..."
    
    # Deploy using zip deployment
    az webapp up \
      --name $APP_NAME \
      --resource-group $RESOURCE_GROUP \
      --runtime "$RUNTIME" \
      --sku $SKU_SIZE \
      --location $LOCATION
    
    echo -e "${GREEN}✅ Code deployed${NC}"
else
    echo -e "${YELLOW}⏭️  Skipping code deployment${NC}"
    echo "Deploy manually with: az webapp up --name $APP_NAME --resource-group $RESOURCE_GROUP"
fi
echo ""

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ DEPLOYMENT COMPLETE!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}🌐 Backend URL:${NC}"
echo -e "${GREEN}   https://$APP_URL${NC}"
echo ""
echo -e "${BLUE}📊 Next steps:${NC}"
echo "   1. Copy ML folder to Azure (see guide)"
echo "   2. Run database migrations:"
echo "      az webapp ssh --name $APP_NAME --resource-group $RESOURCE_GROUP"
echo "      python manage.py migrate"
echo "   3. Create superuser:"
echo "      python manage.py createsuperuser"
echo "   4. Update Vue frontend API URL to: https://$APP_URL"
echo "   5. Test API: curl https://$APP_URL/api/"
echo ""
echo -e "${BLUE}🔧 Management commands:${NC}"
echo "   View logs:    az webapp log tail --name $APP_NAME --resource-group $RESOURCE_GROUP"
echo "   SSH access:   az webapp ssh --name $APP_NAME --resource-group $RESOURCE_GROUP"
echo "   Restart app:  az webapp restart --name $APP_NAME --resource-group $RESOURCE_GROUP"
echo "   Delete app:   az webapp delete --name $APP_NAME --resource-group $RESOURCE_GROUP --yes"
echo ""
