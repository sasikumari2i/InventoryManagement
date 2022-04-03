from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Order
from .service import OrderService
from .serializers import OrderSerializer


@api_view(['POST'])
def add_orders(request):
    """To Add new sales or purchase order"""
    #try:
    order_service = OrderService()
    order_data = order_service.add_orders(request.data)
    return Response(order_data)
    #except Exception as e:
    #    return Response("Quantity")


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
    order_data = order_service.update_order(order_id, **request.data)
    return Response(order_data)