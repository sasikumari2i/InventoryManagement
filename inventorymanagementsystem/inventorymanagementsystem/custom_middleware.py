from re import sub
from django.conf import settings
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.exceptions import InvalidToken
from django.contrib.auth.middleware import AuthenticationMiddleware

from rest_framework.permissions import IsAuthenticated
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import AnonymousUser
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
    #     if user is not None:
    #         user_obj = SimpleLazyObject(lambda : user[0])
    #         print(user_obj.is_authenticated)

           # if user is None:
           #     raise

        # if user is not None:
        #     request.user = SimpleLazyObject(lambda: user)
        #print(request.user.is_authenticated)
        # print(request.user)
        # try:
        #     user = JWTAuthentication().authenticate(Request(request))
        #     print(request.user.is_authenticated)
        # except InvalidToken as exc:
        #     print("Invalid Token error")
        #     raise CustomException(400, "Inval")
