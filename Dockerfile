FROM python:3.9

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV HOME=/project

RUN apt update -y
RUN apt install -y netcat
RUN apt install -y gettext

RUN pip install -U pip setuptools wheel
RUN pip install pdm

COPY pyproject.toml pdm.lock manage.py entrypoint.prod.sh ${HOME}/
COPY .vscode ${HOME}/.vscode

WORKDIR ${HOME}
RUN pdm install

WORKDIR /usr/src/app
COPY src/ ${HOME}

WORKDIR ${HOME}
RUN sed -i 's/\r$//g'  entrypoint.prod.sh
RUN chmod +x  entrypoint.prod.sh


ENV PYTHONPATH=__pypackages__/3.9/lib

ENTRYPOINT ["/project/entrypoint.prod.sh"]