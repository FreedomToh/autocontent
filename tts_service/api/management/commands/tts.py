from django.core.management import BaseCommand

from api.backends import run_wrapper


class Command(BaseCommand):
    help = "python manage.py tts"

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         '--command',
    #         action='store',
    #         help='User`s domain',
    #     )

    def handle(self, *args, **options):
        run_wrapper()

