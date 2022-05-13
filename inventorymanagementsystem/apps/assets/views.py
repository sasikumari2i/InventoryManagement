from rest_framework.response import Response
from rest_framework import viewsets, generics
from django.db import transaction
import logging
from datetime import date, timedelta
from rest_framework.exceptions import NotFound, APIException
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import Http404
from rest_framework import permissions, authentication
from django.contrib.auth.models import User

from .models import Asset, RepairingStock
from .serializers import AssetSerializer, RepairingStockSerializer
from utils.exceptionhandler import CustomException

logger = logging.getLogger('django')

class AssetView(viewsets.ModelViewSet):
    """Gives the view for the Order"""

    queryset = Asset.objects.all()
    serializer_class = AssetSerializer


class RepairingStockView(viewsets.ModelViewSet):
    """Gives the view for the Order"""

    queryset = RepairingStock.objects.all()
    serializer_class = RepairingStockSerializer



