import os
from typing import List

from .common import *

MEDIA_ROOT = os.path.join(ROOT_DIR, "media/")
MEDIA_URL = "/media/"

CSRF_TRUSTED_ORIGINS = ["http://*.com", "https://*.ngrok.io"]

# Debug Tool Bar Config
if DEBUG:
    THIRD_PARTY_APPS += [
        "debug_toolbar",
    ]
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]
    INTERNAL_IPS: List[str] = ["127.0.0.1", os.environ.get("HOST", "localhost")]
    DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda request: True}

INSTALLED_APPS: List[str] = DJANGO_APPS + THIRD_PARTY_APPS + YOUR_PROJECT_APPS

ROOT_URLCONF = "app.urls_dev"

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = ROOT_DIR / "dev_notifications" / "emails"

SMS_BACKEND = "app.ext.sms.backends.filebased.FileBasedSmsBackend"
SMS_FILE_PATH = ROOT_DIR / "dev_notifications" / "sms"
