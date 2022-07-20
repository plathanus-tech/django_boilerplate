# Django Boilerplate

## Development environment

1.  PDM
    Install [PDM](https://pdm.fming.dev/latest/). PDM is a project development management tool. It's really similar to npm.
    Command:

    > pip install pdm==1.15.0

2.  Install python project dependencies:

    > pdm install

3.  Pre-Commit
    Install the [pre-commit](https://pre-commit.com/index.html) into your local git repository.

    > pdm run pre-commit install

4.  Setting up Environment Variables
    Now let's configure the environment variables.

    HOST -> This will define where the project will be reachable when you build in the next step. If you leave the default, `dev.boilerplate.com` then all you need to do is add it to `/etc/hosts` like:
    `127.0.0.1 dev.boilerplate.com`

5.  Docker
    Make sure you have [docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/) installed into your machine. It's used to build and run the project.
    So to build the project you can:

    > docker-compose build

    or, use the shortcut using _Make_ that comes installed on Ubuntu:

    > make build

    After that you can get the project running using:

    > docker-compose up

    or, use the shortcut using _Make_:

    > make up

    If you want you can also debug inside vscode.
    For that you're going to need the [Remote Explorer](https://github.com/Microsoft/vscode-remote-release) extension. After installing the extension run:

    > make debug

    This will get the project running on debug configurations. After, connect to the running api container with Remote Explorer, and from there you can run the Debug mode.

## Third Party Apps

### Django Apps

These are the Django libs built-in

[Django](https://docs.djangoproject.com/en/3.2/)

[DRF - Django Rest Framework](https://www.django-rest-framework.org/)

[DRF Spectacular - OpenAPI 3.0 Generator](https://drf-spectacular.readthedocs.io/en/latest/index.html)

[Django Environ - Environment Variables utility](https://django-environ.readthedocs.io/en/latest/)

[WhiteNoise - Static Files](https://whitenoise.evans.io/)

[Django CORS Headers](https://pypi.org/project/django-cors-headers/)

### Python Libs

These are the python libs:

[TOX - Automated Testing between environments and versions](https://tox.wiki/en/latest/index.html)

[Pytest - Unit Tests](https://docs.pytest.org/en/6.2.x/contents.html)

[Pytest-Django - Pytest Extension](https://pytest-django.readthedocs.io/en/latest/)

[Pytest-Mock - Mocking for Pytest](https://pypi.org/project/pytest-mock/)

[Celery - Distributed Queue](https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html#django-first-steps)

[Coverage - Test Coverage Report](https://coverage.readthedocs.io/en/6.2/)

# Internationalization commands:

Switch to src directory

> cd src/

Generate messages:

> pdm run django-admin makemessages -l pt_BR --settings app.settings.common

Compile messages:

> pdm run django-admin compilemessages
