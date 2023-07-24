import dj_database_url
import os


DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

DB_URL = f'postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/requests'
DATABASES = {
    # 'default': dj_database_url.config(default=DB_URL)
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'requests',

        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': DB_HOST,
        'PORT': DB_PORT
    },
    "migrations": {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    },
}

DATABASE_ROUTERS = ["telegram_service.configs.database.DatabaseRouter"]


class DatabaseRouter:
    def db_for_schema(self, *args, **kwargs):
        return "migrations"
