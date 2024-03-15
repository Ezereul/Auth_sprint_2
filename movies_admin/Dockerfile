FROM python:3.12-slim

WORKDIR /opt/movies_admin

RUN groupadd -r django && useradd -d /opt/movies_admin -r -g django django

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 8
ENV UWSGI_HARAKIRI 240
ENV DJANGO_SETTINGS_MODULE 'config.settings'
ENV PATH /opt/movies_admin/.venv/bin/:$PATH

COPY --chown=django:django poetry.lock pyproject.toml ./

RUN mkdir static \
    && mkdir media \
    && pip install --no-cache-dir poetry==1.7.1 \
    && poetry config virtualenvs.in-project true \
    && poetry install --no-interaction --no-ansi

COPY --chown=django:django . .

RUN poetry run python manage.py collectstatic --noinput

EXPOSE 8000

USER django

ENTRYPOINT ["sh", "entrypoint.sh"]
