FROM python:3.11-slim-buster

WORKDIR /pkgs

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update -y
RUN apt install -y gettext

RUN pip install pip setuptools wheel
RUN pip install pdm==2.7.4

# Install dev deps
COPY pyproject.toml pdm.lock /pkgs/
RUN pdm install -G :all

WORKDIR /app
COPY infra/app/entrypoint.api.sh /app/entrypoint.api.sh
RUN sed -i 's/\r$//g' /app/entrypoint.api.sh
RUN chmod +x  /app/entrypoint.api.sh

ENV PYTHONPATH=/app/src:/pkgs/.venv/lib/python3.11/site-packages
COPY src /app/src
COPY locale /app/locale
COPY manage.py gunicorn.conf.py /app/

ENTRYPOINT [ "sh", "/app/entrypoint.api.sh" ]
