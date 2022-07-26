# Django Boilerplate

## Installing / Running

All steps mentioned above are based on Ubuntu 20.04.
It may not work on MacOs or Windows.

0.  _Python_

    This project requires python3.10 to run. To install it follow these guidelines:

    > sudo apt update && sudo apt upgrade -y

    > sudo apt install software-properties-common -y

    > sudo add-apt-repository ppa:deadsnakes/ppa

    > sudo apt install python3.10

    > sudo apt install python3-pip python3.10-distutils python3-apt --reinstall

    > python3.10 -m pip install --upgrade pip

    > python3.10 -m pip install setuptools wheel

    These steps work from any version of python3.
    Just swap the minor version to the desired version.

1.  _PDM_

    Install [PDM](https://pdm.fming.dev/latest/). PDM is a project development management tool. It's really similar to npm.
    Command:

    > pip install pdm

2.  Install python project dependencies:

    > pdm install

3.  Pre-Commit

    Install the [pre-commit](https://pre-commit.com/index.html) into your local git repository.

    > pdm run pre-commit install

4.  Setting up Environment Variables

    Now let's configure the environment variables. First of all copy the `.env.dev.example` to the root of your project with the name `.env.dev`. The following command should do the job:

    > cp .env.dev.example .env.dev

    When deploying to production do the same for the `.env.prod.example`, copying it to the root with the name `.env.prod`.

    Now inside `.env.dev` are defined your project environment variables, tweak, change them to whatever value you want.

    Some important variables:

    - HOST: This will define where the project will be reachable when you build in the next step. If you leave the default, `dev.boilerplate.com` then all you need to do is add it to `/etc/hosts` like:
      `127.0.0.1 dev.boilerplate.com`
    - DJANGO_SECRET_KEY: For development this can be any value, changing this value after having users registered will break their passwords.
    - DJANGO_SETTINGS_MODULE: Where django will look for the settings. For production swap to `app.settings.prod`
    - DJANGO_DEBUG: When set to True (1) will display Tracebacks and will add a debug toolbar in the site.
    - SQL_HOST: Leaving this value to `localhost` allows you to externally access the database while the docker-compose services are running.

5.  Docker

    Make sure you have [docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/) installed into your machine. It's used to build and run the project.
    So to build the project you can:

    > docker-compose --env-file .env.dev build

    or, use the shortcut using _Make_ that comes installed on Ubuntu:

    > make build

    After that you can get the project running using:

    > docker-compose --env-file .env.dev up

    or, use the shortcut using _Make_:

    > make up

    If you want you can also debug inside vscode.
    For that you're going to need the [Remote Explorer](https://github.com/Microsoft/vscode-remote-release) extension. After installing the extension run:

    > make debug

    This will get the project running on debug configurations. After, connect to the running api container with Remote Explorer, and from there you can run the Debug mode.

After all these steps, you will end up with the following components running in your machine:

- Traefik: A Reverse-Proxy Server that will serve the services over Http(s)
- Django App: Available at the `HOST` variable set in the .env.dev.
- PostgreSQL Server: Available at the `SQL_HOST` variable. You can then use PGAdmin4 or DBeaver to connect.
- Celery Worker: A single thread worker that will execute tasks sent to celery.
- Celery Scheduler: Produces messages (tasks) periodically to workers consume.
- Redis: In-Memory database that is used as a broker for celery.

## Project Dependencies

### Django Apps

These are the Django related libs used in this project:

- [Django](https://docs.djangoproject.com/en/4.0/)
- [Jazzmin - Admin](https://github.com/farridav/django-jazzmin)
- [DRF - Django Rest Framework](https://www.django-rest-framework.org/)
- [Django - Channels](https://github.com/django/channels)
- [Daphne ASGI Server](https://github.com/django/daphne)
- [DRF Spectacular - OpenAPI 3.0 Generator](https://drf-spectacular.readthedocs.io/en/latest/index.html)
- [Django Environ - Environment Variables utility](https://django-environ.readthedocs.io/en/latest/)
- [WhiteNoise - Static Files](https://whitenoise.evans.io/)
- [Django CORS Headers](https://pypi.org/project/django-cors-headers/)

### Python Libs

These are the python libs:

[TOX - Automated Testing between environments and versions](https://tox.wiki/en/latest/index.html)

[Pytest - Unit Tests](https://docs.pytest.org/en/6.2.x/contents.html)

[Pytest-Django - Pytest Extension](https://pytest-django.readthedocs.io/en/latest/)

[Pytest-Mock - Mocking for Pytest](https://pypi.org/project/pytest-mock/)

[Celery - Distributed Queue](https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html#django-first-steps)

[Coverage - Test Coverage Report](https://coverage.readthedocs.io/en/6.2/)
