#!/bin/sh
set -e

# If arguments are passed, run them directly instead of the default startup
if [ $# -gt 0 ]; then
  exec "$@"
fi

echo "Collecting static files..."
python manage.py collectstatic --settings=bidet_davao.settings.production --noinput 

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting server..."
exec gunicorn bidet_davao.wsgi:application --bind 0.0.0.0:8000