import datetime
import json
import logging
import time

import pika
from django.conf import settings

from telegram_service.exceptions import RMQNoConfigError


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
        self.__binding_queue__()

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

    def __binding_queue__(self):
        self.channel.exchange_declare(exchange=self.exchange, exchange_type='fanout')
        self.channel.queue_declare(queue=self.queue, durable=True, arguments=self.arguments)
        self.channel.queue_bind(exchange=self.exchange, queue=self.queue, )

    def __binding_queue_tank__(self):
        self.channel.exchange_declare(exchange=self.exchange_tank, exchange_type='fanout')
        self.channel.queue_declare(queue=self.queue_tank, durable=True, arguments=self.tank_arguments)
        self.channel.queue_bind(exchange=self.exchange_tank, queue=self.queue_tank, )

    @classmethod
    def __prepare_rabbit_data(cls, data: dict, _type):
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

    @classmethod
    def decode_rabbit_data(cls, body: bytes):
        return json.loads(body)

    def publish(self, data: dict) -> bool:
        logging.info(f'Rabbit adding request to queue: {data}')
        try:
            self.channel.basic_publish(
                exchange=self.exchange,
                routing_key=self.queue,
                body=self.__prepare_rabbit_data(data, self.queue),
                properties=pika.BasicProperties(delivery_mode=2, content_type='application/json')
            )
        except Exception as ex:
            logging.error(f"Rabbit add request to queue fail: {ex}")
            return False
        return True

    def bind_func(self, func, args: dict = None):
        logging.info(f"Rabbit binding function to {self.queue}")
        # on_message_callback = functools.partial(func, args=args)
        self.channel.basic_consume(
            queue=self.queue,
            on_message_callback=lambda ch, method, properties, body: func(ch, method, properties, body, args),
            auto_ack=False,
        )

    def close(self):
        logging.info("Rabbit close connection")
        if self.connection.is_open:
            try:
                self.connection.close()
            except Exception as ex:
                logging.error(f"Rabbit close connection: {ex}")

    def start_consuming(self):
        logging.info("Rabbit starting consuming")
        self.channel.start_consuming()

    def stop_consuming(self):
        logging.info("Rabbit stopping consuming")
        try:
            self.channel.stop_consuming()
        except Exception as ex:
            logging.error(f"Rabbit stopping consuming: {ex}")

    def __del__(self):
        self.stop_consuming()
        self.close()



