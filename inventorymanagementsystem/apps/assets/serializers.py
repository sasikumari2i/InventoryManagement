from rest_framework import serializers

from .models import Asset, RepairingStock
from ..products.serializers import InventorySerializer

class AssetSerializer(serializers.ModelSerializer):

    inventory = InventorySerializer()
    class Meta:
        model = Asset
        fields = ("asset_uid", "inventory", "customer", "is_active")


class RepairingStockSerializer(serializers.ModelSerializer):

    asset = AssetSerializer()
    class Meta:
        model = RepairingStock
        fields = (
            "repairing_stock_uid",
            "asset",
            "closed_date",
            "is_active",
        )


class RepairingStockCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairingStock
        fields = ("asset",)


class CloseAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairingStock
        fields = ("asset",)
