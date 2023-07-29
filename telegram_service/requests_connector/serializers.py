import logging

from asgiref.sync import sync_to_async
from rest_framework.serializers import ModelSerializer
from telegram import Update

from requests_connector import models
from requests_connector.models import User


class RequestModelSerializer(ModelSerializer):
    class Meta:
        model = models.RequestsModel
        fields = "__all__"


## Работает только синхронно
def create_task(message: Update.message, user: User):
    serializer = RequestModelSerializer(data={
        "request_src": "telegram",
        "request_text": message.text,
        "user_id": user.user_id
    })
    if not serializer.is_valid():
        logging.error(f"create_task fail: {serializer.errors}")
        return {"error": "Не удалось создать запрос"}


