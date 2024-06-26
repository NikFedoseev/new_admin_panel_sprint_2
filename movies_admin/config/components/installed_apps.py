from django.conf import settings

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'movies'
]

if settings.DEBUG:
    INSTALLED_APPS.extend([
        'debug_toolbar',
    ])
