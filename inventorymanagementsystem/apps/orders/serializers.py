from rest_framework.serializers import ModelSerializer

from .models import Vendor, Order,OrderProduct
from ..products.models import Product

from ..products.serializers import ProductSerializer

class OrderSerializer(ModelSerializer):

    #products = ProductSerializer(many=True)
    class Meta:
        model = Order
        fields = ('id','is_sales_order','order_date','delivery_date','vendors','customers')


class OrderProductSerializer(ModelSerializer):

    #order = OrderSerializer()
    #orderproducts = ProductSerializer(many=True)

    class Meta:
        model = OrderProduct
        fields = ('product','order','quantity')

    # def create(self, validated_data):
    #     products = validated_data['orderproducts']
    #     validated_data.pop('orderproducts')
    #     order = Order.objects.create(validated_data)
    #     for product in products:
    #         product_details = Product.objects.get(id=product['id'])
    #         if order.is_sales_order and product_details.available_stock >= product['quantity'] :
    #             product_details.available_stock = product_details.available_stock - quantity
    #             product_details.save()
    #         elif not order.is_sales_order:
    #             product_details.available_stock = product_details.available_stock + quantity
    #             product_details.save()



