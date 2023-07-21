import logging
import uuid

from rest_framework.generics import get_object_or_404

from api import models, serializers
from gpt_service.chat_gpt_handler import ChatGptHandler


def get_user_by_name(user_name: str = None):
    if user_name:
        user_obj = get_object_or_404(models.User, username=user_name)
    else:
        user_obj = models.User.create_user()

    return user_obj

def result_to_database(request: str, response: str, user: models.User, request_src: str = "base_command"):
    if len(request) == 0 or len(response) == 0:
        logging.error("Incorrect request or response")
        return

    request_id = uuid.uuid4()
    logging.info(f"{request_id} - start result_to_database for {user.user_id}")

    serializer = serializers.RequestModelSerializer(data={
        "request_src": request_src,
        "request_text": request,
        "response_text": response,
        "user_id": user.user_id
    })
    if not serializer.is_valid():
        logging.error(f"{request_id} - fail result_to_database for {user.user_id} {serializer.errors}")
        return

    result = serializer.save()
    logging.info(f"{request_id} - success result_to_database for {user.user_id}: {result.request_id}")


def request_to_gpt(text: None, user_obj: models.User):
    if not text:
        text = ""
    if len(text) == 0:
        logging.error("request_to_gpt fail: No text")
        return {}

    handler = ChatGptHandler(user_obj, text)
    result = handler.ask_gpt()
    result["user"] = user_obj
    return result

