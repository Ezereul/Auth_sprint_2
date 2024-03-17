#!/usr/bin/env bash

poetry run python manage.py migrate --noinput
poetry run pyuwsgi --strict --ini /opt/movies_admin/uwsgi/uwsgi.ini
