FROM python:3.12-slim

ARG NO_DEV="--only=main"
ENV POETRY_VIRTUALENVS_IN_PROJECT=true

WORKDIR /app

RUN pip install -U pip && pip install 'poetry==1.4.0'

COPY ./backend/poetry.lock ./backend/pyproject.toml ./

RUN poetry install --no-root --no-interaction --no-ansi $NO_DEV

ENV PATH /app/.venv/bin:$PATH

COPY ./backend/hermes ./hermses
COPY ./backend/migrations ./migrations
