import logging

from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from redis import exceptions as redis_ex

from gpt_service.exceptions import FailRequestsResponse

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)
TIMEOUT = 172800  # 48 hours


class RedisBackend:
    def __init__(self, login=0, src=None):
        self.login = login
        self.src = src
        self.error = ""
        self.status = True

    def remove(self, key) -> bool:
        try:
            cache.delete(key)
        except redis_ex.ResponseError as ex:
            logging.log(40, f"RedisBackend fail: can`t delete key {key}. {ex}")
            return False

        return True

    def get(self, key):
        result = None
        try:
            result = cache.get(key)
        except redis_ex.ResponseError as ex:
            self.status = False
            self.error = str(ex)
            raise FailRequestsResponse(ex)

        return result

    def check(self, key) -> bool:
        result = False
        try:
            result = key in cache
        except redis_ex.ResponseError as ex:
            self.status = False
            self.error = str(ex)
            raise FailRequestsResponse(ex)

        return result

    def set(self, key, data, timeout) -> None:
        try:
            cache.set(key, data, timeout=timeout)
            self.status = True
        except redis_ex.ResponseError as ex:
            self.status = False
            self.error = str(ex)
            raise FailRequestsResponse(ex)

    def to_cache(self, data, start, end):
        for date in data:
            key = {'login': self.login,
                   'src': self.src,
                   'date': date}

            self.set(key, data[date], timeout=TIMEOUT)
            if not self.status:
                break

        dates = datetime_diap(start, end)
        for date in dates:
            if date not in data.keys():
                key = {'login': self.login,
                       'src': self.src,
                       'date': date}
                self.set(key, {}, timeout=TIMEOUT)
                if not self.status:
                    break

    def from_cache(self, data):
        if not data.get("start") or not data.get("end"):
            self.set_err("Not enough key start/end")
            return []

        dates = datetime_diap(data["start"], data["end"])

        loses = []
        for date in dates:
            key = {'login': self.login,
                   'src': self.src,
                   'date': date}
            if not self.check(key):
                loses.append(key)

            if not self.status:
                return []

        return loses

    def get_cache(self, data):
        dates = datetime_diap(data["start"], data["end"])

        cached_data = []
        for date in dates:
            key = {'login': self.login,
                   'src': self.src,
                   'date': date}
            c = self.get(key)
            if not self.status:
                return []

            cached_data += c

        return cached_data

    def set_err(self, text: str) -> None:
        self.status = False
        self.error = str(text)
