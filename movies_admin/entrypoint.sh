#!/usr/bin/env bash

export DJANGO_SUPERUSER_USERNAME=some_admin
export DJANGO_SUPERUSER_PASSWORD=123123
export DJANGO_SUPERUSER_EMAIL=mail@mail.ru

poetry run python manage.py migrate --noinput
poetry run python manage.py createsuperuser --noinput || true

poetry run pyuwsgi --strict --ini /opt/movies_admin/uwsgi.ini