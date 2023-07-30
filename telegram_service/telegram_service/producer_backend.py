import logging
import time

from django.conf import settings

from api.models import get_messages_without_response, set_message_in_work
from requests_connector.models import get_finished_messages
from telegram_service.rmq_backend import Rabbit


def get_success_messages():
    # get messages without response
    messages_prepared = get_messages_without_response()
    if len(messages_prepared) == 0:
        return []

    ids = [m.get("id") for m in messages_prepared.values("id")]
    messages_finished = get_finished_messages(ids)
    return [
        {
            "user": message.user_id.user_id,
            "message_id": message.request_id,
        }
        for message in messages_finished
    ]


def messages_to_queue(rabbit: Rabbit, messages: list):
    for message in messages:
        if rabbit.publish(message):
            set_message_in_work(message)


def run_producer():
    logging.info(f"Rabbit init PRODUCER")
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

    try:
        while True:
            messages = get_success_messages()
            messages_to_queue(rabbit, messages)
            time.sleep(5)
    except KeyboardInterrupt:
        logging.info(f'Exit')
    except Exception as ex:
        logging.error(f"producer run fail: {ex}")

    rabbit.close()



