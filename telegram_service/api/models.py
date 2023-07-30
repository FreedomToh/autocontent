import logging

from django.db import models


nb = dict(null=True, blank=True)


class TelegramUser(models.Model):
    user_id = models.PositiveBigIntegerField(primary_key=True)
    username = models.CharField(max_length=32, **nb)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, **nb)
    language_code = models.CharField(max_length=8, help_text="Telegram client's lang", **nb)

    class Meta:
        db_table = "telegram_user"


class TelegramRequests(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.DO_NOTHING)
    request = models.CharField(max_length=255)
    request_id = models.BigIntegerField(default=0)
    request_id_ext = models.BigIntegerField(default=0)
    in_work = models.BooleanField(default=False)
    status = models.BooleanField(default=False)

    class Meta:
        db_table = "telegram_request"


def get_messages_without_response():
    return TelegramRequests.objects.filter(status=False, in_work=False)


def set_message_in_work(message_dict: dict):
    message_objs = TelegramRequests.objects.filter(request_id=message_dict.get("message_id"))
    if not message_objs.exists():
        logging.error(f"set_message_in_work fail: message not exists, {message_dict}")
        return

    message = message_objs.first()
    message.in_work = True
    message.save()


def get_user_id_by_message(message_id: int) -> dict:
    user_obj = TelegramRequests.objects.filter(request_id=message_id).select_related('user')
    if not user_obj.exists():
        return None

    return {
        "user_id": user_obj.first().user_id,
        "parent_message_id": user_obj.first().request_id_ext,
    }


