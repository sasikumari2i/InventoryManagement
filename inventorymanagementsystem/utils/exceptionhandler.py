from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException


def custom_exception_handler(exc, context):
    handlers = {
        "Http404" : _handle_generic_error,
    }

    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code
        response.data['message'] = response.data['detail']
        del response.data['detail']

    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc,response)
    return response


class CustomException(APIException):
    def __init__(self, status_code, detail):
        self.detail = detail
        self.status_code = status_code


def _handle_generic_error(exception, response):
    response.data['message'] = "The request page is not found"
    return response