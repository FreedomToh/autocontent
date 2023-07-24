import os

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

REDIS_URL = os.getenv('REDIS_URL', f'redis://127.0.0.1:{REDIS_PORT}')
BROKER_URL = REDIS_URL
# CELERY_BROKER_URL = REDIS_URL
# CELERY_RESULT_BACKEND = REDIS_URL
# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TIMEZONE = TIME_ZONE
# CELERY_TASK_DEFAULT_QUEUE = 'default'

CACHE_KEYS_TEMPLATES = {}

ONE_DAY_TIMEOUT = 86400  # 24 hours
TWO_DAYS_TIMEOUT = 172800  # 48 hours


REDIS_USER = os.getenv("REDIS_USER")
REDIS_PASSWORD = os.getenv("REDIS_PASS")

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "HOST": REDIS_HOST,
        "PORT": REDIS_PORT,
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            #"USER": REDIS_USER,
            # "PASSWORD": REDIS_PASSWORD,
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

