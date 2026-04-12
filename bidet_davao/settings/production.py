from .base import *
DEBUG = False

PARSED_ALLOWED_HOSTS = env('ALLOWED_HOSTS', default="dvobdt.com,www.dvobdt.com").split(',')
ALLOWED_HOSTS.extend(PARSED_ALLOWED_HOSTS)