import logging
import time

from django.conf import settings
from api import models, serializers
from api.serializers import change_status, get_statuses

import logging

from gpt_service.backends import request_to_gpt
from gpt_service.rmq_backend import Rabbit


statuses = get_statuses()


def receive_message(channel, method, properties, body):
    message_data = Rabbit.decode_rabbit_data(body).get("data")
    request_id = message_data.get("request_id", "no request id")
    if message_data.get("type") != settings.RMQ_QUEUE_PRODUCER:
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

    text = request_object.request_text
    if len(text) == 0:
        logging.warning(f"receive_message: request {request_id} has incorrect text: {message_data}")
        channel.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
        return

    user = request_object.user_id
    result = request_to_gpt(text, user)
    response = result.get("message")
    if "error" in response:
        logging.warning(f"receive_message: fail response to gpt {response}")

        # If requeue, message come back to queue
        channel.basic_reject(delivery_tag=method.delivery_tag, requeue=True)
        return

    request_object.response_text = response
    request_object.save()
    change_status(request_object, gpt_status='READY')
    channel.basic_ack(delivery_tag=method.delivery_tag)


def run_consumer():
    logging.info(f"Rabbit init CONSUMER")
    logging.info(f'Queue: {settings.RMQ_QUEUE_PRODUCER}')
    logging.info(f'Exchange: {settings.RMQ_EXCHANGE}')

    rabbit = Rabbit(
        exchange=settings.RMQ_EXCHANGE,
        tank=settings.RMQ_EXCHANGE_TANK,
        queue=settings.RMQ_QUEUE_PRODUCER,
        queue_tank=settings.RMQ_QUEUE_PRODUCER_TANK,
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


