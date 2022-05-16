from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated
import logging

from .models import Invoice, Payment
from .service import InvoiceService, PaymentService
from .serializers import InvoiceSerializer,PaymentSerializer
from utils.exceptionhandler import CustomException

logger = logging.getLogger('django')


class InvoiceView(viewsets.ModelViewSet):
    """Gives the view for the Invoice"""

    # queryset = Invoice.objects.get_queryset().order_by('id')
    serializer_class = InvoiceSerializer
    invoice_service = InvoiceService()

    def get_queryset(self):
        try:
            organisation_id = self.request.query_params.get('organisation', None)
            if organisation_id is None:
                raise CustomException(400, "Credentials required")
            organisation = Organisation.objects.get(id=organisation_id)
            invoices = Invoice.objects.filter(organisation=organisation).order_by('id')
            return invoices
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(400, "Invalid Credentials")

    def create(self, request, *args, **kwargs):
        """Creates new invoice, overrided from ModelViewSet class"""

        try:
            order_id = request.data['order']
            validated_data = InvoiceSerializer(data=request.data)
            validated_data.is_valid(raise_exception=True)
            new_invoice = self.invoice_service.create(validated_data, order_id)
            serialized = InvoiceSerializer(new_invoice)
            return Response(serialized.data)
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)


class PaymentView(viewsets.ModelViewSet):
    """Gives the view for the Payment"""

    # queryset = Payment.objects.get_queryset().order_by('id')
    serializer_class = PaymentSerializer
    payment_service = PaymentService()

    def get_queryset(self):
        try:
            organisation_id = self.request.query_params.get('organisation', None)
            if organisation_id is None:
                raise CustomException(400, "Credentials required")
            organisation = Organisation.objects.get(id=organisation_id)
            payments = Payment.objects.filter(organisation=organisation).order_by('id')
            return payments
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)
        except Organisation.DoesNotExist:
            raise CustomException(400, "Invalid Credentials")

    def create(self, request, *args, **kwargs):
        """Creates new payment, overrided from ModelViewSet class"""

        try:
            invoice_id = request.data['invoice']
            validated_data = PaymentSerializer(data=request.data)
            validated_data.is_valid(raise_exception=True)
            new_payment = self.payment_service.create(validated_data, invoice_id)
            serialized = PaymentSerializer(new_payment)
            logger.info("Payment created")
            return Response(serialized.data)
        except CustomException as exc:
            logger.error("Custom Exception in Payment Creation")
            raise CustomException(exc.status_code, exc.detail)


    def update(self, request, *args, **kwargs):
        return Response({"message" : "Payment cannot be updated"})


class InvoicePaymentView(generics.ListAPIView):

    queryset = Payment.objects.get_queryset().order_by('id')
    serializer_class = PaymentSerializer

    def get(self, request, *args, **kwargs):
        """Retrieves the payments for the Invoice id given"""

        try:
            invoice_id = self.kwargs['invoice']
            payment = Payment.objects.filter(invoice=invoice_id)
            serialized = PaymentSerializer(payment, many=True)
            return Response(serialized.data)
        except ObjectDoesNotExist:
            raise CustomException(404, "The requested invoice does not exist")