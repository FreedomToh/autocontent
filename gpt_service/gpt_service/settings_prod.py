from gpt_service.configs.prod import *
from gpt_service.configs.base import *
from gpt_service.configs.database import *
from gpt_service.configs.loggs import *
from gpt_service.configs.redis_config import *
from gpt_service.configs.rmq import *

import logging
logging.getLogger('pika').setLevel(logging.WARNING)
logging.getLogger('openai').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
