from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from datetime import date, timedelta
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth.models import User
from rest_framework import permissions, authentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from utils.exceptionhandler import CustomException
from .models import Organisation
from .serializers import OrganisationSerializer

# Create your views here.

class OrganisationView(viewsets.ModelViewSet):
    """Gives the view for the Product"""

    queryset = Organisation.objects.order_by('id')
    lookup_field = 'organisation_uid'
    serializer_class = OrganisationSerializer