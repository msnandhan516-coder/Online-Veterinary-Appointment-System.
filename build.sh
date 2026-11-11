#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

# Install production dependencies
pip install -r requirements.txt

# Collect static assets
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate

# Load existing data (runs once, safe to repeat)
if [ -f data.json ]; then
  python manage.py loaddata data.json
  echo "Data loaded successfully"
fi
