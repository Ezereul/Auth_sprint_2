FROM python:3.10-slim as base

WORKDIR /movies_api
ENV PATH /movies_api/.venv/bin/:$PATH
ENV PYTHONPATH /

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY poetry.lock pyproject.toml ./

RUN python -m pip install --no-cache-dir poetry==1.7.1 \
    && poetry config virtualenvs.in-project true \
    && poetry install --no-interaction --with=dev --no-ansi


FROM base AS prod

COPY --from=base /movies_api /movies_api
COPY src ./src
COPY  main.py .

ENTRYPOINT [ "gunicorn", "main:app", "--worker-class", "uvicorn.workers.UvicornWorker ", "--bind", "0.0.0.0:8000" ]

FROM base AS dev

COPY --from=base /movies_api /movies_api

ENTRYPOINT [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]


FROM base as tests

COPY --from=base /movies_api /movies_api
COPY tests tests
ENV PYTHONPATH /movies_api
RUN chmod 774 ./tests/functional/utils/tests_entrypoint.sh

ENTRYPOINT [ "./tests/functional/utils/tests_entrypoint.sh" ]
