FROM python:3.12-slim

WORKDIR /auth
ENV PATH /auth/.venv/bin:$PATH
ENV PYTHONPATH /:$PYTHONPATH

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY poetry.lock pyproject.toml ./

RUN python -m pip install --no-cache-dir poetry==1.7.1 \
    && poetry config virtualenvs.in-project true \
    && poetry install --no-interaction --no-ansi

# list of copied configured via .dockerignore
COPY . .

ENTRYPOINT ["bash", "/auth/docker-entrypoint.sh"]
