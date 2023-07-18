import os

telegram_api_url = os.getenv("TELEGRAM_BOT")
service_name = "gpt_service"
telegram_api_clients = os.getenv("TELEGRAM_USERS", "").split(";")
