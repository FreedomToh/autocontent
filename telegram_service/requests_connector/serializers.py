import logging

from rest_framework.serializers import ModelSerializer

from requests_connector import models


class RequestModelSerializer(ModelSerializer):
    class Meta:
        model = models.RequestsModel
        fields = "__all__"


def get_message_data(request_id: int) -> dict:
    request_obj = models.RequestsModel.objects.filter(request_id=request_id)
    if not request_obj.exists():
        logging.warning(f"get_message_data fail: message with id {request_id} not exists")
        return {}

    serializer = RequestModelSerializer(request_obj.first())
    return serializer.data


