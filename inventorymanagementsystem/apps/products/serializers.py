from rest_framework import serializers

from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("category_uid", "name", "description", "created_date", "updated_date")


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "product_uid",
            "name",
            "description",
            "available_stock",
            "price",
            "category",
            "created_date",
            "updated_date",
        )
