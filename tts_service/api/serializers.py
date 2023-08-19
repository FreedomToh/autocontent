from rest_framework import serializers
from api import models


class YandexTokenModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.YandexTokenModel
        fields = "__all__"


class RequestModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RequestsModel
        fields = "__all__"
