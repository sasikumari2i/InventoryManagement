from rest_framework import serializers

from .models import Asset, RepairingStock


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ("asset_uid", "name", "product", "customer", "serial_no", "is_active")


class RepairingStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairingStock
        fields = (
            "repairing_stock_uid",
            "asset",
            "product",
            "serial_no",
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
