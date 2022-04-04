from rest_framework import serializers
from .models import Product, Category

class CategorySerializer (serializers.ModelSerializer):

    #products = ProductSerializer(read_only=True)

    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer (serializers.ModelSerializer):

    #category = CategorySerializer()

    class Meta:
        model = Product
        #fields = ('id','name','description','available_stock','price')
        fields = '__all__'





