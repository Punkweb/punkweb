#!/bin/bash
./manage.py migrate
./manage.py collectstatic --noinput
sudo -u www-data gunicorn -b 0.0.0.0:8000 --workers=4 punkweb.wsgi
