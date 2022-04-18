import io
from datetime import date, timedelta

from .serializers import InvoiceSerializer
from .models import Invoice
from ..payments.models import Invoice
from ..orders.models import Order
from ..orders.serializers import OrderSerializer
from ..products.models import Product
from django.db import transaction
from utils.exceptionhandler import CustomException
from django.core.exceptions import ValidationError


class InvoiceService:
    """Performs order related operations like add new order, get single order,
    get all orders, update an order and delete order"""

    @transaction.atomic()
    def create(self, validated_data):
        #try:
        order_id = validated_data.data['order']
        print(order_id)
        order = Order.objects.get(id=order_id)
        if not order.is_sales_order:
            raise CustomException(400,"Invoice cannot be created for Purchase Order")
        amount = self.total_amount(order)
        created_date = date.today()
        if validated_data.data['payment_deadline'] is None:
            validated_data.data['payment_deadline'] = created_date + timedelta(days=15)
        payment_deadline = validated_data.data['payment_deadline']
        invoice = Invoice.objects.create(amount=amount, created_date=created_date,
                                         payment_deadline=payment_deadline, order=order)

        return invoice
        #except Exception as exc:
            #raise CustomException(exc.status_code, "Exception in SO Invoice Creation")


    def total_amount(self,order):
        #try:
        amount = 0
        products = Product.objects.all()
        order_serializer = OrderSerializer(order)

        for orders in order_serializer.data['orderproducts']:
            product = products.get(id=orders['product'])
            product_price = product.price
            product_quantity = orders['quantity']
            amount = amount + (product_price * product_quantity)

        return amount
        #except Exception as exc:
         #   raise CustomException(400, "Exception in PO Invoice Creation")