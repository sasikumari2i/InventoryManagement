from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code

    return response


class CustomException(APIException):
    """Exception class inherited from APIException class to handle custom exceptions """

    def __init__(self, status_code, detail):
        self.detail = detail
        self.status_code = status_code

