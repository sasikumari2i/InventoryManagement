from rest_framework.serializers import ModelSerializer

from .models import Vendor, Order,OrderProduct,Customer
from ..products.models import Product

from ..products.serializers import ProductSerializer


class OrderSerializer(ModelSerializer):

    #orders = OrderProductSerializer(many=True,read_only=True)
    #orderproducts = ProductSerializer(many=True)
    #orderproducts = OrderProductSerializer(many=True)
    class Meta:
        model = Order
        fields = ('id','is_sales_order','order_date','delivery_date','vendors','customers')
        #fields = "__all__"
    # def create(self, validated_data):
    #     print(validated_data)
    #     products = validated_data['orders']
    #     #validated_data.pop('orderproducts')
    #     order = Order.objects.create(**validated_data)
    #     for orderproduct in products:
    #         product_details = Product.objects.get(id=orderproduct['id'])
    #         if order.is_sales_order and product_details.available_stock >= orderproduct['quantity'] :
    #             product_details.available_stock = product_details.available_stock - orderproduct['quantity']
    #             product_details.save()
    #         elif not order.is_sales_order:
    #             product_details.available_stock = product_details.available_stock + orderproduct['quantity']
    #             product_details.save()
    #         order_products.create(order=order,product=product_details,quantity=orderproduct['quantity'])
    #     return order

class CustomerSerializer(ModelSerializer):

    class Meta:
        model = Customer
        fields = "__all__"

class VendorSerializer(ModelSerializer):

    class Meta:
        model = Vendor
        fields = "__all__"

class OrderProductSerializer(ModelSerializer):

    #product = ProductSerializer(partial=True)
    #order = OrderSerializer(partial=True)

    #order = OrderSerializer()
    #orderproducts = OrderProductSerializer(many=True)

    class Meta:
        model = OrderProduct
        fields = ('product','order','quantity')