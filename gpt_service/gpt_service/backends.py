import logging

from rest_framework.generics import get_object_or_404

from api import models
from gpt_service.api.telegram_api import TelegramApi
from gpt_service.chat_gpt_handler import ChatGptHandler


def request_to_gpt(text: None, user_name: str = None):
    if not text:
        text = ""
    if len(text) == 0:
        logging.error("request_to_gpt fail: No text")
        return {}

    if user_name:
        user_obj = get_object_or_404(models.User, username=user_name)
    else:
        user_obj = models.User.create_user()

    # handler = ChatGptHandler(user_obj, text)
    telegram = TelegramApi()
    telegram.send("test")

