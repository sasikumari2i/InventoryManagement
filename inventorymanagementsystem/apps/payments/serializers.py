from rest_framework import serializers
from rest_framework.exceptions import APIException

from .models import Invoice
import utils.exceptionhandler as exceptionhandler
from utils.exceptionhandler import CustomException
from ..orders.serializers import OrderSerializer


class InvoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invoice
        fields = ('amount','created_date','payment_deadline', 'order')

