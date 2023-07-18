import logging

import requests
from django.core.cache import cache

from gpt_service.configs.gpt import *

from api.models import User


dialog_template = {'dialog': [{"role": "system", "content": 'Ты полезный'}], 'total_tokens': 0}


class ChatGptHandler:
    user: User = None

    message = ""
    dialog = dialog_template

    redis = False
    redis_dialog_key = ""

    def __init__(self, u: User, message: str):
        self.message = message
        if not User:
            raise TypeError("No user")

        self.user = u
        self.init_redis()
        self.get_dialog_history()

    def get_dialog_history(self):
        self.redis_dialog_key = f"dialogs-{self.user.user_id}"
        if self.redis:
            self.dialog = cache.get(self.redis_dialog_key, dialog_template)
            if not isinstance(self.dialog, dict):
                self.dialog = dialog_template
            if self.dialog.get("total_tokens") >= OPENAI_CHAT_MAX_TOKENS:
                self.dialog = dialog_template
                cache.set(self.redis_dialog_key, dialog_template, CHAT_HISTORY_LIFETIME)
        else:
            logging.warning("ChatGptHandler get_dialog_history: no caching init, dialogs wouldn`t be save")
            self.dialog = dialog_template

    def update_history(self):
        if self.redis:
            print("updating", self.redis_dialog_key, self.dialog)
            cache.set(self.redis_dialog_key, self.dialog, CHAT_HISTORY_LIFETIME)

    def init_redis(self):
        cache.set("ping", "pong", 1000)
        if cache.get("ping"):
            self.redis = True

    def ask_gpt(self) -> dict:
        if len(self.message) == 0:
            return {"error": "Yoy asked nothing..."}
        if not self.user:
            return {"error": "No user"}

        dialog = self.dialog.get("dialog", [])
        dialog.append(
            {"role": "user", "content": self.message}
        )

        try:
            response = openai.ChatCompletion.create(
                model=OPENAI_CHAT_MODEL,
                messages=dialog,
                max_tokens=OPENAI_CHAT_MAX_TOKENS,
                temperature=OPENAI_CHAT_TEMPERATURE,
                stop=None,
                timeout=OEPNAI_CHAT_TIMEOUT
            )
        except Exception as ex:
            print(ex)
            return {"error": "Quota ended"}

        if "choices" not in response:
            logging.error(f"Fail request: ", response)
            return {"error": "Couldn`t connect to ChatGPT"}

        bot_message = response.choices[0].message.content
        dialog.append(
            {"role": "assistant", "content": bot_message}
        )

        self.dialog["dialog"] = dialog
        self.dialog["total_tokens"] += response.usage.completion_tokens

        self.update_history()
        return {
            "message": bot_message,
            "tokens": f'{self.dialog["total_tokens"]}/{OPENAI_CHAT_MAX_TOKENS}'
        }
