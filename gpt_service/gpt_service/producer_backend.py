import logging

from django.conf import settings

from gpt_service.rmq_backend import Rabbit


def prepare_query_element():
    ...

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
        prepare_query_element()
