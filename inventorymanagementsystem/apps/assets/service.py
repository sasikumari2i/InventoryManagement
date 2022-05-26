import io
from datetime import date, timedelta
from django.db import transaction
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework.exceptions import NotFound
import datetime

from .serializers import AssetSerializer, RepairingStockSerializer
from .models import Asset, RepairingStock
from ..orders.models import Customer
from ..products.models import Product, Category
from ..payments.models import Invoice
from ..products.serializers import ProductSerializer
from utils.exceptionhandler import CustomException


class AssetService:
    """Performs asset related operations like add new asset for a customer,
    update asset details"""

    @transaction.atomic()
    def create(self, validated_data, organisation_uid):
        """Creates new Asset from the given data"""

        try:
            product = Product.objects.get(
                organisation_id=organisation_uid,
                product_uid=validated_data.data["product"],
            )
            customer = Customer.objects.get(
                organisation_id=organisation_uid,
                customer_uid=validated_data.data["customer"],
            )

            try:
                asset = Asset.objects.get(
                    product_id=product.id,
                    serial_no=validated_data.data["serial_no"],
                    is_active=True,
                )
                raise CustomException(400, "This product is already assigned")
            except Asset.DoesNotExist:
                pass

            if product.available_stock <= 0:
                raise CustomException(400, "Product is out of Stock")
            new_asset = Asset.objects.create(
                name=validated_data.data["name"],
                serial_no=validated_data.data["serial_no"],
                customer_id=validated_data.data["customer"],
                organisation_id=organisation_uid,
                product_id=validated_data.data["product"],
            )
            product.available_stock -= 1
            product.save()
            return new_asset
        except KeyError as exc:
            raise CustomException(400, "Exception in Asset Service")
        except Product.DoesNotExist:
            raise CustomException(400, "Invalid Product")
        except Customer.DoesNotExist:
            raise CustomException(400, "Invalid Customer")

    def update(self, instance, request):
        """Updates the Asset from the given data"""

        try:
            if not instance.is_active:
                raise CustomException(400, "Only active assets can be updated")
            customer = Customer.objects.get(
                customer_uid=request["customer"], organisation_id=instance.organisation
            )
            product = Product.objects.get(
                product_uid=request["product"], organisation_id=instance.organisation
            )
            instance.updated_date = date.today()
            if product.id != instance.product_id:
                if product.available_stock <=0:
                    raise CustomException(400,"Product is out of stock")
                product.available_stock -= 1
                product.save()
                new_product = Product.objects.get(product_uid=instance.product_id)
                new_product.available_stock += 1
                new_product.save()
            return instance
        except Customer.DoesNotExist:
            raise CustomException(404, "Invalid Customer")
        except Product.DoesNotExist:
            raise CustomException(404, "Invalid Product")
        except KeyError:
            raise CustomException(400, "Product and Customer is mandatory for updating")

    @transaction.atomic()
    def close_asset(self, asset_details, data):
        """Update Asset status to False"""

        try:
            is_active = asset_details.is_active
            response = {}
            if not is_active:
                response = {"message": "It is already not active"}
            elif is_active:
                asset_details.is_active = False
                asset_details.updated_date = date.today()

                try:
                    returned_date = datetime.datetime.strptime(
                        data["return_date"], "%Y-%m-%d"
                    )
                    if returned_date > datetime.datetime.today():
                        raise CustomException(
                            400, "Returned Date cannot be after today"
                        )
                except KeyError:
                    data["return_date"] = datetime.datetime.today()

                asset_details.return_date = data["return_date"]
                asset_details.save()
                response = {"message": "Assigned asset is closed"}
            return response
        except NotFound:
            raise CustomException(
                400, "Internal error in updating active status in asset"
            )


class RepairingStockService:
    """Performs Repairing Stock related operations like add new repairing stock for an asset,
        update repairing stock details"""

    @transaction.atomic()
    def create(self, validated_data, organisation_uid):
        """Creates new Repairing Stock for the given Asset"""

        try:
            asset = Asset.objects.get(
                organisation_id=organisation_uid, asset_uid=validated_data.data["asset"]
            )

            try:
                repairing_stock = RepairingStock.objects.get(
                    asset_id=validated_data.data["asset"], is_active=True
                )
                raise CustomException(400, "This product is already in repairing stock")
            except RepairingStock.DoesNotExist:
                pass

            if asset.is_active:
                raise CustomException(
                    400, "Cannot be created, Assigned is still active"
                )

            new_repairing_stock = RepairingStock.objects.create(
                serial_no=asset.serial_no,
                asset_id=validated_data.data["asset"],
                product_id=asset.product_id,
                organisation_id=organisation_uid,
            )
            return new_repairing_stock
        except KeyError as exc:
            raise CustomException(400, "Exception in Repairing Stock Service")
        except Asset.DoesNotExist:
            raise CustomException(400, "Invalid Asset")

    def update(self, instance, request):
        """Updates Repairing Asset for the given data"""

        try:
            if not instance.is_active:
                raise CustomException(
                    400, "Only active repairing stocks can be updated"
                )
            asset = Asset.objects.get(
                asset_uid=request.data["asset"],
                product_uid=request.data["product"],
                organisation_uid=instance.organisation,
            )
            instance.updated_date = date.today()
            return instance
        except Asset.DoesNotExist:
            raise CustomException(404, "Invalid Asset")

    @transaction.atomic()
    def close_repairing_stock(self, repairing_stock_details, data):
        """Update Reparing status to False and reflects to the product accordingly"""

        try:
            is_active = repairing_stock_details.is_active
            response = {}
            if not is_active:
                response = {"message": "It is already not active"}
            elif is_active:
                repairing_stock_details.is_active = False
                repairing_stock_details.updated_date = date.today()

                try:
                    closed_date = datetime.datetime.strptime(
                        data["closed_date"], "%Y-%m-%d"
                    )
                    if closed_date > datetime.datetime.today():
                        raise CustomException(400, "Closed Date cannot be after today")
                except KeyError:
                    data["closed_date"] = datetime.datetime.today()

                repairing_stock_details.closed_date = data["closed_date"]
                repairing_stock_details.save()
                product = Product.objects.get(
                    product_uid=repairing_stock_details.product_id
                )
                product.available_stock = product.available_stock + 1
                product.save()
                response = {"message": "Repairing Stock asset is closed"}
            return response
        except NotFound:
            raise CustomException(
                400, "Internal error in updating active status in repairing stock"
            )
