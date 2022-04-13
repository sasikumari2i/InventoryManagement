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

    @transaction.atomic()
    def create(self, validated_data, order_products):
        products = Product.objects.all()
        new_order = Order.objects.create(is_sales_order=validated_data.data['is_sales_order'],
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
            order_product_data = OrderProduct.objects.create(order=new_order, product=product_details,
                                                             quantity=product['quantity'])

        order_product_data.save()
        new_order.save()

        return new_order

    @transaction.atomic
    def update(self, order_details, validated_data, order_products):

        order_details.is_sales_order = validated_data.data['is_sales_order']
        order_details.order_date = validated_data.data['order_date']
        order_details.delivery_date = validated_data.data['delivery_date']
        order_details.vendors_id = validated_data.data['vendors']
        order_details.customers_id = validated_data.data['customers']
        order_details.save()

        for product in order_products:
            product_details = Product.objects.get(id=product['product'])
            if validated_data.data['is_sales_order'] and product_details.available_stock >= product['quantity']:
                product_details.available_stock = product_details.available_stock - product['quantity']
            elif not validated_data.data['is_sales_order']:
                product_details.available_stock = product_details.available_stock + product['quantity']
            else:
                raise Exception("Enter only available stock")
            product_details.save()
            order_product_details = OrderProduct.objects.get(product=product_details.id,
                                                             order=order_details.id)
            order_product_details.product = product_details
            order_product_details.order = order_details
            order_product_details.quantity = product['quantity']
            order_product_details.save()

            return order_details