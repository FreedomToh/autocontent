import datetime
import json
import logging
import os
import uuid

import redis.exceptions
import requests
from django.conf import settings
from django.core.cache import cache
from rest_framework import status

from api.serializers import YandexTokenModelSerializer


class YandexTtsService:
    generate_tts_url = "https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize"
    token = None
    iam_token = None

    speed = None
    voice = None
    emotion = None

    def __init__(self, speed: str = None, voice:str = None, emotion: str = None):
        self.prepare_voice(speed, voice, emotion)

        self.token = settings.YANDEX_OAUTH_TOKEN
        self.get_auth_token()
        if not self.token:
            raise FileNotFoundError("no yandex token")

    def prepare_voice(self, speed, voice, emotion):
        pass

    def get_tts_to_cache(self, data, request_id: int) -> dict:
        """
            Функция отправляет данные для генерации TTS, получает байты и складывает их в кэш
        """
        file_name = f"{str(uuid.uuid4())}.mp3"
        cache_key = f"{settings.KEY_PREFIX}_{request_id}"
        # file_name = "5015e01e-c85d-4a8e-a431-d6eaf37a70a5.mp3"
        file_data = self.__request__(self.generate_tts_url, data, False)
        cache.set(cache_key, file_data, settings.ONE_HOUR_TIMEOUT)
        return {
            "file_name": file_name,
            "cache_key": cache_key
        }

    def get_tts_to_file(self, data, request_id: int) -> dict:
        """
            Функция отправляет данные для генерации TTS
        """
        file_name = f"{settings.KEY_PREFIX}_{request_id}"
        # file_name = "5015e01e-c85d-4a8e-a431-d6eaf37a70a5.mp3"
        file_data = self.__request__(self.generate_tts_url, data, False)
        file_path = os.path.join(settings.YANDEX_DIR_PATH, file_name)
        with open(file_path, "wb") as mp3file:
            mp3file.write(file_data)
        return {
            "file_name": file_name,
            "file_path": file_path
        }

    def __request__(self, url, data, encode=True):
        headers = {
            "Authorization": f"Bearer {self.iam_token}"
        }

        response = requests.post(url, headers=headers, data=data)
        if not status.is_success(response.status_code):
            raise requests.exceptions.RequestException(f"fail request to yandex server: {response.content}")
        if not encode:
            return response.content
        else:
            return json.loads(response.content)

    def __get_auth_token__(self) -> str:
        """
            Функция выполняет получение iam токена
            https://cloud.yandex.ru/docs/iam/operations/iam-token/create
        """
        if not settings.YANDEX_GET_TOKEN_URL or not settings.YANDEX_OAUTH_TOKEN:
            raise ValueError("constants YANDEX_GET_TOKEN_URL or YANDEX_OAUTH_TOKEN not exists")

        r = requests.post(
            settings.YANDEX_GET_TOKEN_URL,
            data=json.dumps({'yandexPassportOauthToken': settings.YANDEX_OAUTH_TOKEN}),
            headers={'Content-Type': 'application/json'}
        )
        if not status.is_success(r.status_code):
            raise requests.exceptions.RequestException(f"fail request to yandex server: {r.content}")

        auth_data = json.loads(r.content)
        serializer = YandexTokenModelSerializer(
            data={"token": auth_data.get('iamToken'), "exp_date": auth_data.get('expiresAt')}
        )
        if not serializer.is_valid():
            raise requests.exceptions.RequestException(f"incorrect token or expirity date: {serializer.errors}")
        serializer.save()
        return auth_data.get('iamToken')

    def get_auth_token(self) -> None:
        model_obj = YandexTokenModelSerializer.Meta.model
        # self.iam_token = self.__get_auth_token__()
        # return
        if model_obj.objects.exists():
            if model_obj.objects.latest('exp_date').exp_date.date() < datetime.datetime.now().date():
                self.iam_token = self.__get_auth_token__()
            else:
                self.iam_token = model_obj.objects.latest('exp_date').token
        else:
            self.iam_token = self.__get_auth_token__()

    def text_to_speech(self, request_data: dict, request_id: int) -> dict:
        """
        https://cloud.yandex.ru/docs/speechkit/tts/request
        """
        if not settings.YANDEX_FOLDER_ID:
            raise ValueError("constant YANDEX_FOLDER_ID not exists")

        if not self.iam_token:
            self.get_auth_token()
        prepared_data = {
            "text": request_data.get("text"),
            "lang": request_data.get("lang", "ru-RU"),
            "voice": request_data.get("voice", "filipp"),
            "emotion": request_data.get("emotion", "good"),
            "speed": request_data.get("speed", 1.0),
            "format": "mp3",
            "folderId": settings.YANDEX_FOLDER_ID
        }
        logging.debug(prepared_data)

        # Если кэш работает - засовываем в кэш,
        # Если нет - сохраняем файл
        try:
            cache.set("ping", "pong", 1000)
            return self.get_tts_to_cache(prepared_data, request_id=request_id)
        except redis.exceptions.ConnectionError:
            logging.error("REDIS is down")
            return {"error": "REDIS is down"}
            # return self.get_tts_to_file(prepared_data, request_id=request_id)
        except Exception as ex:
            logging.error(f"Is something wrong: {ex}")
            return {"error": ex}

