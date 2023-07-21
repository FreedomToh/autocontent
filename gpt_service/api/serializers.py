from rest_framework.serializers import ModelSerializer
from api import models


class RequestModelSerializer(ModelSerializer):
    class Meta:
        model = models.RequestsModel
        fields = "__all__"
