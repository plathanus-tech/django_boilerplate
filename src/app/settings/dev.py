# type: ignore

import os
from typing import List

from .common import *

MEDIA_ROOT = os.path.join(ROOT_DIR, "media/")
MEDIA_URL = "/media/"

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

ROOT_URLCONF: str = "app.urls_dev"
