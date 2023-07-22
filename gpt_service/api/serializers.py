import logging

from rest_framework.serializers import ModelSerializer
from api import models


class RequestModelSerializer(ModelSerializer):
    class Meta:
        model = models.RequestsModel
        fields = "__all__"


class RequestStatusesModelSerializer(ModelSerializer):
    class Meta:
        model = models.RequestStatusesModel
        fields = "__all__"


def get_statuses():
    mapping = {
        0: "WAITING",
        1: "INPROCESS",
        2: "READY",
        3: "DOWNLOADED",
    }
    return {mapping[elem.id]: elem for elem in models.StatusesModel.objects.all()}


def init_statuses(instance: models.RequestsModel):
    statuses_model = RequestStatusesModelSerializer(data={
        "request_id": instance.request_id
    })
    if not statuses_model.is_valid():
        logging.error(f"init_statuses fail for {instance.request_id}")
        instance.delete()
        return

    return statuses_model.save()


def change_status(instance: models.RequestsModel, statuses: dict = None,
                  gpt_status: str = None, audio_status: str = None, video_status: str = None):
    if not statuses:
        statuses = get_statuses()
    gpt_status_obj = statuses.get(gpt_status)
    audio_status_obj = statuses.get(audio_status)
    video_status_obj = statuses.get(video_status)

    statuses_instance = models.RequestStatusesModel(request_id=instance)
    if gpt_status_obj:
        statuses_instance.gpt_status = gpt_status_obj
    if audio_status_obj:
        statuses_instance.audio_status = audio_status_obj
    if video_status_obj:
        statuses_instance.video_status = video_status_obj

    statuses_instance.save()

