import os
import sys
import environ
from pathlib import Path
from typing import List, Dict, Any

# Build paths from src directory
BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

env: environ.Env = environ.Env(
    # Key=(type cast, default)
    DJANGO_DEBUG=(bool, False),
    CORS_ORIGIN_ALLOW_ALL=(bool, False),
)

env_file: str = os.path.join(os.path.join(os.path.dirname(__file__), ".env"))
if os.path.exists(env_file) and "pytest" not in sys.argv:
    print("Loading environment variables from file")
    environ.Env.read_env(str(env_file))


# Security
SECRET_KEY: str = env("DJANGO_SECRET_KEY")
DEBUG: bool = env("DJANGO_DEBUG", default=False)
ALLOWED_HOSTS: List[str] = env.list("DJANGO_ALLOWED_HOSTS", default=[])
CORS_ORIGIN_ALLOW_ALL: bool = env("DJANGO_CORS_ORIGIN_ALLOW_ALL", default=False)
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


# Application definition
DJANGO_APPS: List[str] = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
THIRD_PARTY_APPS: List[str] = [
    "material",
    "material.admin",
]
YOUR_PROJECT_APPS: List[str] = [
    "demo.apps.DemoConfig",
]
LOGIN_REDIRECT_URL: str = "/admin/"

MIDDLEWARE: List[str] = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF: str = "app.urls"
TEMPLATES: List[Dict[str, Any]] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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
    "default": env.db(default="sqlite:////tmp/my-tmp-sqlite.db")
}
DEFAULT_AUTO_FIELD: str = "django.db.models.BigAutoField"


# Internationalization
LANGUAGE_CODE: str = "en-us"
TIME_ZONE: str = "UTC"
USE_I18N: bool = True
USE_TZ: bool = True


# Static Files
STATIC_URL: str = "/static/"
STATIC_ROOT: str = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS: List[str] = []
STATICFILES_FINDERS: List[str] = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
STATICFILES_STORAGE: str = "whitenoise.storage.CompressedManifestStaticFilesStorage"


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


# Material Admin Site
MATERIAL_ADMIN_SITE: Dict[str, Any] = {
    "HEADER": ("Admin"),
    "TITLE": ("BoilerPlate"),
    "FAVICON": "favicon.png",
    "MAIN_BG_COLOR": "#007aff",  # Admin site main color, css color should be specified
    "MAIN_HOVER_COLOR": "#43d1ab",  # Admin site main hover color, css color should be specified
    "PROFILE_PICTURE": "",  # Admin site profile picture (path to static should be specified)
    "PROFILE_BG": "",  # Admin site profile background (path to static should be specified)
    "LOGIN_LOGO": "",  # Admin site logo on login page (path to static should be specified)
    "LOGOUT_BG": "",  # Admin site background on login/logout pages (path to static should be specified)
    "SHOW_THEMES": False,
    "TRAY_REVERSE": False,
    "NAVBAR_REVERSE": False,
    "SHOW_COUNTS": True,
    "APP_ICONS": {
        # Set icons for applications(lowercase), including 3rd party apps:
        # {'application_name': 'material_icon_name', ...}
        "sites": "send",
    },
    "MODEL_ICONS": {
        "site": "contact_mail",
    },
}
