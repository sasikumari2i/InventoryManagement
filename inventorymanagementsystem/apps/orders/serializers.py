from rest_framework.serializers import ModelSerializer

from .models import Vendor, Order,OrderProduct

from ..products.serializers import ProductSerializer

class OrderSerializer(ModelSerializer):

    products = ProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id','is_sales_order','order_date','delivery_date','products','vendors','customers')

    def create(self, validated_data):
        print("Inside Createe")
         #= order_data['products']
        print(validated_data)
        products = validated_data.pop('products')
        order = Order.objects.create(**validated_data)
        for product in products:
            print(product)
             #= product['quantity']
            quantity = product.pop('quantity')
            product_details = Product.objects.get(id=products['id'])
            if order.is_sales_order and product_details.available_stock >= quantity:
                product_details.available_stock = product_details.available_stock - quantity
                product_details.save()
            elif not order.is_sales_order:
                product_details.available_stock = product_details.available_stock + quantity
                product_details.save()
            else:
                raise Exception("Enter only available stock")

            order_product = OrderProduct.objects.create(product=product_details, order=order, quantity=quantity)
        return order


class OrderProductSerializer (ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = '__all__'

