FROM python:3.9

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update -y
RUN apt install -y netcat gettext

RUN pip install pip setuptools wheel
RUN pip install pdm==2.1.0

COPY pyproject.toml pdm.lock manage.py /app/
# Install dev deps
RUN pdm install --no-lock --no-editable

COPY entrypoint.api.sh entrypoint.api.sh
RUN sed -i 's/\r$//g' entrypoint.api.sh
RUN chmod +x  entrypoint.api.sh

ENV PYTHONPATH=src:.venv/lib/python3.9/site-packages
COPY ./ /app

ENTRYPOINT [ "sh", "/app/entrypoint.api.sh" ]
