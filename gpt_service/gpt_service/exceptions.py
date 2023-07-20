from rest_framework.renderers import JSONRenderer
from rest_framework.views import exception_handler

from gpt_service.api.telegram_api import TelegramApi


def core_exception_handler(exc, context):
    response = exception_handler(exc, context)
    handlers = {
        'ValidationError': _handle_generic_error,
        'AuthenticationFailed': _handle_generic_error
    }
    exception_class = exc.__class__.__name__
    exception_path = context.get("request").get_full_path()
    message = f"gpt_service. Exception: {exception_class} in {exception_path}"
    api = TelegramApi()
    api.send(message)

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)

    return response


def _handle_generic_error(exc, context, response):
    # Это самый простой обработчик исключений, который мы можем создать. Берём ответ и рендерим его.

    renderer = JSONRenderer()
    response.data = renderer.render(response.data)

    return response


class NoDbNameException(Exception):
    """Django is somehow improperly configured"""
    pass


class FailRequestsResponse(Exception):
    """Django is somehow improperly configured"""
    pass


class RMQNoConfigError(Exception):
    """Django is somehow improperly configured"""
    pass

