from rest_framework import serializers
import datetime

from .models import Vendor, Order,OrderProduct,Customer
from ..products.models import Product

from ..products.serializers import ProductSerializer

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = "__all__"

class OrderProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderProduct
        #depth = 1
        fields = ('product','quantity')
        #exclude = ('id','order')



class OrderSerializer(serializers.ModelSerializer):

    orderproducts = OrderProductSerializer(many=True,read_only=True)

    class Meta:
        model = Order
        #depth = 1
        fields = ('id','is_sales_order','order_date','delivery_date','vendors','customers','orderproducts')

    def validate(self, data):
        if data['is_sales_order'] is True and self.initial_data['vendors'] is not None:
            raise Exception("Sales Order cannot have Vendor")
        elif data['is_sales_order'] is False and self.initial_data['customers'] is not None:
            raise Exception("Purchase Order cannot have Customer")
        elif self.initial_data['vendors'] is None and self.initial_data['customers'] is None:
            raise Exception("Please give vendor or customer details for the order")
        return data

class VendorSerializer(serializers.ModelSerializer):

    orders =OrderSerializer(many=True, read_only=True)

    class Meta:
        model = Vendor
        #depth = 1
        #fields = "__all__"
        fields = ('id','name','address','email','phone_number','orders')