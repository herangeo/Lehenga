#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input
python manage.py migrate
if [[ $CREATE_SUPERUSER ]]; then
    python manage.py createsuperuser --no-input --email "$DJANGO_SUPERUSER_EMAIL" || echo "Superuser creation skipped or failed"
fi
