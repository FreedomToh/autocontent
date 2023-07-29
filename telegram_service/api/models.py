from django.db import models

from requests_connector.models import nb


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
    status = models.BooleanField(default=False)

    class Meta:
        db_table = "telegram_request"


