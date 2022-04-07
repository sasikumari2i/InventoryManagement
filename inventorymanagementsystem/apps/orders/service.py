import io

from .serializers import OrderSerializer
from .serializers import OrderProductSerializer
from .models import Order
from .models import OrderProduct
from ..products.models import Product,Category
from ..products.serializers import ProductSerializer
from django.db import transaction
from ..products.service import ProductService

class OrderService:
    """Performs order related operations like add new order, get single order,
    get all orders, update an order and delete order"""

    products = Product.objects.all()

    @transaction.atomic
    def add_orders(self, validated_data):
        """To Add new sales or purchase order from the given data"""

        products = Product.objects.all()
        order_products = validated_data['orderproducts']
        validated_data.pop('orderproducts')
        order = Order.objects.create(**validated_data)

        for product in order_products:
            product_details = products.get(id=product['product'])
            if validated_data.get('is_sales_order') and product_details.available_stock >= product['quantity']:
                product_details.available_stock = product_details.available_stock - product['quantity']
            elif not validated_data.get('is_sales_order'):
                product_details.available_stock = product_details.available_stock + product['quantity']
            else:
                raise Exception("Enter only available stock")
            product_details.save()
            order_product_data = OrderProduct.objects.create(order=order,product=product_details,
                                                              quantity=product['quantity'])
        #order.save()
        order_response = OrderSerializer(order)

        return order_response.data

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
        # if order_details.is_valid():
        #     order_details.save()
        #     print("Is Valid")

        # order_details = Order.objects.get(id=order_id)
        # for key, value in order_data.items():
        #     if order_details.__getattribute__(key):
        #         order_details.__setattr__(key, value)
        #     order_details.save()
        order_serializer = OrderSerializer(order_details)
        return order_serializer.data