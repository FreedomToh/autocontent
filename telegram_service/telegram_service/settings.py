import os

if os.getenv('DJANGO_PROD', False) in ["true", "True", True]:
    from telegram_service.configs.prod import *
else:
    from telegram_service.configs.dev import *

from telegram_service.configs.base import *
from telegram_service.configs.database import *
from telegram_service.configs.loggs import *
from telegram_service.configs.rmq import *
from telegram_service.configs.telegram_conf import *

import logging
logging.getLogger('pika').setLevel(logging.WARNING)
logging.getLogger('openai').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('httpcore').setLevel(logging.WARNING)
logging.getLogger('telegram').setLevel(logging.WARNING)
logging.getLogger('httpx').setLevel(logging.WARNING)
