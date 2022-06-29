#!/bin/sh

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic

gunicorn --timeout 60 --workers 4 inventorymanagementsystem.wsgi:application --bind 0.0.0.0:8000


