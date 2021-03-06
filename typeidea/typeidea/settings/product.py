from .base import * # NOQA

DEBUG = False

ALLOWED_HOSTS = ['www.the5fire.com']

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.mysql',
        'NAME': 'typeidea_db',
        'USER': 'root',
        'PASSWORD': 'Wobushua2',
        'HOST':'127.0.0.1',
        'PORT': '3306',
        'CONN_MAX_AGE': 5*60,
        'OPTIONS': {'charset':'utf8mb4'},
    }
}

REDIS_URL = '127.0.0.1:6379:1'

CACHES = {
    'default': {
        'BACKEND': 'django_redis,cache.RedisCache',
        'LOCATION': REDIS_URL,
        'TIMEOUT': 300,
        'OPTIONS': {
            #'PASSWORD':'',
            'CLIENT_CLASS': 'django_redis.cliend.DefaultClient',
            'PARSE_CLASS': 'redis.connection.HiredisParser',
        },
        'CONNECTION_POOL_CLASS': 'redis.connection.BlockingConnectionPool',
    }
}

#MIDDLEWARE += [
#    'django.middleware.cache.UpdateCacheMiddleware',
#]