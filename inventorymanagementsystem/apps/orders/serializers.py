from rest_framework import serializers

from .models import Vendor, Order,OrderProduct,Customer
from ..products.models import Product

from ..products.serializers import ProductSerializer

#class OrderRequestSerializer(serializers.Serializer):
 #   class Meta :
  #      fields = ('product',)


class OrderProductSerializer(serializers.ModelSerializer):


    #product = ProductSerializer(partial=True)
    #order = OrderSerializer(partial=True)

    #order = OrderSerializer()
    #orderproducts = OrderProductSerializer(many=True)

    #product = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    #order = OrderSerializer()

    class Meta:
        model = OrderProduct
        #depth = 1
        #fields = ('product','quantity')
        exclude = ('id','order')

class OrderSerializer(serializers.ModelSerializer):

    orderproducts = OrderProductSerializer(many=True)
    #orderproducts = ProductSerializer(many=True)
    #orderproducts = OrderProductSerializer(many=True)
    #orders = serializers.RelatedField(read_only=True)

    class Meta:
        model = Order
        #depth = 1
        fields = ('id','is_sales_order','order_date','delivery_date','orderproducts','vendors','customers')
        #fields = "__all__"


    def create(self, validated_data):
    #     print(validated_data)
        products = validated_data['orderproducts']
        validated_data.pop('orderproducts')
      #  for product in products:
        order = Order.objects.create(**validated_data)
    #     products = validated_data['orders']
    #     order = Order.objects.create(**validated_data)
    #     for orderproduct in products:
    #         print(orderproduct)
    #         product_details = Product.objects.get(id=orderproduct['id'])
    #         if order.is_sales_order and product_details.available_stock >= orderproduct['quantity'] :
    #             product_details.available_stock = product_details.available_stock - orderproduct['quantity']
    #             product_details.save()
    #         elif not order.is_sales_order:
    #             product_details.available_stock = product_details.available_stock + orderproduct['quantity']
    #             product_details.save()
    #         order_products.create(order=order,product=product_details,quantity=orderproduct['quantity'])
        return order

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = "__all__"

class VendorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor
        fields = "__all__"
