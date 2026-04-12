from socket import gethostbyname, gethostname
from .base import *

DEBUG = False

PRIVATE_IP = gethostbyname(gethostname())

ALLOWED_HOSTS = ['*']