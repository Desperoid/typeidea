from .base import * # NOQA
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.mysql',
        'NAME': 'typeidea_db',
        'USER': 'root',
        'PASSWORD': 'Wobushua2',
        'HOST':'127.0.0.1',
        'PORT': '3306',
        #'CONN_MAX_AGE': 5*60,
        #'OPTIONS': {'charset':'utf8mb4'},
    }
}

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ['127.0.0.1']

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL':'https://cdn.bootcss.com/jquery/3.3.1/jquery.min.js',
}

