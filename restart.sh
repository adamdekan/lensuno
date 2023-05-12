#!/bin/bash
python manage.py collectstatic
python manage.py compress
systemctl restart uwsgi
systemctl restart nginx
