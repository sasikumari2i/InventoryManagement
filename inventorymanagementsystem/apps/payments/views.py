from django.shortcuts import render
from .models import Invoice
from .serializers import InvoiceSerializer
from rest_framework import viewsets


# Create your views here.
class InvoiceView(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer