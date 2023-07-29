import telegram
from asgiref.sync import sync_to_async

from api.models import TelegramUser


def _create_user_and_return(**kwargs):
    user_object = TelegramUser(**kwargs)
    user_object.asave()


def find_user_or_create(user: telegram.User) -> TelegramUser:
    user_objects = TelegramUser.objects.filter(user_id=user.id)
    if user_objects.exists():
        return user_objects.first()

    _create_user_and_return(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        language_code=user.language_code,
    )
    return find_user_or_create(user)


def find_user_by_name(username: str) -> TelegramUser:
    user_objects = TelegramUser.objects.filter(username=username)
    if user_objects.exists():
        return user_objects.first()

    return None



