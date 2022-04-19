from django.shortcuts import render
from .models import Invoice, Payment
from .service import InvoiceService, PaymentService
from .serializers import InvoiceSerializer,PaymentSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from utils.exceptionhandler import CustomException


class InvoiceView(viewsets.ModelViewSet):
    """Gives the view for the Invoice"""

    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    invoice_service = InvoiceService()

    def create(self, request, *args, **kwargs):
        try:
            order_id = request.data['order']
            validated_data = InvoiceSerializer(data=request.data)
            validated_data.is_valid(raise_exception=True)
            new_invoice = self.invoice_service.create(validated_data, order_id)
            serialized = InvoiceSerializer(new_invoice)
            return Response(serialized.data)
        except Exception as exc:
            raise CustomException(exc.status_code, "Exception in invoice creation views")

class PaymentView(viewsets.ModelViewSet):
    """Gives the view for the Payment"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    payment_service = PaymentService()

    def create(self, request, *args, **kwargs):
        try:
            invoice_id = request.data['invoice']
            validated_data = PaymentSerializer(data=request.data)
            validated_data.is_valid(raise_exception=True)
            new_payment = self.payment_service.create(validated_data, invoice_id)
            serialized = PaymentSerializer(new_payment)
            return Response(serialized.data)
        except Exception as exc:
            raise CustomException(exc.status_code, "Exception in payment creation views")