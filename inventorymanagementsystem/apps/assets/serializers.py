from rest_framework import serializers

from .models import Asset, RepairingStock
from ..products.serializers import InventorySerializer
from django.core.exceptions import ValidationError
from utils.exceptionhandler import CustomException

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

    # def validate_asset(self, asset):
    #         print("Asasasa")
    #         repairing_stock = RepairingStock.objects.get(
    #             asset_id=validated_data["asset"]
    #         )
    #         raise CustomException(400, "Duplicate Asset")

class CloseAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairingStock
        fields = ("asset",)
