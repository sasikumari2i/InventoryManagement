import sys
from rest_framework import serializers
import datetime
from datetime import date, timedelta
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from .models import Asset, RepairingStock
import utils.exceptionhandler as exceptionhandler
from ..products.serializers import ProductSerializer
from utils.exceptionhandler import CustomException


class AssetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Asset
        fields = ('id', 'name','product','customer','serial_no','is_active')

class RepairingStockSerializer(serializers.ModelSerializer):

    class Meta:
        model = RepairingStock
        fields = ('id','asset','product','serial_no','closed_date','is_active')


class RepairingStockCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = RepairingStock
        fields = ('asset',)
