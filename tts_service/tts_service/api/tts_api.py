import logging
import os

import requests
from rest_framework import status


class TtsApi:
    url = None

    def __init__(self):
        # self.url = os.getenv("TTS_URL")
        self.url = "http://192.168.31.187:8001"
        if not self.url:
            raise NotImplementedError("TTS url not configured")

    def __request_to_api__(self, payload: dict):
        url = f"{self.url}/api/yandex/v1/generate/"
        response = requests.post(url, data=payload)
        if not status.is_success(response.status_code):
            return {
                "error": response.content
            }

        return response.json()

    def text_to_speech(self, text: str) -> dict:
        if len(text) == 0:
            logging.error("text_to_speech error: no text")
            return {
                "error": "no text"
            }

        return self.__request_to_api__({"text": text})

