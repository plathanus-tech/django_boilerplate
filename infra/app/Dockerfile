FROM python:3.11-slim-buster

WORKDIR /pkgs

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update -y
RUN apt install -y gettext

RUN pip install pip setuptools wheel
RUN pip install pdm==2.7.4

COPY pyproject.toml pdm.lock /pkgs/
ARG PDM_INSTALL_ARGS=""
RUN pdm install ${PDM_INSTALL_ARGS}

WORKDIR /app

ENV PYTHONPATH=/app/src:/pkgs/.venv/lib/python3.11/site-packages
COPY src /app/src
COPY locale /app/locale
COPY manage.py gunicorn.conf.py infra/app/before_migrate.sh /app/
