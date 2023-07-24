from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command


@receiver(post_migrate)
def load_fixtures(sender, **kwargs):
    # Загрузка фикстур после успешной миграции
    if kwargs.get('app', None) is None:
        call_command('loaddata', 'initial_data.json')
