from rest_framework import serializers
from rest_framework.exceptions import APIException
import utils.exceptionhandler as exceptionhandler
import datetime
from datetime import date, timedelta

from .models import Invoice,Payment
from utils.exceptionhandler import CustomException
from ..orders.serializers import OrderSerializer


class InvoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invoice
        fields = ('id','amount','created_date','payment_deadline', 'payment_status','orders')

    def validate(self, data):
        try:
            payment_deadline = datetime.datetime.strptime(self.initial_data['payment_deadline'], '%Y-%m-%d')
            if payment_deadline < datetime.datetime.today():
                raise CustomException(400, "Payment date cannot be before today")
            return data
        except KeyError:
            data['payment_deadline'] = date.today() + timedelta(days=15)
            return data


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        #depth = 1
        fields = ('id','payee_name','payment_type','email','phone', 'invoice','amount')
