import os
import openai

openai.organization = os.getenv("OPENAI_ORG_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

OPENAI_CHAT_MODEL = 'gpt-3.5-turbo'
# OPENAI_CHAT_MODEL = 'gpt-4'
OPENAI_CHAT_MAX_TOKENS = 500
OPENAI_CHAT_TEMPERATURE = 0.8
OEPNAI_CHAT_TIMEOUT = 30
CHAT_HISTORY_LIFETIME = 324000
openai.Model.list()
