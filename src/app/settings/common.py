# type: ignore

import os
from datetime import timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

import environ
from django.utils.translation import gettext_lazy as _


# Build paths from src directory
BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
ROOT_DIR: Path = BASE_DIR.parent

env: environ.Env = environ.Env()


# Security
SECRET_KEY: str = env("DJANGO_SECRET_KEY")
DEBUG: bool = env("DJANGO_DEBUG", cast=bool, default=False)
ALLOWED_HOSTS: List[str] = env.list("DJANGO_ALLOWED_HOSTS", default=[])
CORS_ORIGIN_ALLOW_ALL: bool = env(
    "DJANGO_CORS_ORIGIN_ALLOW_ALL", cast=bool, default=False
)
if not CORS_ORIGIN_ALLOW_ALL:
    CORS_ORIGIN_WHITELIST: List[str] = env.list(
        "DJANGO_CORS_ORIGIN_WHITELIST", default=[]
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
DJANGO_APPS: List[str] = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
THIRD_PARTY_APPS: List[str] = [
    "rest_framework",
    "rest_framework.authtoken",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "corsheaders",
]
YOUR_PROJECT_APPS: List[str] = [
    "users.apps.UsersConfig",
]
LOGIN_REDIRECT_URL: str = "/admin/"

MIDDLEWARE: List[str] = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
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


# Database
DATABASES: Dict[str, str] = {
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
LANGUAGE_CODE: str = "en-us"
LANGUAGES: List[Tuple[str, str]] = [
    ("pt-br", _("Brazilian Portuguese")),
    ("en", _("English")),
]
LOCALE_PATHS: List[str] = [
    os.path.join(BASE_DIR, "app", "locale"),
]
USE_I18N: bool = True

# Internationalization
# Dates
USE_L10N: bool = True
FORMAT_MODULE_PATH: List[str] = [
    "app.settings.formats",
]


# Time Zone
TIME_ZONE: str = "UTC"
USE_TZ: bool = True


# Static Files
STATIC_URL: str = "/static/"
STATIC_ROOT: str = os.path.join(ROOT_DIR, "static")
STATICFILES_DIRS: List[str] = []
STATICFILES_FINDERS: List[str] = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
STATICFILES_STORAGE: str = "whitenoise.storage.CompressedStaticFilesStorage"


# Logging
LOGGING_LEVEL: str = env("DJANGO_LOGGING_LEVEL", default="INFO")
LOGGING: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
        "file": {
            "level": LOGGING_LEVEL,
            "class": "logging.FileHandler",
            "filename": "django.log",
        },
    },
    "formatters": {
        "verbose": {
            "format": "{levelname} {module} {asctime}: {message}",
            "style": "{",
        },
        "simple": {"format": "{levelname} {asctime}: {message}", "style": "{"},
    },
    "root": {"handlers": ["console"], "level": LOGGING_LEVEL},
}


JAZZMIN_SETTINGS = {
    "site_logo_classes": "img-circle",
    "site_icon": None,
    "welcome_sign": _("Welcome to the admin!"),
    "user_avatar": None,
    "show_sidebar": True,
    "navigation_expanded": True,
    # https://fontawesome.com/v5/search?m=free
    "icons": {
        "users": "fas fa-users-cog",
        "users.user": "fas fa-user",
        "users.DjangoGroupProxy": "fas fa-users",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "show_ui_builder": False,
    "language_chooser": True,
}


DEFAULT_QUEUE_NAME: Optional[str] = env("DEFAULT_QUEUE_NAME", default="default")
CELERY_ACKS_LATE: Optional[bool] = env("CELERY_ACKS_LATE", default=False)
CELERY_TRACK_STARTED: Optional[bool] = env("CELERY_TRACK_STARTED", default=False)
CELERY_WORKER_PREFETCH_MULTIPLIER: Optional[int] = env(
    "CELERY_WORKER_PREFETCH_MULTIPLIER", default=1
)
CELERY_BEAT_RUNS_EACH_N_MINUTES: Optional[int] = env(
    "CELERY_BEAT_RUNS_EACH_N_MINUTES", default=15
)
CELERY_BEAT_EXPIRES_IN_N_DAYS: Optional[int] = env(
    "CELERY_BEAT_EXPIRES_IN_N_DAYS", default=3
)
CELERY_ALWAYS_EAGER: Optional[bool] = env("CELERY_ALWAYS_EAGER", default=True)
BROKER_URL: str = env("BROKER_URL")
BROKER_TRANSPORT: str = env("BROKER_TRANSPORT")

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ),
    "EXCEPTION_HANDLER": "app.drf_exc_handler.make_error_message_on_validation_error",
}
SPECTACULAR_SETTINGS = {
    "TITLE": _("BoilerPlate"),
    "DESCRIPTION": _("The BoilerPlate's API"),
    "VERSION": "1.0.0",
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
}
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=env("ACCESS_TOKEN_LIFETIME_MINUTES", cast=int)
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=env("REFRESH_TOKEN_LIFETIME_DAYS", cast=int)
    ),
    "UPDATE_LAST_LOGIN": True,
    "ROTATE_REFRESH_TOKENS": True,
}
