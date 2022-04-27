import io
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from django.db import transaction

from .serializers import InvoiceSerializer
from .models import Invoice, Payment
from ..orders.models import Order
from ..orders.serializers import OrderSerializer
from ..products.models import Product
from utils.exceptionhandler import CustomException


class InvoiceService:
    """Performs invoice related operations like creating, updating and deleting"""

    @transaction.atomic()
    def create(self, validated_data, order_id):
        try:
            orders = Order.objects.all()
            order = orders.get(id=order_id)
            # if not order.is_sales_order:
            #     raise CustomException(400,"Invoice cannot be created for Purchase Order")
            amount = self.total_amount(order)
            created_date = date.today()
            if validated_data.data['payment_deadline'] is None:
                validated_data.data['payment_deadline'] = created_date + timedelta(days=15)
            payment_deadline = validated_data.data['payment_deadline']
            invoice = Invoice.objects.create(amount=amount, created_date=created_date,
                                             payment_deadline=payment_deadline, order=order)

            return invoice
        except Exception as exc:
            raise CustomException(exc.status_code, "Exception in SO Invoice Creation")


    def total_amount(self,order):
        try:
            amount = 0
            products = Product.objects.all()
            order_serializer = OrderSerializer(order)

            for orders in order_serializer.data['orderproducts']:
                product = products.get(id=orders['product'])
                product_price = product.price
                product_quantity = orders['quantity']
                amount = amount + (product_price * product_quantity)

            return amount
        except Exception as exc:
            raise CustomException(exc.status_code, "Exception in PO Invoice Creation")

class PaymentService:
    """Performs payment related operations like creating, updating and deleting"""

    @transaction.atomic()
    def create(self, validated_data, invoice_id):
        try:
            invoices = Invoice.objects.all()
            invoice = invoices.get(id=invoice_id)

            invoice.payment_status = True
            invoice.save()
            payment = Payment.objects.create(payee_name=validated_data.data['payee_name'],
                                             email=validated_data.data['email'],
                                             phone=validated_data.data['phone'],
                                             invoice=invoice)
            payment.save()

            return payment
        except Exception as exc:
            raise CustomException(exc.status_code, "Exception in Payment Creation")
