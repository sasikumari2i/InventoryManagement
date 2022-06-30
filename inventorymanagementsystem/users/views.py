import json
import requests
from django.contrib.auth import authenticate
from oauth2_provider.models import Application
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from oauth2_provider.contrib.rest_framework import IsAuthenticatedOrTokenHasScope
from rest_framework import viewsets
from rest_framework.response import Response

from utils.constants import SCOPE_OF_SUPERUSER, SCOPE_OF_STAFF
from utils.exceptionhandler import CustomException
from .models import User
from .serializers import UserSerializer
from .service import UserService


@api_view(['POST'])
@permission_classes((AllowAny,))
def login_user(request):
    user = authenticate(username=request.data['username'], password=request.data['password'])

    if user.is_active:
        app_obj = Application.objects.filter(user=user)
        url = 'http://' + request.get_host() + '/o/token/'
        data_dict = {
            "grant_type": "password",
            "username": request.data['username'],
            "password": request.data['password'],
            "client_id": app_obj[0].client_id,
            "scope": give_scopes_based_on_user_role(user)
        }
        token_obj = requests.post(url=url, data=data_dict)
        token_gen = json.loads(token_obj.text)
        return Response(token_gen)
    else:
        return Response({'message': "Please provide correct username and password"})


def give_scopes_based_on_user_role(user):
    scope = SCOPE_OF_STAFF
    if user.is_superuser:
        scope = SCOPE_OF_SUPERUSER
    # else:
    #     # scope = SCOPE_OF_STAFF
    #     scope = None
    return scope


class UserView(viewsets.ModelViewSet):
    """Organisation level view class for CRUD operations"""

    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    user_service = UserService()
    permission_classes = [IsAuthenticatedOrTokenHasScope]
    required_scopes = ['superuser']

    def create(self, request, *args, **kwargs):

        try:
            created_by = request.user.user_uid
            user = UserSerializer(data=request.data)
            user.is_valid(raise_exception=True)
            new_user = self.user_service.create(user, created_by, request.data['password'])
            serialized = UserSerializer(new_user)
            return Response(serialized.data)
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
