#!/bin/sh
set -e

# If arguments are passed, run them directly instead of the default startup
if [ $# -gt 0 ]; then
  exec "$@"
fi

echo "Checking active AWS Identity..."
python -c "
import boto3
try:
    print('Assumed Identity:', boto3.client('sts').get_caller_identity()['Arn'])
except Exception as e:
    print('Failed to get AWS identity:', str(e))
"

echo "Collecting static files..."
python manage.py collectstatic --settings=bidet_davao.settings.production --noinput 

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting server..."
exec gunicorn bidet_davao.wsgi:application --bind 0.0.0.0:8000