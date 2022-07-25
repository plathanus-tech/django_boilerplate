FROM python:3.9

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update -y
RUN apt install -y netcat gettext

RUN pip install pip setuptools wheel
RUN pip install pdm==1.15.5

COPY pyproject.toml pdm.lock manage.py entrypoint.api.sh /app/
# Install dev deps
RUN pdm install

COPY entrypoint.api.sh entrypoint.api.sh
RUN sed -i 's/\r$//g' entrypoint.api.sh
RUN chmod +x  entrypoint.api.sh

ENV PYTHONPATH=src:__pypackages__/3.9/lib
COPY ./ /app

ENTRYPOINT [ "sh", "/app/entrypoint.api.sh" ]
