#!/bin/bash
./manage.py migrate
./manage.py collectstatic --noinput
gunicorn -b 0.0.0.0:8000 --workers=4 punkweb.wsgi
