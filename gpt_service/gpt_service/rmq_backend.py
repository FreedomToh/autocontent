import datetime
import json
import logging
import time

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

    def __prepare_rabbit_data(self, data: dict, _type):
        body = {
            'meta': {
                'time_send_to_mq_epoch': time.time(),
                'time_send_to_mq_stamp': datetime.datetime.utcnow().isoformat(),
            },
            'data': {
                'type': _type,
                **data
            },
        }
        return json.dumps(body).encode()

    def publish(self, data: dict) -> bool:
        logging.info(f'Rabbit adding request to queue: {data.get("request_id")}')

        need_data = {
            "request_id": data.get("request_id")
        }
        try:
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue,
                body=self.__prepare_rabbit_data(need_data, "gpt_request"),
                properties=pika.BasicProperties(delivery_mode=2, content_type='application/json')
            )
        except Exception as ex:
            logging.error(f"Rabbit add request to queue fail: {ex}")
            return False
        return True



