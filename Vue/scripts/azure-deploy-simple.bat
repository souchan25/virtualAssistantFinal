@echo off
REM Simple Azure Static Web Apps Deployment for Windows (No GitHub Integration)

setlocal enabledelayedexpansion

echo ========================================================
echo CPSU Health Assistant - Azure Static Web Apps Deployment
echo ========================================================
echo.

REM Configuration
set RESOURCE_GROUP=cpsu-health-assistant-rg
set APP_NAME=cpsu-health-assistant
set LOCATION=eastasia

REM Check if Azure CLI is installed
where az >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Azure CLI not found
    echo Install from: https://aka.ms/installazurecliwindows
    exit /b 1
)

REM Check if logged in
echo [INFO] Checking Azure authentication...
az account show >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Not logged in to Azure
    echo Run: az login
    exit /b 1
)
echo [OK] Azure authentication successful
echo.

REM Create resource group
echo [INFO] Checking resource group...
az group show --name %RESOURCE_GROUP% >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Creating resource group: %RESOURCE_GROUP%
    az group create --name %RESOURCE_GROUP% --location %LOCATION% --output table
    echo [OK] Resource group created
) else (
    echo [OK] Resource group exists
)
echo.

REM Create Static Web App
echo [INFO] Creating Azure Static Web App...
az staticwebapp show --name %APP_NAME% --resource-group %RESOURCE_GROUP% >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    az staticwebapp create ^
      --name %APP_NAME% ^
      --resource-group %RESOURCE_GROUP% ^
      --location %LOCATION% ^
      --sku Free ^
      --output table
    echo [OK] Static Web App created
) else (
    echo [OK] Static Web App exists
)
echo.

REM Get deployment token
echo [INFO] Getting deployment token...
for /f "delims=" %%i in ('az staticwebapp secrets list --name %APP_NAME% --resource-group %RESOURCE_GROUP% --query "properties.apiKey" -o tsv') do set DEPLOYMENT_TOKEN=%%i

if "%DEPLOYMENT_TOKEN%"=="" (
    echo [ERROR] Failed to get deployment token
    exit /b 1
)
echo [OK] Deployment token retrieved
echo.

REM Get app URL
for /f "delims=" %%i in ('az staticwebapp show --name %APP_NAME% --resource-group %RESOURCE_GROUP% --query "defaultHostname" -o tsv') do set APP_URL=%%i

REM Navigate to Vue directory
cd /d %~dp0..

REM Install dependencies
echo [INFO] Installing dependencies...
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] npm install failed
    exit /b 1
)
echo [OK] Dependencies installed
echo.

REM Build Vue app
echo [INFO] Building Vue app...
call npm run build
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Build failed
    exit /b 1
)
echo [OK] Build complete
echo.

REM Check if SWA CLI is installed
where swa >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [INFO] Installing Azure Static Web Apps CLI...
    call npm install -g @azure/static-web-apps-cli
    echo [OK] SWA CLI installed
    echo.
)

REM Deploy
echo [INFO] Deploying to Azure...
call swa deploy ./dist ^
  --deployment-token "%DEPLOYMENT_TOKEN%" ^
  --env production

echo.
echo ========================================
echo [SUCCESS] DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo Your app is available at:
echo    https://%APP_URL%
echo.
echo Next steps:
echo    1. Configure Django CORS: Add https://%APP_URL%
echo    2. Update .env.production with backend URL
echo    3. Test the deployed app
echo.
pause
