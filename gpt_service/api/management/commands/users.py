import logging

from django.core.management import BaseCommand

from api.models import User


def add_user(username, is_admin=False):
    if User.objects.filter(username=username).exists():
        logging.error(f"add_user {username} fail: already exists")
        return

    obj = User.create_user(username=username, is_admin=is_admin)
    obj.save()


class Command(BaseCommand):
    help = 'python manage.py users add backend --admin=true'

    def add_arguments(self, parser):
        parser.add_argument('command', type=str)
        parser.add_argument('username', type=str)
        parser.add_argument(
            '--admin',
            action='store',
            help='User`s domain',
        )

    def handle(self, *args, **options):
        command = options.get("command")
        username = options.get("username")
        if command == "add":
            add_user(username, is_admin=options.get("admin", False) in ["true", "True", True])


