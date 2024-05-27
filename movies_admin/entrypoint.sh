#!/usr/bin/env bash

set -e

chown www-data:www-data /var/log
python manage.py migrate
python manage.py initsuperuser
python manage.py collectstatic --noinput --clear --no-post-process
uwsgi --strict --ini /opt/app/uwsgi/uwsgi.ini --py-autoreload 1
