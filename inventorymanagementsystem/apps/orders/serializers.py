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


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ('id','name','address','email','phone_number','wallet','outstanding_payables')

class OrderProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderProduct
        fields = ('product','quantity')


class OrderSerializer(serializers.ModelSerializer):

    order_products = OrderProductSerializer(many=True,read_only=True)

    class Meta:
        model = Order
        fields = ('id','is_sales_order','order_date','delivery_status','delivery_date','vendors',
                  'customers','order_products','invoice',)

    def validate(self, data):
        """Validations for the Order model"""

        try:
            if data['is_sales_order'] is True and self.initial_data['vendors'] is not None:
                raise CustomException(400, "Sales Order cannot have Vendor")
            elif data['is_sales_order'] is False and self.initial_data['customers'] is not None:
                raise CustomException(400, "Purchase Order cannot have Customer")
            elif self.initial_data['vendors'] is None and self.initial_data['customers'] is None:
                raise CustomException(400, "Please give vendor or customer details for the order")

            try:
                delivery_date = datetime.datetime.strptime(self.initial_data['delivery_date'], '%Y-%m-%d')
                if delivery_date < datetime.datetime.today():
                    raise CustomException(400,"Order date cannot be greater than Delivery date")
            except KeyError:
                data['delivery_date'] = date.today() + timedelta(days=15)

            return data
        except CustomException as exc:
            raise CustomException(exc.status_code, exc.detail)



class VendorSerializer(serializers.ModelSerializer):

    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = Vendor
        fields = ('id','name','address','email','phone_number','orders','outstanding_payables')

class DeliverySerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('id',)


