import io
from datetime import date, timedelta
from django.db import transaction
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework.exceptions import NotFound

from .serializers import AssetSerializer, RepairingStockSerializer
from .models import Asset, RepairingStock
from ..orders.models import Customer
from ..products.models import Product,Category
from ..payments.models import Invoice
from ..products.serializers import ProductSerializer
from utils.exceptionhandler import CustomException


class AssetService:
    """Performs order related operations like add new order, get single order,
    get all orders, update an order and delete order"""

    @transaction.atomic()
    def create(self, validated_data, organisation):
        """Creates new order from the given data"""

        try:
            product = Product.objects.get(organisation=organisation,
                                             id=validated_data.data['product'])
            customer = Customer.objects.get(organisation=organisation,
                                            id=validated_data.data['customer'])

            new_asset = Asset.objects.create(name=validated_data.data['name'],
                                             serial_no=validated_data.data['serial_no'],
                                             customer_id=validated_data.data['customer'],
                                             organisation_id=organisation,
                                             product_id=validated_data.data['product'])
            product.available_stock -= 1
            product.save()
            return new_asset
        except KeyError as exc:
            raise CustomException(400, "Exception in Asset Service")
        except Product.DoesNotExist:
            raise CustomException(400, "Invalid Product")
        except Customer.DoesNotExist:
            raise CustomException(400, "Invalid Customer")


class RepairingStockService:

    @transaction.atomic()
    def create(self, validated_data, organisation):
        try:
            asset = Asset.objects.get(organisation=organisation,
                                      id=validated_data.data['asset'])

            new_repairing_stock = RepairingStock.objects.create(serial_no=asset.serial_no,
                                             asset_id=validated_data.data['asset'],
                                             product_id=asset.product_id,
                                             organisation_id=organisation)
            return new_repairing_stock
        except KeyError as exc:
            raise CustomException(400, "Exception in Repairing Stock Service")
        except Asset.DoesNotExist:
            raise CustomException(400, "Invalid Asset")