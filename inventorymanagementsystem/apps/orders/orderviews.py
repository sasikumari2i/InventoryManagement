from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from django.db import transaction

from .models import Order,Customer,OrderProduct,Product, Vendor
from .service import OrderService
from .serializers import OrderSerializer, OrderProductSerializer,CustomerSerializer, VendorSerializer
from ..products.serializers import ProductSerializer

class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    order_service = OrderService()

    def destroy(self, request, *args, **kwargs):
        super().destroy(request)
        return Response({"message" : "Order Deleted"})

    def create(self, request, *args, **kwargs):
        order_products = request.data['orderproducts']
        request.data.pop('orderproducts')
        validated_data = OrderSerializer(data=request.data)
        validated_data.is_valid(raise_exception=True)
        new_order = self.order_service.create(validated_data, order_products)
        serialized = OrderSerializer(new_order)
        return Response(serialized.data)

    def update(self, request, *args, **kwargs):
        order_details = self.get_object()
        order_products = request.data['orderproducts']
        request.data.pop('orderproducts')
        validated_data = OrderSerializer(data=request.data)
        validated_data.is_valid(raise_exception=True)
        order = self.order_service.update(order_details, validated_data, order_products)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        self.update(request)
        return Response({"message" : "Updated"})

class CustomerView(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class VendorView(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer