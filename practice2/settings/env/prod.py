from settings.base import *


DEBUG = False

ALLOWED_HOSTS = ['sephyra.kz']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}