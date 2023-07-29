import logging

from asgiref.sync import sync_to_async
from django.db import models

import telegram
from telegram import Update

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
        managed = False


class StatusesModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "statuses"
        managed = False


class RequestStatusesModel(models.Model):
    request_id = models.OneToOneField(RequestsModel, on_delete=models.CASCADE, primary_key=True)
    gpt_status = models.ForeignKey(StatusesModel, related_name="gpt_status", on_delete=models.DO_NOTHING, default=0)
    audio_status = models.ForeignKey(StatusesModel, related_name="audio_status", on_delete=models.DO_NOTHING, default=0)
    video_status = models.ForeignKey(StatusesModel, related_name="video_status", on_delete=models.DO_NOTHING, default=0)

    class Meta:
        db_table = "requests_status"
        managed = False


async def _create_user_and_return(**kwargs):
    user_object = User(**kwargs)
    await user_object.asave()


async def find_user_or_create(user: telegram.User, create=True) -> User:
    user_objects = await sync_to_async(User.objects.filter)(username=user.username)
    if await user_objects.aexists():
        return await user_objects.afirst()

    if not create:
        return None

    await _create_user_and_return(
        user_id=user.id,
        username=user.username,
        language_code=user.language_code,
    )
    return await find_user_or_create(user)


async def create_task(message: Update.message, user: User) -> dict:
    if not await find_user_or_create(user, create=False):
        logging.warning(f"models create_task fail: user {User.user_id} doesn`t exists")
        return {"error": "Не найден пользователь"}

    text_max_length = RequestsModel._meta.get_field("request_src").max_length
    if len(message.text) > text_max_length:
        return {"error": f"Превышена максимальная длина запроса в {text_max_length} символов"}

    request_object = RequestsModel(
        request_src="telegram",
        request_text=message.text,
        user_id=user
    )
    await request_object.asave()
    return {"status": "Запрос добавлен в обработку"}
