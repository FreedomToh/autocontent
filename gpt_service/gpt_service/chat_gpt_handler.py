import logging

import requests

from gpt_service.configs.gpt import *

from api.models import User


class ChatGptHandler:
    message = ""

    user: User = None

    def __init__(self, u: User, message: str):
        self.message = message
        if not User:
            raise TypeError("No user")

        self.user = u
        # if u.gpt_tokens >= OPENAI_CHAT_MAX_TOKENS:
        #     gpt_dialogs.update(
        #         {u.user_id: {'dialog': [{"role": "system", "content": 'Ты полезный'}], 'total_tokens': 0}}
        #     )

    def check_redis(self):
        pass

    def ask_gpt(self) -> dict:
        if len(self.message) == 0:
            return {"error": "Yoy asked nothing..."}
        if not self.user:
            return {"error": "No user"}

        return

        if not gpt_dialogs.get(self.user.user_id):
            gpt_dialogs[self.user.user_id] = {'dialog': [{"role": "system", "content": 'Ты полезный'}], 'total_tokens': 0}
        gpt_dialogs.get(self.user.user_id).get('dialog').append(
            {"role": "user", "content": self.message}
        )
        dialog = gpt_dialogs.get(self.user.user_id).get("dialog", [])
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
            return {"error": "Couldn`t connect with ChatGPT"}
        bot_message = response.choices[0].message.content

        total_tokens = gpt_dialogs.get(self.user.user_id).get(
            'total_tokens') + response.usage.completion_tokens
        gpt_dialogs.get(self.user.user_id).update({'total_tokens': total_tokens})
        gpt_dialogs.get(self.user.user_id).get('dialog').append({"role": "assistant", "content": bot_message})
        return {
            "message": bot_message,
            "tokens": f"{total_tokens}/{OPENAI_CHAT_MAX_TOKENS}"
        }
