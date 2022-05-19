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
from .serializers import AssetSerializer, RepairingStockSerializer, RepairingStockCreateSerializer, CloseAssetSerializer
from utils.exceptionhandler import CustomException

logger = logging.getLogger('django')

class AssetView(viewsets.ModelViewSet):
    """Gives the view for the Order"""

    # queryset = Asset.objects.get_queryset().order_by('id')
    serializer_class = AssetSerializer
    lookup_field = 'asset_uid'
    asset_service = AssetService()

    def get_queryset(self):
        try:
            organisation_uid = self.request.query_params.get('organisation', None)
            if organisation_uid is None:
                raise CustomException(400, "Credentials required")
            organisation = Organisation.objects.get(organisation_uid=organisation_uid)
            assets = Asset.objects.filter(organisation_id=organisation).order_by('id')
            return assets
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(400, "Invalid Credentials")


    def create(self, request, *args, **kwargs):
        try:
            organisation_uid = request.query_params.get('organisation')
            validated_data = AssetSerializer(data=request.data)
            validated_data.is_valid(raise_exception=True)
            new_asset = self.asset_service.create(validated_data, organisation_uid)
            serialized = AssetSerializer(new_asset)
            return Response(serialized.data)
        except Asset.DoesNotExist:
            raise CustomException(400, "KeyError in Asset Creation View")

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            if not instance.is_active:
                raise CustomException(400,"Only active assets can be updated")
            customer = Customer.objects.get(customer_uid=request.data['customer'],
                                            organisation_uid=instance.organisation)
            product = Product.objects.get(product_uid=request.data['product'],
                                            organisation_uid=instance.organisation)
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
    lookup_field = 'repairing_stock_uid'
    repairing_stock_service = RepairingStockService()

    def get_queryset(self):
        try:
            organisation_uid = self.request.query_params.get('organisation', None)
            if organisation_uid is None:
                raise CustomException(400, "Credentials required")
            organisation = Organisation.objects.get(organisation_uid=organisation_uid)
            repairing_stocks = RepairingStock.objects.filter(organisation=organisation).order_by('id')
            return repairing_stocks
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(400, "Invalid Credentials")

    def create(self, request, *args, **kwargs):
        try:
            organisation_uid = request.query_params.get('organisation')
            validated_data = RepairingStockCreateSerializer(data=request.data)
            validated_data.is_valid(raise_exception=True)
            new_repairing_stock = self.repairing_stock_service.create(validated_data, organisation_uid)
            serialized = RepairingStockSerializer(new_repairing_stock)
            return Response(serialized.data)
        except RepairingStock.DoesNotExist:
            raise CustomException(400, "KeyError in Repairing Stock Creation View")

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            if not instance.is_active:
                raise CustomException(400,"Only active repairing stocks can be updated")
            asset = Asset.objects.get(asset_uid=request.data['asset'],
                                      product_uid=request.data['product'],
                                      organisation_uid=instance.organisation)
            instance.updated_date = date.today()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except Asset.DoesNotExist:
            raise CustomException(404, "Invalid Asset")


class CloseAssetView(generics.GenericAPIView):

    asset_service = AssetService()
    lookup_field = 'asset_uid'

    def get_queryset(self):
        try:
            organisation_uid = self.request.query_params.get('organisation', None)
            if organisation_uid is None:
                raise CustomException(400, "Credentials required")
            organisation = Organisation.objects.get(organisation_uid=organisation_uid)
            assets = Asset.objects.filter(organisation=organisation).order_by('id')
            return assets
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(400, "Invalid Credentials")

    def put(self, request, *args, **kwargs):
        try:
            asset_details = self.get_object()
            response = self.asset_service.close_asset(asset_details, request.data)
            return Response(response)
        except Http404:
            raise CustomException(404,"Exception in Updating Asset Status")


class CloseRepairingStockView(generics.GenericAPIView):

    repairing_stock_service = RepairingStockService()
    lookup_field = 'repairing_stock_uid'

    def get_queryset(self):
        try:
            organisation_uid = self.request.query_params.get('organisation', None)
            if organisation_uid is None:
                raise CustomException(400, "Credentials required")
            organisation = Organisation.objects.get(organisation_uid=organisation_uid)
            repairing_stocks = RepairingStock.objects.filter(organisation=organisation).order_by('id')
            return repairing_stocks
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(400, "Invalid Credentials")

    def put(self, request, *args, **kwargs):
        try:
            repairing_stock_details = self.get_object()
            response = self.repairing_stock_service.close_repairing_stock(repairing_stock_details, request.data)
            return Response(response)
        except Http404:
            raise CustomException(404,"Exception in Updating Repairing Stock Status")


class ProductAssetView(generics.ListAPIView):

    serializer_class = AssetSerializer
    lookup_field = 'product'

    def get_queryset(self):
        try:
            organisation_uid = self.request.query_params.get('organisation', None)
            if organisation_uid is None:
                raise CustomException(400, "Credentials required")
            organisation = Organisation.objects.get(organisation_uid=organisation_uid)
            assets = Asset.objects.filter(organisation=organisation).order_by('id')
            return assets
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(400, "Invalid Credentials")


    def get(self, request, *args, **kwargs):
        """Retrieves the list of Orders for the given vendor"""

        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except NotFound:
            raise CustomException(404, "Requested Orders for the Vendor is not available")

class CustomerAssetView(generics.ListAPIView):

    serializer_class = AssetSerializer
    lookup_field = 'customer'

    def get_queryset(self):
        try:
            organisation_uid = self.request.query_params.get('organisation', None)
            if organisation_uid is None:
                raise CustomException(400, "Credentials required")
            organisation = Organisation.objects.get(organisation_uid=organisation_uid)
            assets = Asset.objects.filter(organisation=organisation).order_by('id')
            return assets
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(400, "Invalid Credentials")


    def get(self, request, *args, **kwargs):
        """Retrieves the list of Orders for the given vendor"""

        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except NotFound:
            raise CustomException(404, "Requested Orders for the Vendor is not available")


class ProductRepairingStockView(generics.ListAPIView):

    serializer_class = RepairingStockSerializer
    lookup_field = 'product'

    def get_queryset(self):
        try:
            organisation_uid = self.request.query_params.get('organisation', None)
            if organisation_uid is None:
                raise CustomException(400, "Credentials required")
            organisation = Organisation.objects.get(organisation_uid=organisation_uid)
            repairing_stocks = RepairingStock.objects.filter(organisation=organisation).order_by('id')
            return repairing_stocks
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(400, "Invalid Credentials")

    def get(self, request, *args, **kwargs):
        """Retrieves the list of Orders for the given vendor"""

        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except NotFound:
            raise CustomException(404, "Requested Orders for the Vendor is not available")


class AssetRepairingStockView(generics.ListAPIView):

    serializer_class = RepairingStockSerializer
    lookup_field = 'asset'

    def get_queryset(self):
        try:
            organisation_uid = self.request.query_params.get('organisation', None)
            if organisation_uid is None:
                raise CustomException(400, "Credentials required")
            organisation = Organisation.objects.get(organisation_uid=organisation_uid)
            repairing_stocks = RepairingStock.objects.filter(organisation=organisation).order_by('id')
            return repairing_stocks
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(400, "Invalid Credentials")

    def get(self, request, *args, **kwargs):
        """Retrieves the list of Orders for the given vendor"""

        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except NotFound:
            raise CustomException(404, "Requested Orders for the Vendor is not available")