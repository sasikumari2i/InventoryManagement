from rest_framework import serializers
from .models import Product, Category

class CategorySerializer (serializers.ModelSerializer):

    class Meta:
        model = Category
        depth = 1
        fields = ('id','name','description',)

class ProductSerializer (serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id','name','description','available_stock','price','category')





