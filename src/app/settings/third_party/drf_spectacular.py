from app.settings.env import env

SPECTACULAR_SETTINGS = {
    "TITLE": env.str("PROJECT_NAME", default="boilerplate"),
    "VERSION": "1.0.0",
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    "SERVE_PUBLIC": False,
}
