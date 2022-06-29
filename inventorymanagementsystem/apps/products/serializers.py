from rest_framework import serializers

from .models import Product, Category, Inventory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("category_uid", "name", "description",)


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
            # "created_date",
            # "updated_date",
        )


class InventorySerializer(serializers.ModelSerializer):

    # product = ProductSerializer()

    class Meta:
        model = Inventory
        # depth = 1
        fields = (
            "inventory_uid",
            "product",
            "serial_no",
            "is_available"
        )


