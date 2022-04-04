from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets

from .models import Order,Customer,OrderProduct,Product, Vendor
from .service import OrderService
from .serializers import OrderSerializer, OrderProductSerializer,CustomerSerializer, VendorSerializer
from ..products.serializers import ProductSerializer


class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class CustomerView(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class VendorView(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class OrderProductView(viewsets.ModelViewSet):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductSerializer


# @api_view(['POST'])
# def add_orders(request):
#     """To Add new sales or purchase order"""
#
#     order_serializer = OrderSerializer(data=request.data)
#     order_serializer.is_valid(raise_exception=True)
#     order_serializer.save()
#     # order_product_serializer = OrderProductSerializer(data=request.data['orderproducts'], many=True)
#     # order_product_serializer.is_valid(raise_exception=True)
#     # order_service = OrderService()
#     # order_details = order_service.add_orders(order_serializer, order_product_serializer)
#     return Response(order_serializer.data)
#     #except Exception as e:
#     #    return Response("Quantity")
#
#
# @api_view(['GET'])
# def get_order_by_id(request, order_id):
#     """Get order details for the given order id"""
#
#     order_service = OrderService()
#     order_data = order_service.get_order_id(order_id)
#     return Response(order_data)
#
#
# @api_view(['GET'])
# def get_all(request):
#     """Get details of all the orders placed"""
#
#     order_service = OrderService()
#     order_data = order_service.get_all_orders()
#     return Response(order_data)
#
#
# @api_view(['PUT'])
# def update_order(request, order_id):
#     """Update details of the order with the given data"""
#
#     order_service = OrderService()
#     order_data = order_service.update_order(order_id, request.data)
#     return Response(order_data)