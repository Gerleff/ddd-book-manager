FROM python:3.10-slim-bullseye
WORKDIR /app/
COPY ./poetry.lock /app/
COPY ./pyproject.toml /app

ENV PYTHONPATH=${PYTHONPATH}:/app/src:/app
ENV ALEMBIC_CONFIG=/app/src/infrastructure/connector/sqla/alembic/alembic.ini
ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.2.1

RUN pip install "poetry==$POETRY_VERSION"
COPY ./ /app/
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

RUN groupadd --gid 1001 app && \
    useradd -u 1001 -g app app && \
    chown -R 1001:1001  /app

USER 1001
