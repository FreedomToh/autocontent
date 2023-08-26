import os

import django.core.cache.backends.redis

REDIS_URL = os.getenv('REDIS_URL', 'redis://redis.autocontent:6379')
BROKER_URL = REDIS_URL
TTS_PREFIX = "tts_service"
# CELERY_BROKER_URL = REDIS_URL
# CELERY_RESULT_BACKEND = REDIS_URL
# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TIMEZONE = TIME_ZONE
# CELERY_TASK_DEFAULT_QUEUE = 'default'


ONE_HOUR_TIMEOUT = 3600  # 24 hours
ONE_DAY_TIMEOUT = 86400  # 24 hours
TWO_DAYS_TIMEOUT = 172800  # 48 hours

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL
    }
}

# django.core.cache.backends.redis.RedisCache
