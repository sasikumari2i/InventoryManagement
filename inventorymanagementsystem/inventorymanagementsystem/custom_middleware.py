from rest_framework_simplejwt.exceptions import InvalidToken

from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from utils.exceptionhandler import CustomException


class CustomMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            user = JWTAuthentication().authenticate(Request(request))
        except InvalidToken:
            raise CustomException(400, "Invalid Authentication Token")