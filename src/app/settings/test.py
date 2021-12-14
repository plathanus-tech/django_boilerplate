import os
from .common import *
from typing import List

print("Applying TEST Settings")

INSTALLED_APPS: List[str] = DJANGO_APPS + THIRD_PARTY_APPS + YOUR_PROJECT_APPS

STATICFILES_DIRS += [
    os.path.join(BASE_DIR, "app/static"),
]
print(INSTALLED_APPS)
