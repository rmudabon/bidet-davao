from .base import *

import os
import socket

DEBUG = False

PRIVATE_IP = socket.gethostbyname(socket.gethostname())

ALLOWED_HOSTS = [
    '0.0.0.0',
    '127.0.0.1' 
    'https://dvobdt.com',
    PRIVATE_IP,  
]