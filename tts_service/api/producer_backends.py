import logging
import time

from django.conf import settings

from api import models, serializers
from api.models import get_query_elements, set_request_in_work
from tts_service.rmq_backend import Rabbit


def add_request_to_queue(rabbit: Rabbit, request: models.RequestStatusesModel):
    serializer = serializers.RequestModelSerializer(request.request_id)
    if rabbit.publish(serializer.data):
        set_request_in_work(request)
        return True
    return False


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
            text_requests = get_query_elements()
            for request in text_requests:
                add_request_to_queue(rabbit, request)

            time.sleep(settings.RMQ_PRODUCER_SLEEP)
    except KeyboardInterrupt:
        logging.info(f'Exit')
    except Exception as ex:
        logging.error(f"normalizer producer run fail: {ex}")

    rabbit.close()
