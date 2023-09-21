from app.settings.infra.hosting import HOST

INTERNAL_IPS = ["127.0.0.1", HOST]
DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda request: True}
