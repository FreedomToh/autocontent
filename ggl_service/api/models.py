import logging
from django.db import models

nb = dict(null=True, blank=True)


class User(models.Model):
    user_id = models.PositiveBigIntegerField(primary_key=True)
    username = models.CharField(max_length=32, **nb)
    language_code = models.CharField(max_length=8, help_text="Telegram client's lang", **nb)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "requests_users"
        app_label = 'requests_connector'
        managed = False

        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.username}' if self.username is not None else f'{self.user_id}'

    @classmethod
    def create_user(cls, username=None, is_admin=False):
        logging.info("Creating user")

        new_id = 0
        if cls.objects.count() > 0:
            new_id = cls.objects.all().order_by("-user_id").first().user_id + 1

        if username:
            obj = cls(user_id=new_id, is_admin=is_admin, username=username)
        else:
            obj = cls(user_id=new_id, is_admin=is_admin)
        obj.save()
        return obj


class RequestsModel(models.Model):
    request_id = models.AutoField(primary_key=True)
    request_src = models.CharField(max_length=255)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    request_text = models.TextField(**nb)
    response_text = models.TextField(**nb)
    audio_url = models.TextField(**nb)
    video_url = models.TextField(**nb)
    finished = models.BooleanField(default=False)

    class Meta:
        db_table = "requests"
        app_label = 'requests_connector'
        managed = False


class StatusesModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "statuses"
        app_label = 'requests_connector'
        managed = False


class RequestStatusesModel(models.Model):
    request_id = models.OneToOneField(RequestsModel, on_delete=models.CASCADE, primary_key=True)
    gpt_status = models.ForeignKey(StatusesModel, related_name="gpt_status", on_delete=models.DO_NOTHING, default=0)
    audio_status = models.ForeignKey(StatusesModel, related_name="audio_status", on_delete=models.DO_NOTHING, default=0)
    video_status = models.ForeignKey(StatusesModel, related_name="video_status", on_delete=models.DO_NOTHING, default=0)

    class Meta:
        db_table = "requests_status"
        app_label = 'requests_connector'
        managed = False


def get_notloaded_requests():
    return RequestStatusesModel.objects.select_related("request_id").filter(audio_status=2)


def add_audio_link_to_request(model_obj: RequestsModel, url: str) -> bool:
    if not url:
        logging.error(f"add_audio_link_to_request fail for {model_obj.request_id}: no url")
        return False
    if len(url) == 0:
        logging.error(f"add_audio_link_to_request fail for {model_obj.request_id}: no url")
        return False

    model_obj.audio_url = url
    model_obj.save()
    return True


def set_request_audio_loaded(model_obj: RequestStatusesModel):
    model_obj.audio_status = StatusesModel.objects.get(name="Загружено")
    model_obj.save()


def set_request_in_work(model_obj: RequestStatusesModel):
    model_obj.audio_status = StatusesModel.objects.get(name="Загружается")
    model_obj.save()