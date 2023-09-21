from environ import Env

env = Env()

CORS_ORIGIN_ALLOW_ALL: bool = env.bool("CORS_ORIGIN_ALLOW_ALL", default=False)
if not CORS_ORIGIN_ALLOW_ALL:
    CORS_ORIGIN_WHITELIST = env.list("CORS_ORIGIN_WHITELIST", default=[])
