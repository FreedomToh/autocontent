import telegram
from asgiref.sync import sync_to_async

from api.models import TelegramUser


async def _acreate_user_and_return(**kwargs):
    user_object = TelegramUser(**kwargs)
    await user_object.asave()


async def afind_user_or_create(user: telegram.User) -> TelegramUser:
    user_objects = await sync_to_async(TelegramUser.objects.filter)(user_id=user.id)
    if await user_objects.aexists():
        return await user_objects.afirst()

    await _acreate_user_and_return(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        language_code=user.language_code,
    )
    return await afind_user_or_create(user)


async def afind_user_by_name(username: str) -> TelegramUser:
    user_objects = await sync_to_async(TelegramUser.objects.filter)(username=username)
    if await user_objects.aexists():
        return await user_objects.afirst()

    return None

