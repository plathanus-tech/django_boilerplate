from datetime import timedelta

from environ import Env

env = Env()

ACCESS_TOKEN_LIFETIME_MINUTES = env.int("ACCESS_TOKEN_LIFETIME_MINUTES", default=15)
REFRESH_TOKEN_LIFETIME_DAYS = env.int("REFRESH_TOKEN_LIFETIME_DAYS", default=7)

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=ACCESS_TOKEN_LIFETIME_MINUTES),
    "REFRESH_TOKEN_LIFETIME": timedelta(REFRESH_TOKEN_LIFETIME_DAYS),
    "UPDATE_LAST_LOGIN": False,
    # We don't want that this is controlled by the serializers of the drf-simple-jwt,
    # we take care of it
    "ROTATE_REFRESH_TOKENS": True,
}
