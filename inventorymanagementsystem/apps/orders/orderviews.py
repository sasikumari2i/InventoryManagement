from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets

from .models import Order,Customer,OrderProduct,Product, Vendor
from .service import OrderService
from .serializers import OrderSerializer, OrderProductSerializer,CustomerSerializer, VendorSerializer
from ..products.serializers import ProductSerializer


# class OrderView(viewsets.ModelViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#
# class CustomerView(viewsets.ModelViewSet):
#     queryset = Customer.objects.all()
#     serializer_class = CustomerSerializer
#
# class VendorView(viewsets.ModelViewSet):
#     queryset = Vendor.objects.all()
#     serializer_class = VendorSerializer
#
# class OrderProductView(viewsets.ModelViewSet):
#     queryset = OrderProduct.objects.all()
#     serializer_class = OrderProductSerializer


@api_view(['POST'])
def add_orders(request):
    """To Add new sales or purchase order"""

    #validated_data = request.data
    #print(request.data['customer'])
    #print(request.data)
    #print(OrderSerializer())
    validated_data = OrderSerializer(data=request.data)
    #print(validated_data)
    validated_data.is_valid(raise_exception=False)
    order_service = OrderService()
    order_details = order_service.add_orders(request.data)

    return Response(order_details)

@api_view(['GET'])
def get_order_by_id(request, order_id):
    """Get order details for the given order id"""

    order_service = OrderService()
    order_data = order_service.get_order_id(order_id)
    return Response(order_data)


@api_view(['GET'])
def get_all(request):
    """Get details of all the orders placed"""

    order_service = OrderService()
    order_data = order_service.get_all_orders()
    return Response(order_data)


@api_view(['PUT'])
def update_order(request, order_id):
    """Update details of the order with the given data"""

    order_service = OrderService()
    order_data = order_service.update_order(order_id, request.data)
    return Response(order_data)