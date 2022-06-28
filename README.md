# Django Boilerplate

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
