import logging
import uuid

from rest_framework.generics import get_object_or_404

from api import models, serializers
from api.serializers import init_statuses
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

    statuses = get_statuses()

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
    if not (statuses_obj := init_statuses(result)):
        logging.error(f"{request_id} - fail init statuses for {user.user_id} {serializer.errors}")
        return

    statuses_obj.gpt_status = statuses.get("READY", 0)
    statuses_obj.save()
    logging.info(f"{request_id} - success result_to_database for {user.user_id}: {result.request_id}")


def request_to_gpt(text: None, user_obj: models.User):
    if not text:
        text = ""
    if len(text) == 0:
        logging.error("request_to_gpt fail: No text")
        return {"error": "no text"}

    handler = ChatGptHandler(user_obj, text)
    result = handler.ask_gpt()
    result["user"] = user_obj
    return result


def request_to_db(text: None, user: models.User, request_src: str = "base_command"):
    if not text:
        text = ""
    if len(text) == 0:
        logging.error("request_to_db fail: No text")
        return {"error": "no text"}

    request_id = uuid.uuid4()
    logging.info(f"{request_id} - start request_to_db for {user.user_id}")

    serializer = serializers.RequestModelSerializer(data={
        "request_src": request_src,
        "request_text": text,
        "user_id": user.user_id
    })
    if not serializer.is_valid():
        logging.error(f"{request_id} - fail request_to_db for {user.user_id} {serializer.errors}")
        return
    result = serializer.save()
    if not init_statuses(result):
        logging.error(f"{request_id} - fail request_to_db init statuses for {user.user_id} {serializer.errors}")
        return
    logging.info(f"{request_id} - success request_to_db for {user.user_id}: {result.request_id}")
    return {"status": "success"}

