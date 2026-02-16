#!/bin/bash
set -x

echo "=========================================="
echo "Starting CPSU Health Backend"
echo "=========================================="

cd /home/site/wwwroot || exit 1

# Use WEBSITES_PORT which is Azure's standard
PORT="${WEBSITES_PORT:-8000}"
export PORT

echo "Port: $PORT"
echo "Python version: $(python --version)"
echo "Django check:"
python manage.py check || echo "Django check failed"

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
  --log-level debug \
  --capture-output
