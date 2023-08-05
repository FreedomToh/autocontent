#!/bin/bash

# Apply database migrations
#echo "Init database migrations"
python3 manage.py makemigrations

## Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Run uWSGI
echo "Running uWSGI"
uwsgi --ini /api/uwsgi.ini