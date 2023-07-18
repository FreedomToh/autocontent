from django.core.management import BaseCommand

from gpt_service.backends import request_to_gpt


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--text',
            action='store',
            help='User`s domain',
        )

        parser.add_argument(
            '--username',
            action='store',
            help='User`s domain',
        )

    def handle(self, *args, **options):
        if not options.get("text"):
            print("No text")
            return

        username = options.get("username")
        # if not username:
        #     username = "backend"
        request_to_gpt(options.get("text", ""), username)


