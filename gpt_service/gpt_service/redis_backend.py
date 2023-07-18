import logging

from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from redis import exceptions as redis_ex

from gpt_service.exceptions import FailRequestsResponse

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)
TIMEOUT = 172800  # 48 hours


class RedisBackend:
    status = False
