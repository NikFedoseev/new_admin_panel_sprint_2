from pathlib import Path
import os
from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', False) == 'True'

include(
    'components/database.py',
    'components/installed_apps.py',
    'components/middlewares.py',
    'components/templates.py',
    'components/internatiolization.py',
    'components/auth.py',
    'components/logging.py'
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1').split(',')

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOCALE_PATHS = ['movies/locale']

INTERNAL_IPS = [
    "127.0.0.1",
    '0.0.0.0',
    'localhost',
    '192.168.112.4',
]
