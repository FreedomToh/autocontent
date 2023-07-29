import dj_database_url
import os


DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# DB_URL = f'postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/requests'
DATABASES = {
    # 'default': dj_database_url.config(default=DB_URL)
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'telegram_service',

        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': DB_HOST,
        'PORT': DB_PORT
    },
    'requests': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'requests',

        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': DB_HOST,
        'PORT': DB_PORT
    },
}

DATABASE_ROUTERS = ["telegram_service.configs.database.DatabaseRouter"]


class DatabaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'requests_connector':
            return 'requests'  # Здесь указывается имя базы данных из DATABASES
        return 'default'  # Возвращайте имя базы данных по умолчанию для других моделей

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'requests_connector':
            return 'requests'  # Здесь указывается имя базы данных из DATABASES
        return 'default'  # Возвращайте имя базы данных по умолчанию для других моделей

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'requests':
            return False
        elif db == 'default':
            return app_label != 'requests_connector'
        return None
