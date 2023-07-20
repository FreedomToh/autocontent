import logging

import pika
from django.conf import settings

from gpt_service.exceptions import RMQNoConfigError


class Rabbit:
    connection = None
    channel = None
    host = None

    exchange = None
    exchange_tank = None

    arguments = None
    tank_arguments = None

    queue = None
    queue_tank = None

    def __init__(self, exchange, tank, queue, queue_tank, arguments, tank_arguments):
        self.host = settings.RMQ_HOST
        self.exchange_tank = tank
        self.exchange = exchange
        self.queue = queue
        self.queue_tank = queue_tank
        self.arguments = arguments
        self.tank_arguments = tank_arguments

        self.__init_connection__()
        self.__init_channel__()

    def __init_connection__(self):
        if not self.host:
            raise RMQNoConfigError

        credentials = pika.PlainCredentials(settings.RMQ_LOGIN, settings.RMQ_PASSWORD)
        configs = pika.ConnectionParameters(host=self.host, heartbeat=600, credentials=credentials)
        self.connection = pika.BlockingConnection(configs)

    def __init_channel__(self):
        if not self.exchange_tank or not self.exchange:
            raise RMQNoConfigError

        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=settings.RMQ_PREFETCH_COUNT, global_qos=settings.RMQ_PREFETCH_GLOBAL)
        self.channel.exchange_declare(exchange=self.exchange, exchange_type='fanout')
        self.channel.exchange_declare(exchange=self.exchange_tank, exchange_type='fanout')

        self.channel.queue_declare(queue=self.queue, durable=True, arguments=self.arguments)
        self.channel.queue_declare(queue=self.queue_tank, durable=True, arguments=self.tank_arguments)

        self.channel.queue_bind(exchange=self.exchange_tank, queue=self.queue_tank, )
        self.channel.queue_bind(exchange=self.exchange, queue=self.queue, )


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
        ...
