import os


TESTING = True
DEBUG = True

MONGO_SETTINGS = {
    'DB_NAME': 'test_{}'.format(os.environ.get('APPLICATION_NAME')),
    'HOST': 'mongomock://localhost',
    'PORT': 27017,
    'USERNAME': '',
    'PASSWORD': '',
}

CELERY_ALWAYS_EAGER = True
