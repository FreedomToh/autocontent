import logging

from django.core.management import BaseCommand

from gpt_service.backends import request_to_gpt, result_to_database, get_user_by_name, request_to_db


class Command(BaseCommand):
    help = 'python manage.py request --text "Расскажи анекдот" --username backend --save True --now=True'

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

        parser.add_argument(
            '--now',
            action='store',
            help='Get answer immediatley',
        )

        parser.add_argument(
            '--save',
            action='store',
            help='User`s domain',
        )

    def handle(self, *args, **options):
        if not options.get("text"):
            logging.error("requests command fail: no text")
            return

        user = get_user_by_name(options.get("username"))

        if options.get("now", False) in ["true", "True", True]:
            result = request_to_gpt(options.get("text", ""), user)
        else:
            request_to_db(options.get("text", ""), user)
            return
        if "error" in result:
            logging.error(f"requests command fail: {result}")
            return
        if options.get("save", False) in ["true", "True", True]:
            result_to_database(
                request=options.get("text", ""),
                response=result.get("message", ""),
                user=user
            )



