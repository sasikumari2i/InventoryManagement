import sys
from rest_framework import serializers
import datetime
from datetime import date, timedelta
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from .models import Vendor, Order,OrderProduct,Customer
from ..products.models import Product
import utils.exceptionhandler as exceptionhandler
from ..products.serializers import ProductSerializer
from utils.exceptionhandler import CustomException


class AssetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Asset
        fields = "__all__"

class RepairingStockSerializer(serializers.ModelSerializer):

    class Meta:
        model = RepairingStock
        fields = "__all__"
