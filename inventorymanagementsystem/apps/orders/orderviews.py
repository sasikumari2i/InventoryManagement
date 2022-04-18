from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from django.db import transaction

from .models import Order,Customer,OrderProduct,Product, Vendor
from .service import OrderService
from .serializers import OrderSerializer, OrderProductSerializer,CustomerSerializer, VendorSerializer
from ..products.serializers import ProductSerializer
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from utils.exceptionhandler import CustomException
from rest_framework.exceptions import APIException

import logging

logger = logging.getLogger('django')


class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    order_service = OrderService()

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except ObjectDoesNotExist as exc:
            raise CustomException(exc.status_code, "The requested page is not found")

    def create(self, request, *args, **kwargs):
        try:
            order_products = request.data['orderproducts']
            request.data.pop('orderproducts')
            validated_data = OrderSerializer(data=request.data)
            validated_data.is_valid(raise_exception=True)
            new_order = self.order_service.create(validated_data, order_products)
            serialized = OrderSerializer(new_order)
            return Response(serialized.data)
        except ObjectDoesNotExist as exc :
            raise CustomException(exc.status_code, "The requested page is not found")


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
            raise CustomException(exc.status_code, "Verify the Data entered")

    def partial_update(self, request, *args, **kwargs):
        response = self.update(request)
        return response

    def destroy(self, request, *args, **kwargs):
        super().destroy(request)
        return Response({"message" : "Order Deleted"})


class CustomerView(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class VendorView(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
