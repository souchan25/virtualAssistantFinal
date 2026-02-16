#!/bin/bash
# Azure App Service deployment script

echo "=========================================="
echo "Azure Deployment Started"
echo "=========================================="

# Install Python dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Add gunicorn (production WSGI server)
pip install gunicorn

echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
