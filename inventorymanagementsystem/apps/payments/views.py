from django.shortcuts import render
from .models import Invoice
from .service import InvoiceService
from .serializers import InvoiceSerializer
from rest_framework import viewsets
from rest_framework.response import Response



# Create your views here.
class InvoiceView(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    invoice_service = InvoiceService()

    def create(self, request, *args, **kwargs):
        validated_data = InvoiceSerializer(data=request.data)
        validated_data.is_valid(raise_exception=True)
        new_invoice = self.invoice_service.create(validated_data)
        serialized = InvoicSerializer(new_invoice)
        return Response(serialized.data)