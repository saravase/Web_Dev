from .base import *
import os

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
INSTALLED_APPS += ('django_nose',)
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
TEST_OUTPUT_DIR = os.environ.get('TEST_OUTPUT_DIR','.')
NOSE_ARGS = [
'--verbosity=2',
'--nologcapture',
'--with-coverage',
'--cover-package=todo',
'--with-spec',
'--spec-color',
'--with-xunit',
'--xunit-file=%s/unittests.xml'% TEST_OUTPUT_DIR,
'--cover-xml',
'--cover-xml-file=%s/coverage.xml'% TEST_OUTPUT_DIR
]

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