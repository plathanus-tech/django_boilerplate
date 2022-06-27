import os
from .common import *
from typing import List

# Debug Tool Bar Config
THIRD_PARTY_APPS += [
    "debug_toolbar",
]
MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]
INTERNAL_IPS: List[str] = ["127.0.0.1", "localhost"]

INSTALLED_APPS: List[str] = DJANGO_APPS + THIRD_PARTY_APPS + YOUR_PROJECT_APPS

MEDIA_ROOT = os.path.join(ROOT_DIR, "media/")
MEDIA_URL = "/media/"


STATICFILES_DIRS += [
    os.path.join(BASE_DIR, "app/static"),
]
