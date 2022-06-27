import os
from .common import *
from typing import List


INSTALLED_APPS: List[str] = DJANGO_APPS + THIRD_PARTY_APPS + YOUR_PROJECT_APPS

STATICFILES_DIRS += [
    os.path.join(BASE_DIR, "app/static"),
]
