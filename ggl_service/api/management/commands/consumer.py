from django.core.management import BaseCommand

from ggl_service.consumer_backends import run_consumer


class Command(BaseCommand):
    help = "python manage.py consumer run"

    def add_arguments(self, parser):
        parser.add_argument(
            'command',
            action='store',
            help='User`s domain',
        )

    def handle(self, *args, **options):
        command = options.get("command")
        if command == "run":
            run_consumer()
