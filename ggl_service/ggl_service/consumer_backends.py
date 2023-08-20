import logging
import time

from django.conf import settings

from api import models
from api.backends import get_audio_info, free_cache
from api.models import add_audio_link_to_request
from ggl_service.apis.google_drive import GoogleDriveApi
from ggl_service.rmq_backend import Rabbit


def receive_message(channel, method, properties, body):
    message_data = Rabbit.decode_rabbit_data(body).get("data")
    request_id = message_data.get("request_id", "no request id")

    logging.info(f"Get request with id {request_id}")
    if message_data.get("type") != settings.RMQ_QUEUE:
        logging.warning(f"receive_message: incorrect queue for message {request_id}, {body}")
        channel.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
        return

    logging.debug(f"receive_message for id {request_id}")
    request_objects = models.RequestStatusesModel.objects.select_related('request_id').filter(request_id=request_id)
    if not request_objects.exists():
        logging.warning(f"receive_message: request {request_id} doesn`t exists")
        channel.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
        return
    request_object = request_objects.first()
    data_info = get_audio_info(request_object.request_id)
    if "error" in data_info:
        logging.error(f"receive_message: data for {request_id} doesn`t exists")
        channel.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
        return

    google_api = GoogleDriveApi()
    result = google_api.load_to_disc(data_info)
    if "url" not in result:
        logging.warning(f"receive_message: google_api.load_to_disc for {request_id}: something went wrong")
        channel.basic_reject(delivery_tag=method.delivery_tag, requeue=True)
        return

    if not add_audio_link_to_request(request_object.request_id, result.get("url")):
        logging.error(f"receive_message: add_audio_link_to_request for {request_id} fail")
        channel.basic_reject(delivery_tag=method.delivery_tag, requeue=True)
        return

    models.set_request_audio_loaded(request_object)
    free_cache(data_info)
    logging.info(f"Ready request with id {request_id}")
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