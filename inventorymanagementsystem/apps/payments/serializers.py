from rest_framework import serializers
from rest_framework.exceptions import APIException

from .models import Invoice,Payment
import utils.exceptionhandler as exceptionhandler
from utils.exceptionhandler import CustomException
from ..orders.serializers import OrderSerializer


class InvoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invoice
        fields = ('id','amount','created_date','payment_deadline', 'payment_status')

class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        #depth = 1
        fields = ('id','payee_name','email','phone', 'invoice')
