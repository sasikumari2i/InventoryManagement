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

from organisations.models import Organisation
from ..orders.models import Customer
from ..orders.models import Product
from .service import AssetService, RepairingStockService
from .models import Asset, RepairingStock
from .serializers import AssetSerializer, RepairingStockSerializer, RepairingStockCreateSerializer
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
            validated_data = AssetSerializer(data=request.data)
            validated_data.is_valid(raise_exception=True)
            new_asset = self.asset_service.create(validated_data, organisation)
            serialized = AssetSerializer(new_asset)
            return Response(serialized.data)
        except Asset.DoesNotExist:
            raise CustomException(400, "KeyError in Asset Creation View")

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            customer = Customer.objects.get(id=request.data['customer'],
                                            organisation_id=instance.organisation)
            product = Product.objects.get(id=request.data['product'],
                                            organisation_id=instance.organisation)
            instance.updated_date = date.today()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except Customer.DoesNotExist:
            raise CustomException(404, "Invalid Customer")
        except Product.DoesNotExist:
            raise CustomException(404, "Invalid Product")


class RepairingStockView(viewsets.ModelViewSet):
    """Gives the view for the Order"""

    # queryset = RepairingStock.objects.get_queryset().order_by('id')
    serializer_class = RepairingStockSerializer
    repairing_stock_service = RepairingStockService()

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

    def create(self, request, *args, **kwargs):
        try:
            organisation = request.query_params.get('organisation')
            validated_data = RepairingStockCreateSerializer(data=request.data)
            validated_data.is_valid(raise_exception=True)
            new_repairing_stock = self.repairing_stock_service.create(validated_data, organisation)
            serialized = RepairingStockSerializer(new_repairing_stock)
            return Response(serialized.data)
        except RepairingStock.DoesNotExist:
            raise CustomException(400, "KeyError in Repairing Stock Creation View")

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            asset = Asset.objects.get(id=request.data['asset'],
                                      product_id=request.data['product'],
                                      organisation_id=instance.organisation)
            instance.updated_date = date.today()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except Asset.DoesNotExist:
            raise CustomException(404, "Invalid Asset")
