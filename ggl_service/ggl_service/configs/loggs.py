import os

LOG_PATH = os.getenv("LOG_PATH", "./logs/")
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'filters': {
        'warning': {
            '()': 'ggl_service.configs.loggs.WarningFilter',
        },
        'debug': {
            '()': 'ggl_service.configs.loggs.DebugFilter',
        },
        'info': {
            '()': 'ggl_service.configs.loggs.InfoFilter',
        },
        'error': {
            '()': 'ggl_service.configs.loggs.ErrorFilter',
        },
        # 'require_debug_true': {
        #     '()': 'django.utils.log.RequireDebugTrue',
        # },
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'DEBUG': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': f'{LOG_PATH}api-DEBUG.log',
            'formatter': 'file',
            'filters': ['debug']
        },
        'WARNING': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': f'{LOG_PATH}api-WARNING.log',
            'formatter': 'file',
            'filters': ['warning']
        },
        'INFO': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': f'{LOG_PATH}api-INFO.log',
            'formatter': 'file',
            'filters': ['info']
        },
        'ERROR': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': f'{LOG_PATH}api-ERROR.log',
            'formatter': 'file',
            'filters': ['error']
        },
    },

    'loggers': {
        '': {
            'level': LOG_LEVEL,
            'handlers': ['console', 'DEBUG', "WARNING", "INFO", "ERROR"]
        },
        'django.request': {
            'level': "ERROR",
            'handlers': ['console', 'DEBUG', "WARNING", "INFO", "ERROR"]
        }
    }
}


class WarningFilter:
    def filter(self, record):
        return record.levelname == "WARNING"


class DebugFilter:
    def filter(self, record):
        return record.levelname == "DEBUG"


class InfoFilter:
    def filter(self, record):
        return record.levelname == "INFO"


class ErrorFilter:
    def filter(self, record):
        return record.levelname == "ERROR" or record.levelname == "CRITICAL"
