from .common import *
from typing import List

print("Applying PROD Settings")

INSTALLED_APPS: List[str] = DJANGO_APPS + THIRD_PARTY_APPS + YOUR_PROJECT_APPS
