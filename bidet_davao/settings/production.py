from socket import gethostbyname, gethostname

from .base import *

DEBUG = False
USE_S3 = env.bool('USE_S3', default=False)

PARSED_ALLOWED_HOSTS = env('ALLOWED_HOSTS', default="dvobdt.com,www.dvobdt.com").split(',')
ALLOWED_HOSTS.extend(PARSED_ALLOWED_HOSTS)

try:
    hostname = gethostname()
    container_ip = gethostbyname(hostname)
    if container_ip:
        ALLOWED_HOSTS.append(container_ip)
except Exception:
    # Fallback if socket fails
    pass

ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS if host.strip()]

if USE_S3:
    AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME', default=None)
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME', default=None)

    # S3 Settings
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    
    # Static file settings
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
    STORAGES = {
        "staticfiles": {
            "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
            "OPTIONS": {
                "location": "static",
            },
        },
    }