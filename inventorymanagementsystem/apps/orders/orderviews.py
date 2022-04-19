from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from django.db import transaction
import logging
from rest_framework.exceptions import APIException
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from .models import Order,Customer,OrderProduct,Product, Vendor
from .service import OrderService
from .serializers import OrderSerializer, OrderProductSerializer,CustomerSerializer, VendorSerializer
from ..products.serializers import ProductSerializer
from utils.exceptionhandler import CustomException

logger = logging.getLogger('django')

class OrderView(viewsets.ModelViewSet):
    """Gives the view for the Order"""

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    order_service = OrderService()

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as exc:
            raise CustomException(exc.status_code, "Exception in Retrieving Orders")

    def create(self, request, *args, **kwargs):
        try:
            order_products = request.data['orderproducts']
            request.data.pop('orderproducts')
            validated_data = OrderSerializer(data=request.data)
            validated_data.is_valid(raise_exception=True)
            new_order = self.order_service.create(validated_data, order_products)
            serialized = OrderSerializer(new_order)
            return Response(serialized.data)
        except Exception as exc :
            raise CustomException(exc.status_code, "Exception in Creating Order")


    def update(self, request, *args, **kwargs):
        try:
            order_details = self.get_object()
            order_products = request.data['orderproducts']
            request.data.pop('orderproducts')
            validated_data = OrderSerializer(data=request.data)
            validated_data.is_valid(raise_exception=True)
            order = self.order_service.update(order_details, validated_data, order_products)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except KeyError as exc :
            raise CustomException(exc.status_code, "Exception in Updating Order")

    def partial_update(self, request, *args, **kwargs):
        try:
            response = self.update(request)
            return response
        except KeyError as exc :
            raise CustomException(exc.status_code, "Exception in Patch Order")

    def destroy(self, request, *args, **kwargs):
        try:
            super().destroy(request)
            return Response({"message" : "Order Deleted"})
        except Exception as exc:
            raise CustomException(exc.status_code, "Exception in Delete Order")


class CustomerView(viewsets.ModelViewSet):
    """Gives the view for the Customer"""

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class VendorView(viewsets.ModelViewSet):
    """Gives the view for the Vendor"""

    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
