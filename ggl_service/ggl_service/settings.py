import os

if os.getenv("DJANGO_PROD", False) in ["true", "True", True]:
    from ggl_service.configs.prod import *
else:
    from ggl_service.configs.dev import *

from ggl_service.configs.base import *
from ggl_service.configs.database import *
from ggl_service.configs.loggs import *
from ggl_service.configs.telegram_conf import *
from ggl_service.configs.rmq import *
from ggl_service.configs.redis_config import *
from ggl_service.configs.googledrive_config import *

import logging
logging.getLogger('pika').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
