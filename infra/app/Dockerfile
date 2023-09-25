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
RUN pdm install --prod --no-lock --no-editable

WORKDIR /app

ENV PYTHONPATH=/app/src:/pkgs/.venv/lib/python3.11/site-packages
COPY src /app/src
COPY locale /app/locale
COPY manage.py gunicorn.conf.py /app/
RUN python manage.py collectstatic --noinput
RUN python manage.py compilemessages
