from .base import *
import os

if os.environ.get('DEBUG'):
	DEBUG = True
else:
	DEBUG = False
	
ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS'), '*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'todo',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}

STATIC_ROOT = os.environ.get('STATIC_ROOT','/var/www/TodoApp/static')
MEDIA_ROOT = os.environ.get('MEDIA_ROOT','/var/www/TodoApp/media')