from environ import Env

env = Env()

REDIS_HOST = env("REDIS_HOST")
REDIS_PORT = env("REDIS_PORT", cast=int)
REDIS_PASSWORD = env("REDIS_PASSWORD", default=None)
REDIS_DB = env("REDIS_DB", default="0")
if REDIS_PASSWORD is None:
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
else:
    REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
