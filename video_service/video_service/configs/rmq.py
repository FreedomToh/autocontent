import os

RMQ_HOST = os.getenv("RMQ_HOST")
RMQ_LOGIN = os.getenv("RMQ_LOGIN")
RMQ_PASSWORD = os.getenv("RMQ_PASSWORD")

# ограничивает количество неподтвержденных сообщений, которые могут быть использованы
RMQ_PREFETCH_COUNT = 10
RMQ_PREFETCH_GLOBAL = False  # true - для всего канала, false - для каждого потребителя
RMQ_PRODUCER_SLEEP = 1

RMQ_EXCHANGE = "video_service_exchange"
RMQ_EXCHANGE_TANK = "video_service_exchange_tank"

RMQ_QUEUE = "video_service"
RMQ_QUEUE_TANK = "video_service_tank"

RMQ_ARGS = {
    'x-dead-letter-exchange': RMQ_EXCHANGE_TANK,
}
RMQ_TANK_ARGS = {
    'x-message-ttl': 10000,
    'x-dead-letter-exchange': RMQ_EXCHANGE,
}
