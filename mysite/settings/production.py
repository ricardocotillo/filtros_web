import environ
from .base import *  # noqa

DEBUG = False

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))  # noqa

SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'atencionalcliente@filtroswillybusch.com.pe'
EMAIL_USE_SSL = True
EMAIL_PORT = 465

try:
    from .local import *  # noqa
except ImportError:
    pass
