from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command


def add_permissions():
    import os
    import django

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'requests_api.settings')
    django.setup()

    from django.db import connection
    sql_queries = [
        "GRANT INSERT, SELECT, UPDATE, DELETE ON requests_status TO PUBLIC;",
        "GRANT INSERT, SELECT, UPDATE, DELETE ON requests_users TO PUBLIC;",
        "GRANT INSERT, SELECT, UPDATE, DELETE ON statuses TO PUBLIC;",
        "GRANT INSERT, SELECT, UPDATE, DELETE ON requests TO PUBLIC;",
        "GRANT INSERT, SELECT, UPDATE, DELETE ON requests_request_id_seq TO PUBLIC;",
    ]
    with connection.cursor() as cursor:
        for sql_query in sql_queries:
            print(sql_query)
            cursor.execute(sql_query)


@receiver(post_migrate)
def load_fixtures(sender, **kwargs):
    # Загрузка фикстур после успешной миграции
    if kwargs.get('app', None) is None:
        call_command('loaddata', 'initial_data.json')

    if sender.name == "api":
        add_permissions()



