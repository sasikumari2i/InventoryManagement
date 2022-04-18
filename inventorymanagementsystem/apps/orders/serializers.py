import sys
from rest_framework import serializers
import datetime
from django.core.exceptions import ValidationError

from .models import Vendor, Order,OrderProduct,Customer
from ..products.models import Product
import utils.exceptionhandler as exceptionhandler
from ..products.serializers import ProductSerializer
from rest_framework.exceptions import APIException
from utils.exceptionhandler import CustomException


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = "__all__"

class OrderProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderProduct
        fields = ('product','quantity')


class OrderSerializer(serializers.ModelSerializer):

    orderproducts = OrderProductSerializer(many=True,read_only=True)

    class Meta:
        model = Order
        fields = ('id','is_sales_order','order_date','delivery_date','vendors','customers','orderproducts')

    def validate(self, data):
        if data['is_sales_order'] is True and self.initial_data['vendors'] is not None:
            raise CustomException(400, "Sales Order cannot have Vendor")
        elif data['is_sales_order'] is False and self.initial_data['customers'] is not None:
            raise CustomException(400, "Purchase Order cannot have Customer")
        elif self.initial_data['vendors'] is None and self.initial_data['customers'] is None:
            raise CustomException(400, "Please give vendor or customer details for the order")
        return data


class VendorSerializer(serializers.ModelSerializer):

    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = Vendor
        fields = ('id','name','address','email','phone_number','orders')