from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class PrivateMediaStorage(S3Boto3Storage):
    """Stores privately on Aws S3"""

    location = settings.AWS_MEDIA_LOCATION
    default_acl = "private"
    file_overwrite = False
    custom_domain = False


class PublicMediaStorage(S3Boto3Storage):
    """Stores public on Aws S3"""

    location = settings.AWS_MEDIA_LOCATION
    default_acl = "public-read"
    file_overwrite = False
    custom_domain = False
