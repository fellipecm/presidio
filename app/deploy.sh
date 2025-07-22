#!/bin/bash

# Simple deployment script using Azure Functions Core Tools
echo "🚀 Deploying with Azure Functions Core Tools..."

RESOURCE_GROUP_NAME=${1:-"personal"}
FUNCTION_APP_NAME=${2:-"presidio-func"}

# Check if func command is available
if ! command -v func &> /dev/null; then
    echo "❌ Azure Functions Core Tools not installed."
    echo "📦 Install with: npm install -g azure-functions-core-tools@4 --unsafe-perm true"
    exit 1
fi

# Check local Python version
PYTHON_VERSION=$(python --version 2>&1 | grep -oP '\d+\.\d+')
echo "🐍 Local Python version detected: $PYTHON_VERSION"

if [[ "$PYTHON_VERSION" != "3.13" ]]; then
    echo "⚠️ Warning: Local Python version is $PYTHON_VERSION, but we'll configure Azure for 3.13"
    echo "💡 Consider using pyenv or conda to switch to Python 3.13 for better compatibility"
fi

# Check if logged in to Azure
az account show > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Not logged in to Azure. Please run 'az login' first."
    exit 1
fi

# Navigate to function app directory
cd function_app

# Configure essential app settings before deployment
echo "⚙️ Configuring function app settings..."

# Configure app settings
az functionapp config appsettings set \
    --resource-group $RESOURCE_GROUP_NAME \
    --name $FUNCTION_APP_NAME \
    --settings FUNCTIONS_WORKER_RUNTIME=python \
                WEBSITE_RUN_FROM_PACKAGE=1 \
                SCM_DO_BUILD_DURING_DEPLOYMENT=true \
                PYTHON_VERSION=3.12

# Deploy directly
echo "📦 Deploying function app..."
func azure functionapp publish $FUNCTION_APP_NAME --python

if [ $? -eq 0 ]; then
    echo "✅ Deployment completed successfully!"
    
    # # Run post-deployment commands
    # echo "📦 Running post-deployment setup..."
    # echo "🔧 Installing spaCy English model..."
    # az functionapp deployment source config-local-git \
    #     --resource-group $RESOURCE_GROUP_NAME \
    #     --name $FUNCTION_APP_NAME \
    #     --query url -o tsv > /dev/null 2>&1 || true
    
    # # Use Azure CLI to run the spaCy download command
    # az functionapp ssh \
    #     --resource-group $RESOURCE_GROUP_NAME \
    #     --name $FUNCTION_APP_NAME \
    #     --command "python -m spacy download en_core_web_sm" 2>/dev/null || \
    # echo "⚠️ Could not run post-deployment command via SSH. Model will be downloaded on first run."
    
    # Wait a moment for functions to initialize
    echo "⏳ Waiting for functions to initialize..."
    sleep 10
    
    # Get function app URL
    FUNCTION_URL=$(az functionapp show --resource-group $RESOURCE_GROUP_NAME --name $FUNCTION_APP_NAME --query "defaultHostName" -o tsv)
    echo "🌐 Function App URL: https://$FUNCTION_URL"
    
    # Test the functions
    echo ""
    echo "🧪 Testing endpoints:"
    echo "  Health Check: https://$FUNCTION_URL/api/health"
    echo "  Hello World: https://$FUNCTION_URL/api/hello"
    echo "  Diagnostics: https://$FUNCTION_URL/api/diagnostics"
    
    # Test health endpoint
    echo ""
    echo "📡 Testing health endpoint..."
    curl -s "https://$FUNCTION_URL/api/health" | jq '.' || echo "❌ Health check failed"
    
else
    echo "❌ Deployment failed!"
    exit 1
fi

echo "🎉 Deployment completed!"
