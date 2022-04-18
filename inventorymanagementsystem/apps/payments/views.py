from django.shortcuts import render
from .models import Invoice, Payment
from .service import InvoiceService, PaymentService
from .serializers import InvoiceSerializer,PaymentSerializer
from rest_framework import viewsets
from rest_framework.response import Response


# Create your views here.
class InvoiceView(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    invoice_service = InvoiceService()

    def create(self, request, *args, **kwargs):
        order_id = request.data['order']
        validated_data = InvoiceSerializer(data=request.data)
        validated_data.is_valid(raise_exception=True)
        new_invoice = self.invoice_service.create(validated_data, order_id)
        serialized = InvoiceSerializer(new_invoice)
        return Response(serialized.data)

class PaymentView(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    payment_service = PaymentService()

    def create(self, request, *args, **kwargs):
        invoice_id = request.data['invoice']
        validated_data = PaymentSerializer(data=request.data)
        validated_data.is_valid(raise_exception=True)
        new_payment = self.payment_service.create(validated_data, invoice_id)
        serialized = PaymentSerializer(new_payment)
        return Response(serialized.data)