import os

if os.getenv("DJANGO_PROD", False) in ["true", "True", True]:
    from tts_service.configs.prod import *
else:
    from tts_service.configs.dev import *

from tts_service.configs.base import *
from tts_service.configs.database import *
from tts_service.configs.loggs import *
from tts_service.configs.telegram_conf import *
from tts_service.configs.rmq import *
from tts_service.configs.yandex_config import *
from tts_service.configs.redis_config import *

import logging
logging.getLogger('pika').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
