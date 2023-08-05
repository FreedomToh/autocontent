import os
if os.getenv('DJANGO_PROD', False) in ["true", "True", True]:
    from requests_api.configs.prod import *
else:
    from requests_api.configs.dev import *

from requests_api.configs.base import *
from requests_api.configs.database import *
from requests_api.configs.loggs import *

import logging
logging.getLogger('pika').setLevel(logging.WARNING)
logging.getLogger('openai').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
