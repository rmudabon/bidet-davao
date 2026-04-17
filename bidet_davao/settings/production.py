from .base import *
DEBUG = False

PARSED_ALLOWED_HOSTS = env('ALLOWED_HOSTS', default="dvobdt.com,www.dvobdt.com").split(',')
ALLOWED_HOSTS.extend(PARSED_ALLOWED_HOSTS)

USE_S3 = env.bool('USE_S3', default=False)

if USE_S3:
    AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME', default=None)
    AWS_STORAGE_BUCKET_NAME = env('AWS_S3_BUCKET_NAME', default=None)

    # S3 Settings
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    
    # Static file settings
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
    STATICFILES_STORAGE = 'storages.backends.s3.S3Storage'