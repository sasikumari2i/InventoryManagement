from rest_framework import serializers
from rest_framework.exceptions import APIException

from .models import Invoice
import utils.exceptionhandler as exceptionhandler
from utils.exceptionhandler import CustomException


class InvoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invoice
        fields = "__all__"