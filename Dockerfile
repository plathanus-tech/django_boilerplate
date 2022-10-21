FROM python:3.9.13

WORKDIR /pkgs

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update -y
RUN apt install -y gettext

RUN pip install pip setuptools wheel
RUN pip install pdm==2.1.0

# Install dev deps
COPY pyproject.toml pdm.lock /pkgs/
RUN pdm install

WORKDIR /app
COPY entrypoint.api.sh entrypoint.api.sh
RUN sed -i 's/\r$//g' entrypoint.api.sh
RUN chmod +x  entrypoint.api.sh

ENV PYTHONPATH=src:/pkgs/.venv/lib/python3.9/site-packages
COPY ./ /app

ENTRYPOINT [ "sh", "/app/entrypoint.api.sh" ]
