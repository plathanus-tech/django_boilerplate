FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update -y
RUN apt install -y netcat

# install PDM
RUN pip install -U pip setuptools wheel
RUN pip install pdm

# copy files
COPY . /project/

WORKDIR /project
RUN sed -i 's/\r$//g' /project/entrypoint.prod.sh
RUN chmod +x /project/entrypoint.prod.sh

# install dependencies and project
RUN pdm install --no-lock --no-editable

# retrieve packages from build stage
ENV PYTHONPATH=/project/__pypackages__/3.9/lib

WORKDIR /project
ENTRYPOINT ["/project/entrypoint.prod.sh"]
