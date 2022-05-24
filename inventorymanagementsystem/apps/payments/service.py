import io
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from django.db import transaction

from .serializers import InvoiceSerializer
from .models import Invoice, Payment
from ..orders.models import Order, Customer
from ..orders.serializers import OrderSerializer
from ..products.models import Product
from utils.exceptionhandler import CustomException
from django.contrib.auth.middleware import AuthenticationMiddleware


class InvoiceService:
    """Performs invoice related operations like creating, updating and deleting"""

    @transaction.atomic()
    def create(self, validated_data, order_id, organisation):
        """Creates new Invoice for the given order and the data"""

        try:
            orders = Order.objects.filter(organisation_id=organisation)
            order = orders.get(order_uid=order_id)
            if order.invoices is not None:
                try:
                    invoice = Invoice.objects.get(order=order, is_active=True)
                    if invoice is not None:
                        raise CustomException(
                            400, "Invoice Already active for this Order"
                        )
                except Invoice.DoesNotExist:
                    pass
            amount = self.total_amount(order, organisation)
            created_date = date.today()
            if validated_data.data["payment_deadline"] is None:
                validated_data.data["payment_deadline"] = created_date + timedelta(
                    days=15
                )
            payment_deadline = validated_data.data["payment_deadline"]
            invoice = Invoice.objects.create(
                amount=amount,
                created_date=created_date,
                payment_deadline=payment_deadline,
                orders=order,
                organisation_id=order.organisation_id,
            )

            return invoice
        except ValidationError:
            raise CustomException(400, "Validation Error in payment service")

    def total_amount(self, order, organisation):
        """Calculates total amount of the order to be placed"""

        try:
            amount = 0
            products = Product.objects.get(organisation_id=organisation)
            order_serializer = OrderSerializer(order)

            for orders in order_serializer.data["order_products"]:
                product = products.get(product_uid=orders["product"])
                product_price = product.price
                product_quantity = orders["quantity"]
                amount = amount + (product_price * product_quantity)

            return amount
        except ValidationError:
            raise CustomException(400, "Exception in PO Invoice Creation")

    def retrieve(self, pk, organisation):
        """To retrieve the Invoice of given Id"""

        try:
            invoice = Invoice.objects.get(invoice_uid=pk, organisation_id=organisation)
            return invoice
        except Invoice.DoesNotExist:
            raise CustomException(404, "Invoice Not Found")

    def update_invoice(self, invoice_details):
        """Updates the invoice status of the given order"""

        try:
            invoice_status = invoice_details.is_active
            response = {}
            if not invoice_status:
                response = {"message": "It is already Inactive"}
            elif invoice_status:
                invoice_details.is_active = False
                invoice_details.save()
                response = {"message": "Invoice Status Updated"}
            return response
        except NotFound:
            raise CustomException(400, "Internal error in updating delivery status")


class PaymentService:
    """Performs payment related operations like creating, updating and deleting"""

    @transaction.atomic()
    def create(self, validated_data, invoice_id, organisation):
        """Creates new payment for the invoice given"""

        try:
            invoice = Invoice.objects.get(
                invoice_uid=invoice_id, is_active=True, organisation_id=organisation
            )
            if invoice.payment_status:
                raise CustomException(status_code=400, detail="Already paid")
            invoice.payment_status = True
            if invoice.amount == validated_data.data["amount"]:
                invoice.save()
                payment = Payment.objects.create(
                    payee_name=validated_data.data["payee_name"],
                    email=validated_data.data["email"],
                    payment_type=validated_data.data["payment_type"],
                    phone=validated_data.data["phone"],
                    amount=validated_data.data["amount"],
                    invoice=invoice,
                    organisation_id=organisation,
                )
                payment.save()
            else:
                raise CustomException(400, "Please give correct amount")
            return payment
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Invoice.DoesNotExist:
            raise CustomException(404, " Invoice not available")
