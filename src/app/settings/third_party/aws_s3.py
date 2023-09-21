from environ import Env

env = Env()

AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID", str)
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY", str)
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME", str)
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
AWS_MEDIA_LOCATION = "media/"
