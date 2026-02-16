#!/bin/bash
set -x

echo "=========================================="
echo "Starting CPSU Health Backend"
echo "=========================================="

# Azure extracts files to different locations, find the right one
if [ -f "/home/site/wwwroot/manage.py" ]; then
    APP_DIR="/home/site/wwwroot"
elif [ -f "manage.py" ]; then
    APP_DIR="."
else
    # Files might be in parent directory
    APP_DIR="/home/site/wwwroot"
fi

echo "App directory: $APP_DIR"
cd $APP_DIR || exit 1

# Verify we're in the right place
if [ ! -f "manage.py" ]; then
    echo "ERROR: manage.py not found!"
    echo "Current directory: $(pwd)"
    echo "Files in current directory:"
    ls -la
    exit 1
fi

# Use WEBSITES_PORT which is Azure's standard
PORT="${WEBSITES_PORT:-8000}"
export PORT

echo "Port: $PORT"
echo "Python version: $(python --version)"
echo "Django check:"
python manage.py check || echo "Django check failed but continuing..."

echo "Collecting static files..."
python manage.py collectstatic --noinput 2>&1 || echo "Static collection skipped"

echo "Running migrations..."
python manage.py migrate --noinput 2>&1 || echo "Migrations skipped"

echo "Starting Gunicorn on 0.0.0.0:$PORT..."
exec gunicorn health_assistant.wsgi:application \
  --bind=0.0.0.0:$PORT \
  --workers=2 \
  --timeout=300 \
  --access-logfile '-' \
  --error-logfile '-' \
  --log-level info \
  --capture-output
