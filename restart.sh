#!/bin/bash
python manage.py collectstatic --noinput
python manage.py compress
systemctl restart uwsgi
systemctl restart nginx
