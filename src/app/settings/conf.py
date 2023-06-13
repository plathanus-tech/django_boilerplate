import os
from datetime import timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import environ
from django.utils.translation import gettext_lazy as _

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
SECRET_KEY: str = env("DJANGO_SECRET_KEY")
ALLOWED_HOSTS: List[str] = env.list("DJANGO_ALLOWED_HOSTS", default=[])
DEBUG: bool = env("DJANGO_DEBUG", cast=bool, default=False)
USE_DEBUG_TOOLBAR = env("USE_DEBUG_TOOLBAR", cast=bool, default=False)
IS_TESTING = env("IS_TESTING", cast=bool, default=False)


SECURE_SSL_REDIRECT = env("SECURE_SSL_REDIRECT", bool, default=False)
CSRF_COOKIE_SECURE = env("CSRF_COOKIE_SECURE", bool, default=False)
SECURE_HSTS_SECONDS = env("SECURE_HSTS_SECONDS", int, default=0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env("SECURE_HSTS_INCLUDE_SUBDOMAINS", bool, default=False)
SECURE_HSTS_PRELOAD = env("SECURE_HSTS_PRELOAD", bool, default=False)
SESSION_COOKIE_SECURE = env("SESSION_COOKIE_SECURE", bool, default=False)

# Security - CORS
CORS_ORIGIN_ALLOW_ALL: bool = env("CORS_ORIGIN_ALLOW_ALL", cast=bool, default=False)
if not CORS_ORIGIN_ALLOW_ALL:
    CORS_ORIGIN_WHITELIST: List[str] = env.list("CORS_ORIGIN_WHITELIST", default=[])

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
    "rest_framework_simplejwt",
    "rest_framework.authtoken",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "corsheaders",
]
YOUR_PROJECT_APPS: List[str] = [
    "app",
    "users.apps.UsersConfig",
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + YOUR_PROJECT_APPS


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
    "django.middleware.locale.LocaleMiddleware",
    "app.middlewares.tz.TimezoneMiddleware",
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

REDIS_HOST = env("REDIS_HOST")
REDIS_PORT = env("REDIS_PORT", cast=int)
REDIS_PASSWORD = env("REDIS_PASSWORD", default=None)
REDIS_DB = env("REDIS_DB", default="0")
if REDIS_PASSWORD is None:
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
else:
    REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

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
LANGUAGE_CODE: str = "pt-br"
LANGUAGES: List[Tuple[str, str]] = [
    ("pt-br", _("Brazilian Portuguese")),
    ("en-us", _("English")),
]
LOCALE_PATHS = [
    BASE_DIR / "app" / "locale",
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
TIMEZONE_FOR_LANGUAGE = {
    "pt-br": "America/Sao_Paulo",
    "en": "UTC",
}

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
STATICFILES_STORAGE: str = "django.contrib.staticfiles.storage.StaticFilesStorage"

# Media files
MEDIA_ROOT = os.path.join(ROOT_DIR, env("MEDIA_ROOT", default="storage/media/"))
MEDIA_URL = "/media/"

# Storages
DEFAULT_FILE_STORAGE = env(
    "DEFAULT_FILE_STORAGE", default="django.core.files.storage.FileSystemStorage"
)
if DEFAULT_FILE_STORAGE == "app.ext.storage.aws_s3.PrivateMediaStorage":
    INSTALLED_APPS.append("storages")
    AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID", str)
    AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY", str)
    AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME", str)
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": "max-age=86400",
    }
    AWS_MEDIA_LOCATION = "media/"

# Logging
LOGGING_LEVEL: str = env("DJANGO_LOGGING_LEVEL", default="INFO")
SENDGRID_LOGGING_LEVEL: str = env("SENDGRID_LOGGING_LEVEL", default="WARNING")
TWILIO_LOGGING_LEVEL: str = env("TWILIO_LOGGING_LEVEL", default="INFO")

LOGGING: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "formatters": {
        "verbose": {
            "format": "{levelname} {module} {asctime}: {message}",
            "style": "{",
        },
    },
    "filters": {
        "health_check_filter": {"()": "app.logging.filters.HealthCheckFilter"},
    },
    "root": {"handlers": ["console"], "level": LOGGING_LEVEL},
    "loggers": {
        "django.channels.server": {
            "handlers": ["console"],
            "level": LOGGING_LEVEL,
            "propagate": False,
            "filters": ["health_check_filter"],
        },
        "send_grid": {
            "handlers": ["console"],
            "level": SENDGRID_LOGGING_LEVEL,
        },
        "twilio": {
            "handlers": ["console"],
            "level": TWILIO_LOGGING_LEVEL,
        },
        "users.tasks": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}


JAZZMIN_SETTINGS = {
    "site_logo_classes": "img-circle",
    "site_icon": None,
    "site_title": "Admin",
    "site_brand": "Boilerplate",
    "site_header": "Admin",
    "welcome_sign": "Boilerplate",
    "user_avatar": None,
    "show_sidebar": True,
    "navigation_expanded": True,
    # https://fontawesome.com/v5/search?m=free
    "icons": {
        "users": "fas fa-users-cog",
        "users.user": "fas fa-user",
        "users.Group": "fas fa-users",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "show_ui_builder": False,
    "language_chooser": True,
}
JAZZMIN_UI_TWEAKS = {
    "actions_sticky_top": True,
    "navbar_fixed": True,
}


DEFAULT_QUEUE_NAME: Optional[str] = env("DEFAULT_QUEUE_NAME", default="default")
CELERY_ACKS_LATE: Optional[bool] = env("CELERY_ACKS_LATE", default=True)
CELERY_TRACK_STARTED: Optional[bool] = env("CELERY_TRACK_STARTED", default=False)
CELERY_WORKER_PREFETCH_MULTIPLIER: Optional[int] = env(
    "CELERY_WORKER_PREFETCH_MULTIPLIER", default=1
)
CELERY_BEAT_EXPIRES_IN_N_DAYS: Optional[int] = env("CELERY_BEAT_EXPIRES_IN_N_DAYS", default=3)
CELERY_ALWAYS_EAGER: Optional[bool] = env("CELERY_ALWAYS_EAGER", default=False)
BROKER_URL = REDIS_URL

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
}
SPECTACULAR_SETTINGS = {
    "TITLE": _("BoilerPlate"),
    "DESCRIPTION": _("The BoilerPlate's API"),
    "VERSION": "1.0.0",
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    "SERVE_PUBLIC": False,
}
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=env("ACCESS_TOKEN_LIFETIME_MINUTES", cast=int)),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=env("REFRESH_TOKEN_LIFETIME_DAYS", cast=int)),
    "UPDATE_LAST_LOGIN": True,
    "ROTATE_REFRESH_TOKENS": True,
}

# External Services
EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
if EMAIL_BACKEND == "app.ext.email.send_grid.SendGridEmailBackend":
    SENDGRID_API_KEY = env("SENDGRID_API_KEY")

SMS_BACKEND = env("SMS_BACKEND", default="app.ext.sms.backends.stdout.StdOutSmsBackend")
if SMS_BACKEND == "app.ext.sms.backends.twilio.TwilioSmsBackend":
    TWILIO_ACCOUNT_SID = env("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = env("TWILIO_AUTH_TOKEN")
    TWILIO_SERVICE_PHONE = env("TWILIO_SERVICE_PHONE")

PUSH_NOTIFICATION_SERVICE_ADAPTER = env("PUSH_NOTIFICATION_SERVICE_ADAPTER", default="expo")

if DEBUG and USE_DEBUG_TOOLBAR:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
    INTERNAL_IPS = ["127.0.0.1", os.environ.get("HOST", "localhost")]
    DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda request: True}
    ROOT_URLCONF = "app.urls_dev"

if IS_TESTING:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
