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

    @transaction.atomic
    def add_orders(self, order_serializer):
        """To Add new sales or purchase order from the given data"""

        order_serializer.is_valid(raise_exception=True)

        order_placed = OrderSerializer(order_serializer)
        #order_placed.is_valid(raise_exception=True)
        #order_placed.

        print(order_placed)

        #print(type(order_placed))
        #print(order_placed)

        #print(order_placed.data['orderproducts'])

        #products = Product.objects.all()
        #print(products.get(id=4))
        #order_serializer.save()
        #print(order_serializer)
        #order_serializer.is_valid(raise_exception=True)
        #order_serializer.save()
        #order = OrderSerializer(order_serializer)
        #order_conf = Order.objects.create(**order)
        #order = Order.objects.create(rder_serializer)
        #data = order_serializer.validated_data
        #order_serializer.save()
        #print(order_products)
        #print(type(order_serializer))
        #order_serializer.pop('orderproducts')
        #print(order_serializer)
        # for order_products in order_product_serializer:
        #     product_details = products.get(id=order_products['products'])
        #
        #     if order_serializer.is_sales_order and product_details.available_stock >= order_products.quantity:
        #         product_details.available_stock = product_details.available_stock - order_products.quantity
        #     elif not order.is_sales_order:
        #         product_details.available_stock = product_details.available_stock + order_products.quantity
        #     else:
        #         raise Exception("Enter only available stock")
        #     product_details.save()
        #     order_product_data = OrderProduct.objects.create(order=order_serializer,product=product_details,
        #                                                      quantity=order_products.quantity)


        # product_data = data['products']
        # data.pop('products')
        # order = Order.objects.create(**data)
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
        # #     else:
        # #         raise Exception("Enter only available stock")
        # #
        #     order_product = OrderProduct.objects.create(product=product_details,order=order,quantity=quantity)
        #
        #ordered = OrderProductSerializer(order_product_data)
        return order_serializer

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