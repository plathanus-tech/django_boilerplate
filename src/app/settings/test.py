# type: ignore

import os
from typing import List

from .common import *

INSTALLED_APPS: List[str] = DJANGO_APPS + THIRD_PARTY_APPS + YOUR_PROJECT_APPS

STATICFILES_DIRS += [
    os.path.join(BASE_DIR, "app/static"),
]

MEDIA_ROOT = os.path.join(BASE_DIR, "test_media/")
