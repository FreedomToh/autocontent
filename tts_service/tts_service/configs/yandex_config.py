import os

YANDEX_SERVER = "https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize"
YANDEX_GET_TOKEN_URL = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
YANDEX_METHOD = "POST"
YANDEX_MAX_LENGTH = "150KB"

YANDEX_OAUTH_TOKEN = os.getenv("YANDEX_OAUTH_TOKEN")
YANDEX_FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")
YANDEX_DIR_PATH = os.getenv("YANDEX_DIR_PATH")
#YANDEX_OAUTH_TOKEN = 'y0_AgAEA7qiqhfsAATuwQAAAADeeo8rjmJa7HT5SMC0bybqtYBzP6uNZ8w'
#YANDEX_IAM_TOKEN = "t1.9euelZqOkc-OicqKl5KayIqZmJvPyu3rnpWalo6TkJCey4-djMaVzJqdy4vl8_d_dhNc-e98FzJU_d3z9z8lEVz573wXMlT9zef1656VmsqZk8mZlZ7PyomNkMael8vO7_zF656VmsqZk8mZlZ7PyomNkMael8vO.rzOUjGOBk_hWVdxGwZjY9htZVTxisqyWv7maOR35scthwCJA5HzGYAJ0q1bVFAnLrYo5Viih14e20jD9mniLDA"
#YANDEX_FOLDER_ID = 'b1gmb97oud37sqteth3r'
