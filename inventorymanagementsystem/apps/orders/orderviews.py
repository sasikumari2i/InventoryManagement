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

    def destroy(self, request, *args, **kwargs):
        #order = self.get_object()
        #order.delete()
        super().destroy(request)
        return Response({"message" : "Order Deleted"})

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        products = Product.objects.all()
        order_products = request.data['orderproducts']
        request.data.pop('orderproducts')
        validated_data = OrderSerializer(data=request.data)
        validated_data.is_valid(raise_exception=True)
        new_order = Order.objects.create(is_sales_order=validated_data.data['is_sales_order'],
                                         #order_date=validated_data.data['order_date'],
                                         delivery_date=validated_data.data['delivery_date'],
                                         vendors_id=validated_data.data['vendors'],
                                         customers_id=validated_data.data['customers'])

        for product in order_products:
            product_details = products.get(id=product['product'])
            if validated_data.data['is_sales_order'] and product_details.available_stock >= product['quantity']:
                product_details.available_stock = product_details.available_stock - product['quantity']
            elif not validated_data.data['is_sales_order']:
                product_details.available_stock = product_details.available_stock + product['quantity']
            else:
                raise Exception("Enter only available stock")
            product_details.save()
            order_product_data = OrderProduct.objects.create(order=new_order,product=product_details,
                                                              quantity=product['quantity'])

        order_product_data.save()
        new_order.save()
        serialized = OrderSerializer(new_order)
        return Response(serialized.data)



class CustomerView(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class VendorView(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


# class OrderProductView(viewsets.ModelViewSet):
#     queryset = OrderProduct.objects.all()
#     serializer_class = OrderProductSerializer


# @api_view(['POST'])
# def add_orders(request):
#     """To Add new sales or purchase order"""
#
#     validated_data = OrderSerializer(data=request.data)
#     validated_data.is_valid(raise_exception=True)
#     order_service = OrderService()
#     order_details = order_service.add_orders(request.data)
#
#     return Response(order_details)
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