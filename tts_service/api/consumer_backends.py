import logging
import time

from django.conf import settings

from api import models
from api.models import set_request_ready_to_download
from tts_service.rmq_backend import Rabbit
from tts_service.yandex_backend import YandexTtsService


def receive_message(channel, method, properties, body):
    message_data = Rabbit.decode_rabbit_data(body).get("data")
    request_id = message_data.get("request_id", "no request id")
    if message_data.get("type") != settings.RMQ_QUEUE:
        logging.warning(f"receive_message: incorrect queue for message {request_id}, {body}")
        channel.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
        return

    logging.debug(f"receive_message for id {request_id}")
    request_objects = models.RequestsModel.objects.select_related('user_id').filter(request_id=request_id)
    if not request_objects.exists():
        logging.warning(f"receive_message: request {request_id} doesn`t exists")
        channel.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
        return
    request_object = request_objects.first()

    api = YandexTtsService()
    tts_data = api.text_to_speech(dict(text=request_object.response_text), request_id=request_object.request_id)
    if tts_data.get("error") or not tts_data.get("cache_key"):
        logging.error(f"consumer receive_message fail: {tts_data}")
        channel.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
        return

    set_request_ready_to_download(request_object)
    channel.basic_ack(delivery_tag=method.delivery_tag)


def run_consumer():
    logging.info(f"Rabbit init CONSUMER")
    logging.info(f'Queue: {settings.RMQ_QUEUE}')
    logging.info(f'Exchange: {settings.RMQ_EXCHANGE}')

    rabbit = Rabbit(
        exchange=settings.RMQ_EXCHANGE,
        tank=settings.RMQ_EXCHANGE_TANK,
        queue=settings.RMQ_QUEUE,
        queue_tank=settings.RMQ_QUEUE_TANK,
        arguments=settings.RMQ_ARGS,
        tank_arguments=settings.RMQ_TANK_ARGS,
    )

    args = []
    rabbit.bind_func(receive_message, args)
    try:
        rabbit.start_consuming()
    except KeyboardInterrupt:
        logging.info(f"Rabbit stopping")
        rabbit.stop_consuming()
    except Exception as ex:
        logging.error(f"Rabbit consumer fail: {ex}")
        exit()

    rabbit.close()
