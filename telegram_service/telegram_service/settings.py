from telegram_service.configs.dev import *
from telegram_service.configs.base import *
from telegram_service.configs.database import *
from telegram_service.configs.loggs import *
#from telegram_service.configs.redis_config import *
from telegram_service.configs.rmq import *

import logging
logging.getLogger('pika').setLevel(logging.WARNING)
logging.getLogger('openai').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
