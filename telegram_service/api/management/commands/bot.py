import asyncio
import logging
from django.core.management import BaseCommand

from api.bot.backends import start_bot, make_message_to_user


class Command(BaseCommand):
    help = 'python manage.py bot start'

    def add_arguments(self, parser):
        parser.add_argument('command', type=str)
        parser.add_argument(
            '--username',
            action='store',
            help='User`s domain',
        )
        parser.add_argument(
            '--message',
            action='store',
            help='User`s domain',
        )

    def handle(self, *args, **options):
        command = options.get("command")
        username = options.get("username")
        message = options.get("message")

        if command == "start":
            start_bot()
        elif command == "message" and username and message:
            asyncio.run(make_message_to_user(username, message))




