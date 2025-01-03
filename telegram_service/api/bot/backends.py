import logging
import os

import django
import telegram
from django.conf import settings

from api import backends_acync
from api.backends_acync import afind_user_by_name
from requests_connector import models as request_models
from requests_connector.models import create_task

# settings.TELEGRAM_TOKEN

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telegram_service.settings')
django.setup()

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler
from telegram.ext import filters


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "Данный бот является обёрткой для сервиса Автоконтента,"
    message = f"{message} который формирует ваш запрос к ChatGpt и возвращает ответ в текстовом виде,"
    message = f"{message} в виде аудио и видео-файлов. Просто напишите вопрос!"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


async def wrap_message_send(update: Update, context: ContextTypes.DEFAULT_TYPE, message: dict):
    if not message:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Возникла ошибка")
    elif "message" in message:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message.get("message"))
    elif "error" in message:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message.get("error", "Возникла ошибка"))
    else:
        logging.warning(f"Incorrect data in message: {message}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Возникла ошибка")


async def free_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_obj = await backends_acync.afind_user_or_create(update.message.from_user)
    request_user = await request_models.find_user_or_create(update.message.from_user)
    logging.info(f"Request for user {user_obj.user_id} ({request_user}): {update.message.text} ")
    message = await create_task(update.message, request_user)
    if not await backends_acync.track_request(update.message, user_obj, message.get("message_id")):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Возникла ошибка")
        return

    await wrap_message_send(update, context, message)


async def with_attachment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Вложения пока не поддерживаются")


async def send_message(user_id: int, message: str, reply_to: int = None):
    async with (bot := telegram.Bot(settings.TELEGRAM_TOKEN)):
        if not reply_to or reply_to == 0:
            await bot.send_message(text=message, chat_id=user_id)
        else:
            await bot.send_message(text=message, chat_id=user_id, reply_to_message_id=reply_to)


async def make_message_to_user(username: str, message: str, reply_to: int = None):
    user = await afind_user_by_name(username)
    if not user:
        logging.error("User not found")
        return
    if len(message) == 0:
        logging.error("No message")
        return
    async with (bot := telegram.Bot(settings.TELEGRAM_TOKEN)):
        if not reply_to or reply_to == 0:
            await bot.send_message(text=message, chat_id=user.user_id)
        else:
            await bot.send_message(text=message, chat_id=user.user_id, reply_to_message_id=reply_to)


def start_bot():
    application = ApplicationBuilder().token(settings.TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), free_message))
    application.add_handler(MessageHandler(filters.ATTACHMENT & (~filters.COMMAND), with_attachment))
    application.run_polling()


class SingletonMetaclass(type):
    _instances = {}

    def __call(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class TelegramBot(metaclass=SingletonMetaclass):
    token = None
    bot = None

    def __init__(self, token: str = settings.TELEGRAM_TOKEN):
        self.bot = telegram.Bot(token)

    async def send_text_message(self, chat_id, text):
        await self.bot.send_message(chat_id=chat_id, text=text)

