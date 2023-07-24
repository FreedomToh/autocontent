import logging
from django.core.management import BaseCommand

from api.backends import start_bot


class Command(BaseCommand):
    help = 'python manage.py users add backend --admin=true'

    def add_arguments(self, parser):
        parser.add_argument('command', type=str)
        parser.add_argument(
            '--admin',
            action='store',
            help='User`s domain',
        )

    def handle(self, *args, **options):
        command = options.get("command")
        if command == "start":
            start_bot()


