import io
from datetime import date, timedelta

from .serializers import OrderSerializer
from .serializers import OrderProductSerializer
from .models import Order
from .models import OrderProduct
from ..products.models import Product,Category
from ..payments.models import Invoice
from ..products.serializers import ProductSerializer
from django.db import transaction
from utils.exceptionhandler import CustomException
from django.core.exceptions import ValidationError


class OrderService:
    """Performs order related operations like add new order, get single order,
    get all orders, update an order and delete order"""

    @transaction.atomic()
    def create(self, validated_data, order_products):
        try:
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
                    raise CustomException(400,"Enter only available stock")
                product_details.save()
                order_product_data = OrderProduct.objects.create(order=new_order, product=product_details,
                                                                 quantity=product['quantity'])

            if not new_order.is_sales_order:
                invoice = self.create_invoice(new_order)
                invoice.save()

            order_product_data.save()
            new_order.save()
            return new_order
        except Exception as exc:
            raise CustomException(exc.status_code, "Exception in Order Creation")

    @transaction.atomic
    def update(self, order_details, validated_data, order_products):
        try:
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
                    raise CustomException(400, "Enter only available stock")
                product_details.save()
                order_product_details = OrderProduct.objects.get(product=product_details.id,
                                                                 order=order_details.id)
                order_product_details.product = product_details
                order_product_details.order = order_details
                order_product_details.quantity = product['quantity']
                order_product_details.save()

            return order_details
        except ValidationError as exc:
            raise CustomException(exc.status_code, "Exception in Order Update")


    def create_invoice(self,new_order):
        try:
            amount = 0
            products = Product.objects.all()
            order_serializer = OrderSerializer(new_order)
            for orders in order_serializer.data['orderproducts']:
                product = products.get(id=orders['product'])
                product_price = product.price
                product_quantity = orders['quantity']
                amount = amount + (product_price * product_quantity)

            created_date = date.today()
            payment_deadline = created_date + timedelta(days=15)
            invoice = Invoice.objects.create(amount=amount, created_date=created_date,
                                             payment_deadline=payment_deadline, order=new_order)
            return invoice
        except Exception as exc:
            raise CustomException(exc.status_code, "Exception in PO Invoice Creation")


