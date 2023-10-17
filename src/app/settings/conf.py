import os
from pathlib import Path
from typing import Any, Dict, List, Tuple

import environ
from django.utils.translation import gettext_lazy as _

from app.consts.i18n import Language

# Build paths from src directory
BASE_DIR: Path = Path(__file__).resolve()
for x in range(10):
    BASE_DIR = BASE_DIR.parent
    if BASE_DIR.name == "src":
        break
else:
    raise AssertionError("Project not build from src directory")

ROOT_DIR: Path = BASE_DIR.parent

env: environ.Env = environ.Env()


# Security
ON_PRODUCTION = env.bool("DJANGO_ON_PRODUCTION", default=False)
SECRET_KEY: str = env("DJANGO_SECRET_KEY", default="django-insecure-foo-123")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])
DEBUG: bool = env("DJANGO_DEBUG", cast=bool, default=False)
USE_DEBUG_TOOLBAR = env("USE_DEBUG_TOOLBAR", cast=bool, default=False)
IS_TESTING = env("IS_TESTING", cast=bool, default=False)


SECURE_SSL_REDIRECT = env("SECURE_SSL_REDIRECT", bool, default=False)
CSRF_COOKIE_SECURE = env("CSRF_COOKIE_SECURE", bool, default=False)
SECURE_HSTS_SECONDS = env("SECURE_HSTS_SECONDS", int, default=0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env("SECURE_HSTS_INCLUDE_SUBDOMAINS", bool, default=False)
SECURE_HSTS_PRELOAD = env("SECURE_HSTS_PRELOAD", bool, default=False)
SESSION_COOKIE_SECURE = env("SESSION_COOKIE_SECURE", bool, default=False)

# Security - CSRF
CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS", default=["http://*.com", "https://*.ngrok.io"]
)

# Password Validation
AUTH_PASSWORD_VALIDATORS: List[Dict[str, str]] = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
AUTH_USER_MODEL = "users.User"


# Application definition
INSTALLED_APPS = [
    "django_extensions",
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework.authtoken",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "corsheaders",
    "app.apps.RootAppConfig",
    "users.apps.UsersConfig",
    "push_notifications.apps.PushNotificationsConfig",
]


ADMIN_URL_PREFIX = "a"
LOGIN_URL = f"/{ADMIN_URL_PREFIX}/login/"
LOGIN_REDIRECT_URL: str = f"/{ADMIN_URL_PREFIX}/"

MIDDLEWARE: List[str] = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "app.middlewares.i18n.TimezoneMiddleware",
    "app.middlewares.i18n.LanguageMiddleware",
    "app.middlewares.log.LogContextMiddleware",
]
ROOT_URLCONF: str = "app.urls"
TEMPLATES: List[Dict[str, Any]] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "app", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION: str = "app.wsgi.application"
ASGI_APPLICATION: str = "app.asgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": env("SQL_ENGINE", default="django.db.backends.postgresql"),
        "NAME": env("SQL_DATABASE", default="app"),
        "USER": env("SQL_USER", default="postgres"),
        "PASSWORD": env("SQL_PASSWORD", default="postgres"),
        "HOST": env("SQL_HOST", default="localhost"),
        "PORT": env("SQL_PORT", default="5432"),
    }
}

# Internationalization
LANGUAGE_CODE = Language.PT_BR
LANGUAGES = Language.choices
LOCALE_PATHS = [
    ROOT_DIR / "locale",
]
USE_I18N: bool = True

# Internationalization
# Dates
FORMAT_MODULE_PATH: List[str] = [
    "app.settings.formats",
]


# Time Zone
TIME_ZONE: str = "UTC"
USE_TZ: bool = True

# Static Files
STATIC_URL: str = "/static/"
STATIC_ROOT: str = os.path.join(ROOT_DIR, env("STATIC_ROOT", default="storage/static"))
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, direc) for direc in env.list("STATICFILES_DIRS", default=[])
]
STATICFILES_FINDERS: List[str] = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Media files
MEDIA_ROOT = os.path.join(ROOT_DIR, env("MEDIA_ROOT", default="storage/media/"))
MEDIA_URL = "/media/"

# Storages
DEFAULT_FILE_STORAGE_BACKEND = env(
    "DEFAULT_FILE_STORAGE", default="django.core.files.storage.FileSystemStorage"
)
STATICFILES_STORAGE_BACKEND = env(
    "STATICFILES_STORAGE_BACKEND", default="django.contrib.staticfiles.storage.StaticFilesStorage"
)
PUBLIC_MEDIA_STORAGE_BACKEND = env(
    "PUBLIC_MEDIA_STORAGE_BACKEND", default=DEFAULT_FILE_STORAGE_BACKEND
)
STORAGES = {
    "default": {"BACKEND": DEFAULT_FILE_STORAGE_BACKEND},
    "staticfiles": {"BACKEND": STATICFILES_STORAGE_BACKEND},
    "public_media": {"BACKEND": PUBLIC_MEDIA_STORAGE_BACKEND},
}
if DEFAULT_FILE_STORAGE_BACKEND == "app.storage.aws_s3.PrivateMediaStorage":
    INSTALLED_APPS.append("storages")
    from .third_party.aws_s3 import *


if DEBUG and USE_DEBUG_TOOLBAR:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
    ROOT_URLCONF = "app.urls_dev"
    from .third_party.dj_debug_toolbar import *

if IS_TESTING:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

from .external_services.geolocation import *
from .external_services.messaging import *
from .external_services.push_notification import *
from .external_services.sms import *
from .external_services.zipcode import *
from .infra.log import *
from .infra.reporting import *
from .third_party.celery import *
from .third_party.dj_cors_headers import *
from .third_party.drf import *
from .third_party.drf_simple_jwt import *
from .third_party.drf_spectacular import *
from .third_party.email import *
from .third_party.jazzmin import *
from .third_party.redis import *
