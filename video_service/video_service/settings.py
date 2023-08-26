import os

if os.getenv("DJANGO_PROD", False) in ["true", "True", True]:
    from video_service.configs.prod import *
else:
    from video_service.configs.dev import *

from video_service.configs.base import *
from video_service.configs.database import *
from video_service.configs.loggs import *
from video_service.configs.telegram_conf import *
from video_service.configs.rmq import *
from video_service.configs.redis_config import *
from video_service.configs.googledrive_config import *

import logging
logging.getLogger('pika').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
