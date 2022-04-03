import io

from .serializers import OrderSerializer
from .serializers import OrderProductSerializer
from .models import Order
from .models import OrderProduct
from ..products.models import Product,Category
from ..products.serializers import ProductSerializer
from django.db import transaction
import io
from rest_framework.parsers import JSONParser

class OrderService:
    """Performs order related operations like add new order, get single order,
    get all orders, update an order and delete order"""

    @transaction.atomic
    def add_orders(self, data):
        """To Add new sales or purchase order from the given data"""

        #product_data = order_data['products']
        #order_data.pop('products')
        #print(data['products'])
        order = OrderSerializer(data=data)
        order.is_valid(raise_exception=False)
        print(order.errors)
        order.save()
        return order
        #if not order.is_valid():
        #    order.save()

        # order = Order.objects.create(**order_data)
        # for products in product_data:
        #     quantity = products['quantity']
        #     products.pop('quantity')
        #     product_details = Product.objects.get(id=products['id'])
        #     if order.is_sales_order and product_details.available_stock >= quantity :
        #         product_details.available_stock = product_details.available_stock - quantity
        #         product_details.save()
        #     elif not order.is_sales_order:
        #         product_details.available_stock = product_details.available_stock + quantity
        #         product_details.save()
        #     else:
        #         raise Exception("Enter only available stock")
        #
        #     order_product = OrderProduct.objects.create(product=product_details,order=order,quantity=quantity)

        #order_serializer = OrderProductSerializer(order_product)
        #return order_serializer.data

    def get_order_id(self,order_id):
        """Get order details for the given order id"""

        order_data = Order.objects.get(id=order_id)
        order_serializer = OrderSerializer(order_data)
        return order_serializer.data

    def get_all_orders(self):
        """Get details of all the orders placed"""

        orders = Order.objects.all()
        order_serializer = OrderSerializer(orders, many=True)
        return order_serializer.data

    def update_order(self,order_id, order_data):
        """Update details of the order with the given data"""

        order_details = OrderSerializer(data=order_data)
        if order_details.is_valid():
            order_details.save()
            print("Is Valid")

        # order_details = Order.objects.get(id=order_id)
        # for key, value in order_data.items():
        #     if order_details.__getattribute__(key):
        #         order_details.__setattr__(key, value)
        #     order_details.save()
        order_serializer = OrderSerializer(order_details)
        return order_serializer.data