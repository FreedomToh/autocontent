import asyncio
import json
import logging
import time

from django.conf import settings

from api.bot.backends import TelegramBot, send_message
from api.models import get_user_id_by_message, set_message_succeed
from requests_connector.serializers import get_message_data
from telegram_service.rmq_backend import Rabbit


def receive_message(channel, method, properties, body, args):
    message = Rabbit.decode_rabbit_data(body).get("data")
    message_id = message.get("message_id", "no message id")
    # bot_instance = args.get("bot")
    # if not bot_instance:
    #     logging.error(f"receive_message fail: no bot instance")
    #     time.sleep(5)
    #     return

    user_dict = get_user_id_by_message(message_id)
    if not user_dict:
        logging.warning(f"receive_message fail: user for message not exists {message_data}")
        channel.basic_reject(delivery_tag=method.delivery_tag, requeue=False)

    print(user_dict)
    message_data = get_message_data(message_id)

    video_url = message_data.get("video_url")
    audio_url = message_data.get("audio_url")
    text_response = message_data.get("response_text")

    # asyncio.run(bot_instance.send_text_message(chat_id=user_id, text="Вот ваш ответ:"))
    # asyncio.run(bot_instance.send_text_message(chat_id=user_id, text=text_response))
    # asyncio.run(send_message(user_id=user_id, message="Вот ваш ответ:"))

    user_id = user_dict.get("user_id")
    reply_id = user_dict.get("parent_message_id")
    asyncio.run(send_message(user_id=user_id, message=text_response, reply_to=reply_id))
    asyncio.run(send_message(user_id=user_id, message=audio_url, reply_to=reply_id))
    asyncio.run(send_message(user_id=user_id, message=video_url, reply_to=reply_id))
    set_message_succeed(message)

    # channel.basic_reject(delivery_tag=method.delivery_tag, requeue=True)
    channel.basic_ack(delivery_tag=method.delivery_tag)


def run_consumer():
    logging.info(f"Rabbit init CONSUMER")
    logging.info(f'Queue: {settings.RMQ_QUEUE}')
    logging.info(f'Exchange: {settings.RMQ_EXCHANGE}')

    bot = TelegramBot()

    rabbit = Rabbit(
        exchange=settings.RMQ_EXCHANGE,
        tank=settings.RMQ_EXCHANGE_TANK,
        queue=settings.RMQ_QUEUE,
        queue_tank=settings.RMQ_QUEUE_TANK,
        arguments=settings.RMQ_ARGS,
        tank_arguments=settings.RMQ_TANK_ARGS,
    )

    arguments = {
        'bot': bot
    }
    rabbit.bind_func(receive_message, arguments)
    try:
        rabbit.start_consuming()
    except KeyboardInterrupt:
        logging.info(f"Rabbit stopping")
        rabbit.stop_consuming()
    except Exception as ex:
        logging.error(f"Rabbit consumer fail: {ex}")
        exit()

    rabbit.close()
