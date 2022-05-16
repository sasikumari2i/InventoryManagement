from rest_framework import serializers

from .models import Product, Category

class CategorySerializer (serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id','name','description','created_date','updated_date')
        # fields = '__all__'

class ProductSerializer (serializers.ModelSerializer):

    # write_only_fields = ('organisation',)

    class Meta:
        model = Product
        fields = ('id','name','description','available_stock','price','category','created_date',
                  'updated_date')




