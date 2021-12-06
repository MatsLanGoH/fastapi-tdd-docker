FROM python:3.9.9-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.1.11

RUN pip install -U pip \
    && apt-get update \
    && apt-get -y install netcat gcc curl \
    && apt-get clean \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="${PATH}:/root/.poetry/bin"

RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /usr/src/app
COPY poetry.lock pyproject.toml /usr/src/app/

# Project initialization
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Creating folders and files for project
COPY .. /code
