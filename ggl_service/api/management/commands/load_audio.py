from django.core.management import BaseCommand

from api.backends import load_audio_wrapper


class Command(BaseCommand):
    help = "python manage.py load_audio"

    def handle(self, *args, **options):
        load_audio_wrapper()
