from requests_api.configs.prod import *
from requests_api.configs.base import *
from requests_api.configs.database import *
from requests_api.configs.loggs import *
from requests_api.configs.redis_config import *
from requests_api.configs.rmq import *

import logging
logging.getLogger('pika').setLevel(logging.WARNING)
logging.getLogger('openai').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
