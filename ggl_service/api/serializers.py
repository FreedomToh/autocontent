from rest_framework import serializers
from api import models


class RequestModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RequestsModel
        fields = "__all__"
