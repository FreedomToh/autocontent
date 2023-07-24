import datetime

from django.utils import timezone
from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from dtb.chat_gpt_handler import ChatGptHandler
from dtb.tts_api import TtsApi
from tgbot.handlers.onboarding import static_text
from tgbot.handlers.utils.info import extract_user_data_from_update
from users.models import User
from tgbot.handlers.onboarding.keyboards import make_keyboard_for_start_command


def command_start(update: Update, context: CallbackContext) -> None:
    u, created = User.get_user_and_created(update, context)

    if created:
        text = static_text.start_created.format(first_name=u.first_name)
    else:
        text = static_text.start_not_created.format(first_name=u.first_name)

    # update.message.reply_text(text=text,
    #                           reply_markup=make_keyboard_for_start_command())
    update.message.reply_text(text=text,
                              reply_markup=None)


def secret_level(update: Update, context: CallbackContext) -> None:
    # callback_data: SECRET_LEVEL_BUTTON variable from manage_data.py
    """ Pressed 'secret_level_button_text' after /start command"""
    user_id = extract_user_data_from_update(update)['user_id']
    text = static_text.unlock_secret_room.format(
        user_count=User.objects.count(),
        active_24=User.objects.filter(updated_at__gte=timezone.now() - datetime.timedelta(hours=24)).count()
    )

    context.bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML
    )


def common_texting_return(update: Update, context: CallbackContext) -> None:
    u, created = User.get_user_and_created(update, context)

    user_message = update.message.text
    gpt = ChatGptHandler(u, user_message)
    update.message.reply_text(text="Ожидаю ответа...",
                              reply_markup=None)
    answer = gpt.ask_gpt()
    if "message" not in answer:
        update.message.reply_text(text=f"Не удалось преобразовать текст в речь :( Вот ошибка: {answer.get('error')}",
                                  reply_markup=None)
        return
    tts_api = TtsApi()
    result = tts_api.text_to_speech(answer.get("message"))
    if "url" in result:
        update.message.reply_text(
            text=result.get("url"), reply_markup=None)
    else:
        update.message.reply_text(
            text="Не удалось сформировать аудизапись. Держи текстом:", reply_markup=None)
    update.message.reply_text(
        text=f'{answer.get("message")}\nТокены {answer.get("tokens")}', reply_markup=None)
