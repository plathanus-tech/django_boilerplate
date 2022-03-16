from .common import *
from typing import List

print("Applying PROD Settings")

INSTALLED_APPS: List[str] = DJANGO_APPS + THIRD_PARTY_APPS + YOUR_PROJECT_APPS

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

STATIC_ROOT: str = os.path.join(BASE_DIR, "static")
