from django.core.exceptions import ImproperlyConfigured

from app.settings.env import env

PROJECT_NAME = env.str("PROJECT_NAME", default="boilerplate")
HOST = env.str("HOST", default="localhost")

EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")

EMAIL_HOST = env("EMAIL_HOST", default="mailpit")
EMAIL_PORT = env.int("EMAIL_PORT", default=1025)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=False)
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL", default=False)


EMAIL_SUBJECT_PREFIX = env("EMAIL_SUBJECT_PREFIX", default=f"[{PROJECT_NAME.title()}] -")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default=f"{PROJECT_NAME.title()} <noreply@{HOST}>")
SERVER_EMAIL = env("SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)

ON_PRODUCTION = env.bool("DJANGO_ON_PRODUCTION", default=False)
if ON_PRODUCTION:
    if EMAIL_HOST == "mailpit":
        raise ImproperlyConfigured("Mailpit should only be used for development")

    if EMAIL_USE_SSL and EMAIL_USE_TLS:
        raise ImproperlyConfigured("EMAIL_USE_SSL and EMAIL_USE_TLS are mutually exclusive")
