from rest_framework.response import Response
from rest_framework import viewsets, generics
from django.db import transaction
import logging
from rest_framework.exceptions import APIException
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import Http404

from .models import Order,Customer,OrderProduct,Product, Vendor
from .service import OrderService
from .serializers import CustomerSerializer, VendorSerializer, DeliverySerializer
from .serializers import OrderSerializer, OrderProductSerializer
from ..products.serializers import ProductSerializer
from utils.exceptionhandler import CustomException

logger = logging.getLogger('django')

class OrderView(viewsets.ModelViewSet):
    """Gives the view for the Order"""

    queryset = Order.objects.get_queryset().order_by('id')
    serializer_class = OrderSerializer
    order_service = OrderService()

    def retrieve(self, request, *args, **kwargs):
        """Retrieves specific order for the given order id"""

        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as exc:
            raise CustomException(exc.status_code, "Exception in Retrieving Orders")

    def create(self, request, *args, **kwargs):
        """Creates new order using given data"""

        try:
            order_products = request.data['order_products']
            request.data.pop('order_products')
            validated_data = OrderSerializer(data=request.data)
            validated_data.is_valid(raise_exception=True)
            new_order = self.order_service.create(validated_data, order_products)
            serialized = OrderSerializer(new_order)
            return Response(serialized.data)
        except Vendor.DoesNotExist:
            raise CustomException(400, "KeyError in Order Creation View")


    def update(self, request, *args, **kwargs):
        """Updates the given order"""

        try:
            order_details = self.get_object()
            order_products = request.data['order_products']
            request.data.pop('order_products')
            validated_data = OrderSerializer(data=request.data)
            validated_data.is_valid(raise_exception=True)
            order = self.order_service.update(order_details, validated_data, order_products)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except KeyError:
            raise CustomException(400, "Exception in Updating Order View")
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)

    def partial_update(self, request, *args, **kwargs):
        """Updates partial fields for the given order"""

        try:
            response = self.update(request)
            return response
        except KeyError:
            raise CustomException(400, "Exception in Patch Order")


    def destroy(self, request, *args, **kwargs):
        """Deletes the given order"""

        try:
            super().destroy(request)
            return Response({"message" : "Order Deleted"})
        except Http404:
            raise CustomException(404, "Exception in Delete Order")



class CustomerView(viewsets.ModelViewSet):
    """Gives the view for the Customer"""

    queryset = Customer.objects.get_queryset().order_by('id')
    serializer_class = CustomerSerializer


class VendorView(viewsets.ModelViewSet):
    """Gives the view for the Vendor"""

    queryset = Vendor.objects.get_queryset().order_by('id')
    serializer_class = VendorSerializer


class DeliveryView(generics.GenericAPIView):

    queryset = Order.objects.all()
    serializer_class = DeliverySerializer
    order_service = OrderService()

    def put(self, request, *args, **kwargs):
        try:
            order_details = self.get_object()
            response = self.order_service.update_delivery(order_details)
            return Response(response)
        except Http404:
            raise CustomException(404,"Exception in Updating Delivery Status")


class CustomerOrderView(generics.ListAPIView):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        """Retrieves the list of Orders for the given customer"""

        customer_id = self.kwargs['customer']
        orders = Order.objects.filter(customers=customer_id)
        serialized = OrderSerializer(orders,many=True)
        return Response(serialized.data)

class VendorOrderView(generics.ListAPIView):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        """Retrieves the list of Orders for the given vendor"""

        vendor_id = self.kwargs['vendor']
        orders = Order.objects.filter(vendors=vendor_id)
        serialized = OrderSerializer(orders,many=True)
        return Response(serialized.data)
