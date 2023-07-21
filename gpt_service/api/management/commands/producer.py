from django.core.management import BaseCommand

from gpt_service.producer_backend import run_producer


class Command(BaseCommand):
    help = 'python manage.py producer --command run'

    def add_arguments(self, parser):
        parser.add_argument(
            '--command',
            action='store',
            help='User`s domain',
        )

    def handle(self, *args, **options):
        command = options.get("command")
        if command == "run":
            run_producer()
