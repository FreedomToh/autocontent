import logging

from django.conf import settings
from api import models, serializers
from api.serializers import change_status, get_statuses

from gpt_service.rmq_backend import Rabbit


statuses = get_statuses()


def get_query_elements():
    return models.RequestStatusesModel.objects.select_related("request_id").filter(
        gpt_status=statuses.get("WAITING")
    )


def add_request_to_queue(rabbit: Rabbit, request: models.RequestsModel):
    serializer = serializers.RequestModelSerializer(request)
    if rabbit.publish(serializer.data):
        change_status(request, statuses=statuses, gpt_status="INPROCESS")


def run_producer():
    logging.info(f"Rabbit init PRODUCER")
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
    while True:
        text_requests = get_query_elements()
        for request in text_requests:
            add_request_to_queue(rabbit, request.request_id)

        break
