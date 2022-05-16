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


from .service import AssetService
from .models import Asset, RepairingStock
from .serializers import AssetSerializer, RepairingStockSerializer
from utils.exceptionhandler import CustomException

logger = logging.getLogger('django')

class AssetView(viewsets.ModelViewSet):
    """Gives the view for the Order"""

    # queryset = Asset.objects.get_queryset().order_by('id')
    serializer_class = AssetSerializer
    asset_service = AssetService()

    def get_queryset(self):
        try:
            organisation_id = self.request.query_params.get('organisation', None)
            if organisation_id is None:
                raise CustomException(400, "Credentials required")
            organisation = Organisation.objects.get(id=organisation_id)
            assets = Asset.objects.filter(organisation=organisation).order_by('id')
            return assets
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(400, "Invalid Credentials")


    def create(self, request, *args, **kwargs):
        try:
            organisation = request.query_params.get('organisation')
            request.data['organisation'] = organisation
            validated_data = AssetSerializer(data=request.data)
            validated_data.is_valid(raise_exception=True)
            new_asset = asset_service.create(validated_data)
            serialized = OrderSerializer(new_asset)
            return Response(serialized.data)
        except Asset.DoesNotExist:
            raise CustomException(400, "KeyError in Asset Creation View")


class RepairingStockView(viewsets.ModelViewSet):
    """Gives the view for the Order"""

    # queryset = RepairingStock.objects.get_queryset().order_by('id')
    serializer_class = RepairingStockSerializer

    def get_queryset(self):
        try:
            organisation_id = self.request.query_params.get('organisation', None)
            if organisation_id is None:
                raise CustomException(400, "Credentials required")
            organisation = Organisation.objects.get(id=organisation_id)
            repairing_stocks = RepairingStock.objects.filter(organisation=organisation).order_by('id')
            return repairing_stocks
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(400, "Invalid Credentials")


