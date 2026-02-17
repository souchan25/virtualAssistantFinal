#!/bin/bash
echo "=========================================="
echo "Starting CPSU Health Backend"
echo "=========================================="

cd /home/site/wwwroot

echo "Current directory: $(pwd)"
echo "Contents:"
ls -la

echo "Installing dependencies..."
pip install -r requirements.txt --quiet

echo "Running collectstatic..."
python manage.py collectstatic --noinput 2>/dev/null || true

echo "Running migrations..."
python manage.py migrate --noinput 2>/dev/null || true

echo "Starting Gunicorn..."
gunicorn health_assistant.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --timeout 300 \
    --access-logfile '-' \
    --error-logfile '-' \
    --log-level info \
    --chdir /home/site/wwwroot
