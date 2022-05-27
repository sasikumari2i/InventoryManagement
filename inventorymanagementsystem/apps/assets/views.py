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
from ..orders.models import Customer, Product
from .service import AssetService, RepairingStockService
from .models import Asset, RepairingStock
from .serializers import (
    AssetSerializer,
    RepairingStockSerializer,
    RepairingStockCreateSerializer,
    CloseAssetSerializer,
)
from utils.exceptionhandler import CustomException

logger = logging.getLogger("django")


class AssetView(viewsets.ModelViewSet):
    """Gives the view for the Asset"""

    serializer_class = AssetSerializer
    lookup_field = "asset_uid"
    asset_service = AssetService()

    def get_queryset(self):
        """Query Set for the getting Asset"""

        try:
            organisation_uid = self.request.query_params.get("organisation", None)
            if organisation_uid is None:
                raise CustomException(400, "Credentials required")
            organisation = Organisation.objects.get(organisation_uid=organisation_uid)
            assets = Asset.objects.filter(organisation_id=organisation).order_by("id")
            return assets
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(400, "Invalid Credentials")

    def create(self, request, *args, **kwargs):
        """To create new Asset"""

        try:
            organisation_uid = request.query_params.get("organisation")
            validated_data = AssetSerializer(data=request.data)
            validated_data.is_valid(raise_exception=True)
            new_asset = self.asset_service.create(validated_data.data, organisation_uid)
            serialized = AssetSerializer(new_asset)
            return Response(serialized.data)
        except Asset.DoesNotExist:
            raise CustomException(400, "KeyError in Asset Creation View")

    def update(self, request, *args, **kwargs):
        """To update the given Asset"""

        try:
            partial = kwargs.pop("partial", False)
            instance = self.get_object()
            asset = self.asset_service.update(instance, request.data)
            serializer = self.get_serializer(asset, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except KeyError:
            raise CustomException(400, "Product and Customer is mandatory for updating")


class RepairingStockView(viewsets.ModelViewSet):
    """Gives the view for the Repairing Stock"""

    serializer_class = RepairingStockSerializer
    lookup_field = "repairing_stock_uid"
    repairing_stock_service = RepairingStockService()

    def get_queryset(self):
        """Query Set for Repairing Stock"""

        try:
            organisation_uid = self.request.query_params.get("organisation", None)
            if organisation_uid is None:
                raise CustomException(400, "Credentials required")
            organisation = Organisation.objects.get(organisation_uid=organisation_uid)
            repairing_stocks = RepairingStock.objects.filter(
                organisation=organisation
            ).order_by("id")
            return repairing_stocks
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(400, "Invalid Credentials")

    def create(self, request, *args, **kwargs):
        """To create new Repairing Stock"""

        try:
            organisation_uid = request.query_params.get("organisation")
            validated_data = RepairingStockCreateSerializer(data=request.data)
            validated_data.is_valid(raise_exception=True)
            new_repairing_stock = self.repairing_stock_service.create(
                validated_data.data, organisation_uid
            )
            serialized = RepairingStockSerializer(new_repairing_stock)
            return Response(serialized.data)
        except RepairingStock.DoesNotExist:
            raise CustomException(400, "KeyError in Repairing Stock Creation View")

    def update(self, request, *args, **kwargs):
        """To Update the given Repairing Stock"""

        try:
            partial = kwargs.pop("partial", False)
            instance = self.get_object()
            repairing_stock = self.repairing_stock_service.update(
                instance, request.data
            )
            serializer = self.get_serializer(
                repairing_stock, data=request.data, partial=partial
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except ValidationError:
            raise CustomException(404, "Exception in Updating Repairing Stocks")


class CloseAssetView(generics.GenericAPIView):
    """Gives the Generic Api view for Closing the Asset"""

    serializer_class = CloseAssetSerializer
    asset_service = AssetService()
    lookup_field = "asset_uid"

    def get_queryset(self):
        """Query Set for the getting Asset"""

        try:
            organisation_uid = self.request.query_params.get("organisation", None)
            if organisation_uid is None:
                raise CustomException(400, "Credentials required")
            organisation = Organisation.objects.get(organisation_uid=organisation_uid)
            assets = Asset.objects.filter(organisation=organisation).order_by("id")
            return assets
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(400, "Invalid Credentials")

    def put(self, request, *args, **kwargs):
        """Updates Status for the Asset"""

        try:
            asset_details = self.get_object()
            response = self.asset_service.close_asset(asset_details, request.data)
            return Response(response)
        except Http404:
            raise CustomException(404, "Exception in Updating Asset Status")


class CloseRepairingStockView(generics.GenericAPIView):
    """Gives the Generic Api view for Closing the Repairing Stock"""

    serializer_class = RepairingStockCreateSerializer
    repairing_stock_service = RepairingStockService()
    lookup_field = "repairing_stock_uid"

    def get_queryset(self):
        """Query Set for the getting Repairing Stock"""

        try:
            organisation_uid = self.request.query_params.get("organisation", None)
            if organisation_uid is None:
                raise CustomException(400, "Credentials required")
            organisation = Organisation.objects.get(organisation_uid=organisation_uid)
            repairing_stocks = RepairingStock.objects.filter(
                organisation=organisation
            ).order_by("id")
            return repairing_stocks
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(400, "Invalid Credentials")

    def put(self, request, *args, **kwargs):
        """Updates Status for the Repairing Stock"""

        try:
            repairing_stock_details = self.get_object()
            response = self.repairing_stock_service.close_repairing_stock(
                repairing_stock_details, request.data
            )
            return Response(response)
        except Http404:
            raise CustomException(404, "Exception in Updating Repairing Stock Status")


class ProductAssetView(generics.ListAPIView):
    """Gives the view for getting Assets based on given Product"""

    serializer_class = AssetSerializer
    lookup_field = "product"

    def get_queryset(self):
        """Query Set for the getting Assets"""

        try:
            organisation_uid = self.request.query_params.get("organisation", None)
            if organisation_uid is None:
                raise CustomException(400, "Credentials required")
            organisation = Organisation.objects.get(organisation_uid=organisation_uid)
            assets = Asset.objects.filter(organisation=organisation).order_by("id")
            return assets
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(400, "Invalid Credentials")

    def get(self, request, *args, **kwargs):
        """Retrieves the list of assets for the given product"""

        try:
            organisation = self.request.query_params.get("organisation", None)
            product_id = self.kwargs["product"]
            assets = Asset.objects.filter(
                product=product_id, organisation_id=organisation
            )
            serialized = AssetSerializer(assets, many=True)
            return Response(serialized.data)
        except NotFound:
            raise CustomException(
                404, "Requested Assets for the Product is not available"
            )


class CustomerAssetView(generics.ListAPIView):
    """Gives the view for getting Assets based on given Customer"""

    serializer_class = AssetSerializer
    lookup_field = "customer"

    def get_queryset(self):
        """Query Set for the getting Assets"""

        try:
            organisation_uid = self.request.query_params.get("organisation", None)
            if organisation_uid is None:
                raise CustomException(400, "Credentials required")
            organisation = Organisation.objects.get(organisation_uid=organisation_uid)
            assets = Asset.objects.filter(organisation=organisation).order_by("id")
            return assets
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(400, "Invalid Credentials")

    def get(self, request, *args, **kwargs):
        """Retrieves the list of Assets for the given Customer"""

        try:
            organisation = self.request.query_params.get("organisation", None)
            customer_id = self.kwargs["customer"]
            assets = Asset.objects.filter(
                customer=customer_id, organisation_id=organisation
            )
            serialized = AssetSerializer(assets, many=True)
            return Response(serialized.data)
        except NotFound:
            raise CustomException(
                404, "Requested Assets for the Customer is not available"
            )


class ProductRepairingStockView(generics.ListAPIView):
    """Gives the view for getting Repairing Stocks based on given Product"""

    serializer_class = RepairingStockSerializer
    lookup_field = "product"

    def get_queryset(self):
        """Query Set for the getting Repairing Stock"""

        try:
            organisation_uid = self.request.query_params.get("organisation", None)
            if organisation_uid is None:
                raise CustomException(400, "Credentials required")
            organisation = Organisation.objects.get(organisation_uid=organisation_uid)
            repairing_stocks = RepairingStock.objects.filter(
                organisation=organisation
            ).order_by("id")
            return repairing_stocks
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(400, "Invalid Credentials")

    def get(self, request, *args, **kwargs):
        """Retrieves the list of Repairing Stocks
           for the given product"""

        try:
            organisation = self.request.query_params.get("organisation", None)
            product_id = self.kwargs["product"]
            repairing_stocks = RepairingStock.objects.filter(
                product=product_id, organisation_id=organisation
            )
            serialized = RepairingStockSerializer(repairing_stocks, many=True)
            return Response(serialized.data)
        except NotFound:
            raise CustomException(
                404, "Requested Repairing Stocks for the Product is not available"
            )


class AssetRepairingStockView(generics.ListAPIView):
    """Gives the view for getting Repairing Stocks based on given Assets"""

    serializer_class = RepairingStockSerializer
    lookup_field = "asset"

    def get_queryset(self):
        """Query Set for the getting Repairing Stock"""

        try:
            organisation_uid = self.request.query_params.get("organisation", None)
            if organisation_uid is None:
                raise CustomException(400, "Credentials required")
            organisation = Organisation.objects.get(organisation_uid=organisation_uid)
            repairing_stocks = RepairingStock.objects.filter(
                organisation=organisation
            ).order_by("id")
            return repairing_stocks
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(400, "Invalid Credentials")

    def get(self, request, *args, **kwargs):
        """Retrieves the list of Repairing stocks
           for the given asset"""

        try:
            organisation = self.request.query_params.get("organisation", None)
            asset_id = self.kwargs["asset"]
            repairing_stocks = RepairingStock.objects.filter(
                asset=asset_id, organisation_id=organisation
            )
            serialized = RepairingStockSerializer(repairing_stocks, many=True)
            return Response(serialized.data)
        except NotFound:
            raise CustomException(
                404, "Requested Repairing stock for the asset is not available"
            )
