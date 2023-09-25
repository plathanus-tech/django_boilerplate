# Django Boilerplate

## Installing / Running

All steps mentioned above are based on Ubuntu 20.04.
It may not work on MacOs or Windows.

0.  _Python_

    This project requires python3.11 to run. To install it follow these guidelines:

    > sudo apt update && sudo apt upgrade -y

    > sudo apt install software-properties-common -y

    > sudo add-apt-repository ppa:deadsnakes/ppa

    > sudo apt install python3.11

    > sudo apt install python3-pip python3.11-distutils python3-apt --reinstall

    > python3.11 -m pip install --upgrade pip

    > python3.11 -m pip install setuptools wheel

    These steps work from any version of python3.
    Just swap the minor version to the desired version.

1.  _PDM_

    Install [PDM](https://pdm.fming.dev/latest/). PDM is a project development management tool. It's really similar to npm.
    Command:

    > pip install pdm

2.  Setup your local environment for development:

    > pdm use

    Select the python3.9 interpreter

    After that, create a virtual environment for this interpreter

    > pdm venv create

    > pdm use

    Select the interpreter for the virtual environment you just created

    > pdm install

    Setup on vscode the virtual environment of the interpreter (bottom-right corner)

    Install the [pre-commit](https://pre-commit.com/index.html) into your local git repository.

    > pdm run pre-commit install

2.1. Setting up Environment Variables

    Now let's configure the environment variables. First of all copy the `.env_files/.env.example` to the root of your project with the name `.env`. The following command should do the job:

    > cp .env_files/.env.example .env

    Now inside `.env` are defined your project environment variables, tweak, change them to whatever value you want.

    Some important variables:

    - DJANGO_SECRET_KEY: For development this can be any value, changing this value after having users registered will break their passwords.
    - DJANGO_DEBUG: When set to True (1) will display Tracebacks and will add a debug toolbar in the site.
    - SQL_HOST: Leaving this value to `localhost` allows you to externally access the database while the docker-compose services are running.

3.  Docker

    Make sure you have [docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/) installed into your machine. It's used to build and run the project.
    So to build the project you can:

    > docker compose --env-file .env -f local.yml build

    After that you can get the project running using:

    > docker compose --env-file .env -f local.yml up

    To create a user to access the admin panel, run:

    > pdm run createsuperuser

    or, if you don't have pdm on your machine:

    > docker compose --env-file .env -f local.yml exec app python manage.py createsuperuser

After all these steps, you will end up with the following components running in your machine:

- Django App: Available at the `HOST` variable set in the .env.
- PostgreSQL Server: Available at the `SQL_HOST` variable. You can then use PGAdmin4 or DBeaver to connect.
- Celery Worker: A single thread worker that will execute tasks sent to celery.
- Celery Scheduler: Produces messages (tasks) periodically to workers consume.
- Redis: In-Memory database that is used as a broker for celery.

## Going Live:

For production environments you most likely will be using a AWS EC2 instance for a MVP product. The project is configured so you just need to git clone it in the virtual machine, setup the `.env` file, build the `production.yml` file and run the `up` command.
For production we don't use some of the docker services that are present on development, they are:

- db:
  You will need to setup a AWS RDS instance for the PostgreSQL Database, then set the proper environment variables in the .env file: `SQL_ENGINE`, `SQL_DATABASE`, `SQL_USER`, `SQL_PASSWORD`, `SQL_HOST`, `SQL_PORT`.
- media storage:
  On development we store media on the local machine, but in production you should setup a S3 Bucket to receive the images. Then, you must configure the following environment variables: `AWS_ACCESS_KEY_ID`,`AWS_SECRET_ACCESS_KEY`,`AWS_STORAGE_BUCKET_NAME`.
- sms:
  By default, the boilerplate will use the twilio Api to send SMS's. If you wish to use it, set the `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_SERVICE_PHONE` variables.

### Django Apps

These are the Django related libs used in this project:

- [Django](https://docs.djangoproject.com/en/4.0/)
- [Jazzmin - Admin](https://github.com/farridav/django-jazzmin)
- [DRF - Django Rest Framework](https://www.django-rest-framework.org/)
- [Django - Channels](https://github.com/django/channels)
- [Daphne ASGI Server](https://github.com/django/daphne)
- [DRF Spectacular - OpenAPI 3.0 Generator](https://drf-spectacular.readthedocs.io/en/latest/index.html)
- [Django Environ - Environment Variables utility](https://django-environ.readthedocs.io/en/latest/)
- [Django CORS Headers](https://pypi.org/project/django-cors-headers/)

### Python Libs

These are the python libs:

[TOX - Automated Testing between environments and versions](https://tox.wiki/en/latest/index.html)

[Pytest - Unit Tests](https://docs.pytest.org/en/6.2.x/contents.html)

[Pytest-Django - Pytest Extension](https://pytest-django.readthedocs.io/en/latest/)

[Pytest-Mock - Mocking for Pytest](https://pypi.org/project/pytest-mock/)

[Celery - Distributed Queue](https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html#django-first-steps)

[Coverage - Test Coverage Report](https://coverage.readthedocs.io/en/6.2/)
