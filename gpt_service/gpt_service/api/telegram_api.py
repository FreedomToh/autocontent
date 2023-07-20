import requests

from gpt_service.configs import telegram_conf


class TelegramApi:
    service_name = "Default"
    telegram_config = {
        "name": "telegram",
        "link": f"https://api.telegram.org/{telegram_conf.telegram_api_url}/sendMessage",
        "clients": telegram_conf.telegram_api_clients
    }

    def __init__(self):
        if telegram_conf.service_name and len(str(telegram_conf.service_name)) > 0:
            self.service_name = telegram_conf.service_name

    def send(self, msg):
        clients = self.telegram_config.get("clients")
        link = self.telegram_config.get("link")
        msg = f"{self.service_name} {msg}"

        for elem in clients:
            to_send = {
                'chat_id': elem,
                'text': msg,
                'disable_notification': 'true'
            }

            try:
                requests.post(link, json=to_send, timeout=10.001)
            except requests.exceptions.RequestException as ex:
                print("Message not sent. Nothing save us.: ", ex)
