import logging
import time

from django.conf import settings

from api import models, serializers
from api.models import get_query_elements, set_request_in_work, set_request_ready_to_download
from tts_service.rmq_backend import Rabbit
from tts_service.yandex_backend import YandexTtsService


def run_wrapper():
    api = YandexTtsService()
    requests = get_query_elements()

    for request in requests:
        request_id = request.request_id.request_id
        if len(request.request_id.response_text) == 0:
            continue

        tts_data = api.text_to_speech(dict(text=request.request_id.response_text), request_id=request_id)
        # tts_data = {'file_name': '88bfec0e-ec2f-43f6-8071-d4e14c53cb43.mp3', 'cache_key': 'tts_service_2'}
        if tts_data.get("cache_key"):
            set_request_ready_to_download(request)
