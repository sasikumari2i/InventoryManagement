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
        """Created new Invoice for the given order and the data"""

        try:
            orders = Order.objects.all()
            order = orders.get(id=order_id)
            amount = self.total_amount(order)
            created_date = date.today()
            if validated_data.data['payment_deadline'] is None:
                validated_data.data['payment_deadline'] = created_date + timedelta(days=15)
            payment_deadline = validated_data.data['payment_deadline']
            invoice = Invoice.objects.create(amount=amount, created_date=created_date,
                                             payment_deadline=payment_deadline, order=order)

            return invoice
        except ValidationError:
            raise CustomException(400, "Validation Error in payment service")


    def total_amount(self,order):
        """Calculates total amount of the order to be placed"""

        try:
            amount = 0
            products = Product.objects.all()
            order_serializer = OrderSerializer(order)

            for orders in order_serializer.data['order_products']:
                product = products.get(id=orders['product'])
                product_price = product.price
                product_quantity = orders['quantity']
                amount = amount + (product_price * product_quantity)

            return amount
        except ValidationError:
            raise CustomException(400, "Exception in PO Invoice Creation")

class PaymentService:
    """Performs payment related operations like creating, updating and deleting"""

    @transaction.atomic()
    def create(self, validated_data, invoice_id):
        """Creates new payment for the invoice given"""

        try:
            invoices = Invoice.objects.all()
            invoice = invoices.get(id=invoice_id)
            if invoice.payment_status:
                raise CustomException(status_code=400, detail="Already paid")
            invoice.payment_status = True
            invoice.save()
            payment = Payment.objects.create(payee_name=validated_data.data['payee_name'],
                                             email=validated_data.data['email'],
                                             payment_type=validated_data.data['payment_type'],
                                             phone=validated_data.data['phone'],
                                             amount=validated_data.data['amount'],
                                             invoice=invoice)
            payment.save()
            return payment
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
