import logging
import os
import sys

telegram_api_url = os.getenv("TELEGRAM_BOT")
service_name = "ggl_service"
telegram_api_clients = os.getenv("TELEGRAM_USERS", "").split(";")


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if TELEGRAM_TOKEN is None:
    logging.error("Please provide TELEGRAM_TOKEN in .env file.")
    sys.exit(1)

TELEGRAM_LOGS_CHAT_ID = os.getenv("TELEGRAM_LOGS_CHAT_ID", default=None)

