import os
from .common import *
from typing import List, Dict, Callable

print("Applying DEV Settings")

# Debug Tool Bar Config
THIRD_PARTY_APPS += [
    "debug_toolbar",
]
MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]
INTERNAL_IPS: List[str] = ["127.0.0.1", "localhost"]
DEBUG_TOOLBAR_CONFIG: Dict[str, Callable[..., bool]] = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: not request.is_ajax()
}

INSTALLED_APPS: List[str] = DJANGO_APPS + THIRD_PARTY_APPS + YOUR_PROJECT_APPS


STATICFILES_DIRS += [
    os.path.join(BASE_DIR, "app/static"),
]
